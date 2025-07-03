import math
import re
import typing
import unicodedata
import PIL.Image
import beet
import beet.contrib.vanilla
import model_resolver
import model_resolver.utils

def main(ctx: beet.Context):
   icon = beet.PngFile(PIL.Image.open('in/pack.png'))
   ctx.assets.icon = icon
   ctx.data.icon = icon
   datapack = ctx.data['tryashtar.shulker_preview']
   resourcepack = ctx.assets['tryashtar.shulker_preview']
   # to do: when https://github.com/mcbeet/beet/pull/472 is merged, use 'minecraft' field
   target_version = ctx.meta['minecraft_version']
   
   # flat items can have their actual textures added to the font
   # but 3D models like blocks need to be rendered and stored separately in the pack
   # ideally in a big grid like a normal font provider texture
   ctx.meta['model_resolver'] = {
      'minecraft_version': target_version,
      'preferred_minecraft_generated': 'java',
      'special_rendering': True,
      'use_cache': True
   }
   render = model_resolver.Render(ctx=ctx)
   render.default_render_size = 64
   
   # the renderer doesn't provide a simple model -> image API
   # instead, we feed it many models with output paths, then it saves them all to the pack at once
   # but we don't want them in the pack, we want them in a big grid
   # so we keep track of the output paths so we can load the generated images, then delete them from the pack
   rendered_sprites: list[str] = []
   atlas_sprites: list[str] = []
   
   font = FontManager(rows=3)
   next_slot = font.get_space(15)
   empty_slot = font.get_space(18)
   overlay = font.get_space(-3)
   tooltip_push_back = font.get_space(-4)
   tooltip_push_fwd = font.get_space(8)
   row_end = font.get_space(-162)
   lang = resourcepack.languages['en_us']
   for tex, tip, bottom in [('shulker_box', 'shulker_tooltip', 20), ('generic_54', 'ender_tooltip', 27)]:
      ascent = 8
      slices = [{'height':8,'range':[0]},{'height':8,'range':[2,3,4,5,6,7,8,bottom]}]
      text = ''
      for section in slices:
         for include in section['range']:
            positive = ['\u0000'] * (256 // section['height'])
            negative = ['\u0000'] * (256 // section['height'])
            pos = font.next_char()
            neg = font.next_char()
            positive[include] = pos
            negative[include] = neg
            font.add_provider({"type": "bitmap", "file": f"minecraft:gui/container/{tex}.png", "ascent": ascent, "height": section['height'], "chars": positive})
            font.add_provider({"type": "bitmap", "file": f"minecraft:gui/container/{tex}.png", "ascent": -32768, "height": -section['height'], "chars": negative})
            ascent -= section['height']
            text += pos + neg + overlay
      lang.data[f"tryashtar.shulker_preview.{tip}"] = tooltip_push_back + text + tooltip_push_fwd
   lang.data['tryashtar.shulker_preview.empty_slot'] = empty_slot
   lang.data['tryashtar.shulker_preview.row_end'] = row_end
   missing = font.add_sprite('tryashtar.shulker_preview:missingno')
   for row in range(font.rows):
      lang.data[f'tryashtar.shulker_preview.missingno.{row}'] = missing['rows'][row] + missing['negative'] + next_slot

   # the goal is to convert every vanilla item model definition to text components
   # anything we can draw "all at once" gets a lang file entry consisting of its characters
   # most models can be entirely drawn all at once just by looking up their lang file entry with a macro
   # but a few need special command logic written by hand
   model_translations: dict[str, list[str]] = {}
   overlay_translations: dict[str, list[str]] = {}
   
   # even among models that can't be drawn with a simple macro, there are common patterns
   # for example, many models are simply a single texture with a hardcoded color
   # to make the item-drawing function more efficient, we want to detect these models in groups and do the special logic
   # so collect models into these groups with known strategies for special drawing
   PropertyEntry = typing.TypedDict('PropertyEntry', {'check': str, 'true': str, 'false': str})
   ArmorTrims = typing.TypedDict('ArmorTrims', {'model': str, 'overrides': dict[str, TextureColor]})
   ArmorEntry = typing.TypedDict('ArmorEntry', {'trims': dict[str, TextureColor], 'models': list[ArmorTrims]})
   simple_tinted: dict[str, int] = {}
   simple_property: dict[str, PropertyEntry] = {}
   potionlike: dict[int, dict[str, list[str]]] = {}
   armor: list[ArmorEntry] = []
   
   vanilla = beet.contrib.vanilla.Vanilla(ctx, minecraft_version=target_version)
   block_atlas = vanilla.assets.atlases['minecraft:blocks']
   
   ModelLayer = typing.TypedDict('ModelLayer', {'layer': str, 'tint': dict[str, typing.Any] | None})
   def get_model_layers(item_model: dict[str, typing.Any]) -> list[ModelLayer] | None:
      model_type = short(item_model['type'])
      match model_type:
         case 'model':
            tints: list[dict[str, typing.Any]] = item_model.get('tints', [])
            model_name = canon(item_model['model'])
            model = vanilla.assets.models[model_name]
            layers = generated_layers(vanilla.assets.models, model)
            if layers is None:
               # this is a 3D model, render it and use that texture as the single layer
               gen_name = model_name + '.model'
               if gen_name not in rendered_sprites:
                  render.add_model_task(
                     model = model_name,
                     path_ctx = gen_name,
                     animation_mode = 'one_file'
                  )
                  rendered_sprites.append(gen_name)
               layers = [gen_name]
            else:
               for layer in layers:
                  if layer not in atlas_sprites:
                     atlas_sprites.append(layer)
            if len(tints) > len(layers):
               return None
            return [{'layer':layers[i], 'tint':tints[i] if i < len(tints) else None} for i in range(len(layers))]
         case 'special':
            match short(item_model['model']['type']):
               case 'chest' | 'conduit' | 'head' | 'player_head' | 'shulker_box' | 'bed' | 'banner':
                  gen_name = name + '.item'
                  if gen_name not in rendered_sprites:
                     render.add_item_task(
                        item = model_resolver.Item(id=name, components={'minecraft:item_model':name}),
                        path_ctx = gen_name,
                        animation_mode = 'one_file'
                     )
                     rendered_sprites.append(gen_name)
                  return [{'layer':gen_name, 'tint':None}]
               case _:
                  return None
         case 'composite':
            combined = []
            for entry in item_model['models']:
               result = get_model_layers(entry)
               if result is None:
                  return None
               combined.extend(result)
            return combined
         case _:
            return None
   
   def handle_layered(name: str, layers: list[ModelLayer]) -> bool:
      has_tints = [i for i, layer in enumerate(layers) if layer['tint'] is not None]
      if len(has_tints) == 0:
         model_translations[name] = [layer['layer'] for layer in layers]
         return True
      if has_tints == [0]:
         model_translations[name] = [layers[0]['layer']]
         if len(layers) > 1:
            overlay_translations[name] = [layer['layer'] for layer in layers[1:]]
         tint = layers[0]['tint']
         assert tint is not None
         # simple trick, vanilla items use this exact configuration which we can precompute
         if short(tint['type']) == 'grass':
            if tint['downfall'] == 1.0 and tint['temperature'] == 0.5:
               tint['type'] = 'minecraft:constant'
               tint['value'] = 0xff7bbd6b
         match (short(tint['type']), len(layers)):
            case ('constant', 1):
               simple_tinted[name] = tint['value']
               return True
            case ('potion', 2):
               if tint['default'] not in potionlike:
                  potionlike[tint['default']] = {}
               potionlike[tint['default']][name] = [layer['layer'] for layer in layers]
               return True
            case _:
               return False
      return False
   
   def dict_diff(d1: dict, d2: dict) -> dict:
      result = {}
      for key, value in d1.items():
         if key not in d2 or d2[key] != value:
            result[key] = value
      return result
   
   def handle_select(name: str, item_model: dict[str, typing.Any]) -> bool:
      match short(item_model['property']):
         case 'trim_material':
            # armor tends to follow a specific pattern
            # with no trim, it renders some untinted layers
            # with a trim, it renders those same untinted layers with one trim texture on top
            # (and a slightly different trim texture when the material matches)
            # check that this item matches this exact pattern so we can render it correctly
            common_base: list[str] | None = None
            trims: dict[str, TextureColor] = {}
            layers = get_model_layers(item_model['fallback'])
            if layers is not None and all(x['tint'] is None for x in layers):
               common_base = [x['layer'] for x in layers]
            if common_base is None:
               return False
            for case in item_model['cases']:
               layers = get_model_layers(case['model'])
               if layers is None:
                  return False
               if not all(x['tint'] is None for x in layers):
                  return False
               all_layers = [x['layer'] for x in layers]
               if len(all_layers) != len(common_base) + 1:
                  return False
               if all_layers[:len(common_base)] != common_base:
                  return False
               perm = get_texture_from_atlas_entry(vanilla.assets.textures, block_atlas, all_layers[-1])
               if perm is None:
                  return False
               trims[canon(case['when'])] = perm
            model_translations[name] = common_base
            for trim in trims.values():
               overlay_translations[trim['texture']] = [trim['texture']]
            for entry in armor:
               difference = dict_diff(trims, entry['trims'])
               if len(difference) <= 2:
                  entry['models'].append({'model':name, 'overrides':difference})
                  return True
            armor.append({'trims':trims, 'models':[{'model':name, 'overrides':{}}]})
            return True
         case _:
            return False
   
   def handle_condition(name: str, item_model: dict[str, typing.Any]) -> bool:
      match short(item_model['property']):
         case 'broken':
            check = 'max_damage,!unbreakable,damage~{durability:{max:1}}'
            true_name = name + '.broken'
         case 'has_component':
            component = item_model['component']
            check = short(component)
            true_name = name + '.' + check
         case 'component':
            component = item_model['predicate']
            predicate = item_model['value']
            # to do: convert to SNBT
            check = f'{short(component)}~{predicate}'
            true_name = name + '.check'
            print(f'Model {name} is using component condition! {item_model}')
         case 'damaged':
            check = 'max_damage,!unbreakable,damage~{damage:{min:1}}'
            true_name = name + '.damaged'
         case _:
            return False
      on_true = get_model_layers(item_model['on_true'])
      on_false = get_model_layers(item_model['on_false'])
      # all(x['tint'] is None for x in layers)
      if on_true is not None and on_false is not None:
         false_name = name
         model_translations[true_name] = [x['layer'] for x in on_true]
         model_translations[false_name] = [x['layer'] for x in on_false]
         simple_property[name] = {'check':check, 'true': true_name, 'false': false_name}
         return True
      return False
   
   for name, entry in vanilla.assets.item_models.items():
      name = canon(name)
      squashed_model = squash_conditions(entry.data['model'])
      result = get_model_layers(squashed_model)
      if result is not None:
         handled = handle_layered(name, result)
      else:
         handled = False
      if not handled:
         model_type = short(squashed_model['type'])
         match model_type:
            case 'select':
               handled = handle_select(name, squashed_model)
            case 'condition':
               handled = handle_condition(name, squashed_model)
            case _:
               handled = False
      if not handled:
         print(f'Unhandled item model {name}: {squashed_model}')

   render.run()
   generated_entries = [(ctx.assets.textures[x].image, x) for x in rendered_sprites]
   grid_img, grid_refs = make_grid(generated_entries, render.default_render_size)
   for path in rendered_sprites:
      del ctx.assets.textures[path]
   resourcepack.textures['block_sheet'] = beet.Texture(grid_img)
   font.add_grid('block_sheet', grid_refs)
   for entry in atlas_sprites:
      texture = get_texture_from_atlas_entry(vanilla.assets.textures, block_atlas, entry)
      if texture is not None:
         font.add_sprite(texture['texture'])
      else:
         print(f'Texture not found in atlas {texture}')
   resourcepack.fonts['preview'] = font.build()
   
   for model, sprites in model_translations.items():
      data = [font.get_sprite(x) for x in sprites]
      for row in range(font.rows):
         lang.data[f'tryashtar.shulker_preview.item.{model}.{row}'] = overlay.join([x['rows'][row] + x['negative'] for x in data]) + next_slot

   for name, sprites in overlay_translations.items():
      data = [font.get_sprite(x) for x in sprites]
      for row in range(font.rows):
         lang.data[f'tryashtar.shulker_preview.layer.{name}.{row}'] = overlay + overlay.join([x['rows'][row] + x['negative'] for x in data]) + next_slot

   
   # we need the item_model component in a string to run the macro
   # but there's no way to do this if the component is set to the default for that item type (which it almost always is)
   # so we need to bake into the pack a way to convert an item type to an item_model component
   # fortunately, for every vanilla item, its default item_model component is identical to its ID
   # so this is a very easy default strategy
   # here we look for any item types that don't have this property
   # any that do can be specifically checked for and the correct item_model string assigned
   components = model_resolver.utils.get_default_components(ctx)
   unusual_default_models = {}
   for model, defaults in components.items():
      if defaults['minecraft:item_model'] != model:
         unusual_default_models[model] = defaults['minecraft:item_model']
   
   def check_model(models: typing.Iterable[str], extra: str | None=None) -> str:
      extra = '' if extra is None else extra + ','
      check = extra + '|'.join([f'item_model="{short(x)}"' for x in models])
      return f'if items entity @s contents *[{check}]'
   
   for row in range(font.rows):
      item_fn = [
         "# render the base item model",
         'data modify entity @s Item set from storage tryashtar.shulker_preview:data item',
         f'function tryashtar.shulker_preview:render/row_{row}/model',
      ]
      model_fn = [
         "# an item's rendering depends on its item_model component, so get that first",
         "# there's no known way to get the value of default components, so we have to guess by the ID",
         "# in vanilla, every single item has a default item_model that matches its ID",
         "# if there were any exceptions, we could list them here",
         "# when the item stack has a custom item_model component, use it instead",
         'data modify storage tryashtar.shulker_preview:data item.model set from storage tryashtar.shulker_preview:data item.id',
      ]
      for item, model in unusual_default_models.items():
         model_fn.append(f'execute if data storage tryashtar.shulker_preview:data item{{id:"{item}"}} run data modify storage tryashtar.shulker_preview:data item.model set value "{model}"')
      model_fn.extend([
         'data modify storage tryashtar.shulker_preview:data item.model set from storage tryashtar.shulker_preview:data item.components."minecraft:item_model"',
         '',
         "# models that require special rendering, like component checks or colored layers",
      ])
      
      model_fn.append(f'execute {check_model(simple_property.keys())} run return run function tryashtar.shulker_preview:render/row_{row}/model/property')
      property_fn = []
      for model, entry in simple_property.items():
         property_fn.extend([
            f'execute {check_model([model], entry['check'])} run return run data modify storage tryashtar.shulker_preview:data tooltip append value {{translate:"tryashtar.shulker_preview.item.{entry['true']}.{row}",fallback:"%s",with:[{{translate:"tryashtar.shulker_preview.missingno.{row}"}}]}}',
            f'execute {check_model([model])} run return run data modify storage tryashtar.shulker_preview:data tooltip append value {{translate:"tryashtar.shulker_preview.item.{entry['false']}.{row}",fallback:"%s",with:[{{translate:"tryashtar.shulker_preview.missingno.{row}"}}]}}',
         ])
      datapack.functions[f'render/row_{row}/model/property'] = beet.Function(property_fn)
      
      model_fn.append(f'execute {check_model(simple_tinted.keys())} run return run function tryashtar.shulker_preview:render/row_{row}/model/tinted')
      tinted_fn = []
      for model, tint in simple_tinted.items():
         tinted_fn.append(f'execute {check_model([model])} run return run data modify storage tryashtar.shulker_preview:data tooltip append value {{translate:"tryashtar.shulker_preview.item.{model}.{row}",color:"{color_hex(tint)}",fallback:"%s",with:[{{translate:"tryashtar.shulker_preview.missingno.{row}"}}]}}')
      datapack.functions[f'render/row_{row}/model/tinted'] = beet.Function(tinted_fn)
      
      for default_color, data in potionlike.items():
         fn_name = f'render/row_{row}/model/potion' if len(potionlike) == 1 else f'render/row_{row}/model/potion/{default_color}'
         model_fn.append(f'execute {check_model(data.keys())} run return run function tryashtar.shulker_preview:{fn_name}')
         color = color_hex(default_color)
         potionlike_fn = [
            '# potions can be any color, so a macro is needed',
            f'data modify storage tryashtar.shulker_preview:data item merge value {{red:"{color[1:3]}",green:"{color[3:5]}","blue":"{color[5:7]}"}}',
            'execute store success score #has_color shulker_preview store result score #color shulker_preview run data get storage tryashtar.shulker_preview:data item.components."minecraft:potion_contents".custom_color',
            'execute if score #has_color shulker_preview matches 1 run function tryashtar.shulker_preview:render/convert_color',
            'execute if score #has_color shulker_preview matches 0 run function tryashtar.shulker_preview:render/potion_color',
            f'function tryashtar.shulker_preview:{fn_name}.macro with storage tryashtar.shulker_preview:data item',
         ]
         potionlike_fn2 = [
            '# potions render with a base layer and a colored layer',
            f'$data modify storage tryashtar.shulker_preview:data tooltip append value [{{translate:"tryashtar.shulker_preview.item.$(model).{row}",color:"#$(red)$(green)$(blue)",fallback:"%s",with:[{{translate:"tryashtar.shulker_preview.missingno.{row}"}}]}},{{translate:"tryashtar.shulker_preview.layer.$(model).0.{row}",color:"white",fallback:"%s",with:[{{translate:"tryashtar.shulker_preview.missingno.{row}"}}]}}]',
         ]
         datapack.functions[fn_name] = beet.Function(potionlike_fn)
         datapack.functions[f'{fn_name}.macro'] = beet.Function(potionlike_fn2)
      
      model_fn.append(f'execute {check_model([model['model'] for entry in armor for model in entry['models']])} run return run function tryashtar.shulker_preview:render/row_{row}/model/armor')
      armor_fn = [
         "# armor starts with normal rendering of the base model",
         'function tryashtar.shulker_preview:render/row_0/model/simple.macro with storage tryashtar.shulker_preview:data item',
         '',
         "# then the trim overlay if present",
      ]
      for entry in armor:
         # kinda lazy way to come up with a name for the categories
         slot_name = entry['models'][0]['model'].split('_')[1]
         armor_fn.append(f'execute {check_model([model['model'] for model in entry['models']], 'trim')} run return run function tryashtar.shulker_preview:render/row_{row}/model/armor/{slot_name}')
         slot_fn = [
            "# render the armor trim overlay based on the material color",
            "# it's not as accurate as the true items which use paletted permutations",
            "# items of a matching material use a darker color",
         ]
         for model in entry['models']:
            for material, texture in model['overrides'].items():
               color = f',color:"{color_hex(texture['color'])}"' if texture['color'] is not None else ''
               slot_fn.append(f'execute {check_model([model['model']], f'trim~{{material:"{short(material)}"}}')} run return run data modify storage tryashtar.shulker_preview:data tooltip append value {{translate:"tryashtar.shulker_preview.layer.{texture['texture']}.0.{row}"{color},fallback:"%s",with:[{{translate:"tryashtar.shulker_preview.missingno.{row}"}}]}}')
         for material, texture in entry['trims'].items():
            color = f',color:"{color_hex(texture['color'])}"' if texture['color'] is not None else ''
            slot_fn.append(f'execute if items entity @s contents *[trim~{{material:"{short(material)}"}}] run return run data modify storage tryashtar.shulker_preview:data tooltip append value {{translate:"tryashtar.shulker_preview.layer.{texture['texture']}.0.{row}"{color},fallback:"%s",with:[{{translate:"tryashtar.shulker_preview.missingno.{row}"}}]}}')
         datapack.functions[f'render/row_{row}/model/armor/{slot_name}'] = beet.Function(slot_fn)
      datapack.functions[f'render/row_{row}/model/armor'] = beet.Function(armor_fn)
      
      model_fn.extend([
         '',
         'function tryashtar.shulker_preview:render/row_0/model/simple.macro with storage tryashtar.shulker_preview:data item'
      ])
      simple_fn = [
         "# macro for simple models that are just one or more uncolored layers",
         f'$data modify storage tryashtar.shulker_preview:data tooltip append value {{translate:"tryashtar.shulker_preview.item.$(model).{row}",fallback:"%s",with:[{{translate:"tryashtar.shulker_preview.missingno.{row}"}}]}}'
      ]
      datapack.functions[f'render/row_{row}/model/simple.macro'] = beet.Function(simple_fn)
      
      datapack.functions[f'render/row_{row}/item'] = beet.Function(item_fn)
      datapack.functions[f'render/row_{row}/model'] = beet.Function(model_fn)

TextureColor = typing.TypedDict('TextureColor', {'texture': str, 'color': int | None})
def get_texture_from_atlas_entry(textures: beet.NamespaceProxy[beet.Texture], atlas: beet.Atlas, entry: str) -> TextureColor | None:
   entry = canon(entry)
   _namespace, path = entry.split(':')
   for source in atlas.data['sources']:
      match short(source['type']):
         case 'directory':
            prefix = source['source'] + '/'
            if path.startswith(prefix):
               texture = canon(source['prefix'] + path.removeprefix(prefix))
               return {'texture': texture, 'color': None}
         case 'paletted_permutations':
            for base in source['textures']:
               prefix = canon(base) + '_'
               if entry.startswith(prefix):
                  material = entry.removeprefix(prefix)
                  if material in source['permutations']:
                     texture = textures[canon(source['permutations'][material])]
                     # kinda lazy way to get the color for this palette
                     r,g,b = texture.image.getpixel((0, 0))
                     color = r * 2**16 + g * 2**8 + b
                     return {'texture':canon(base), 'color':color}
         case _:
            pass
   return None

def color_hex(color: int):
   if color < 0:
      color += 2**32
   color %= 2**24
   return f'#{format(color, '06x')}'

# item models can have logic to switch to different models if certain conditions are met
# we have to check these conditions with commands
# some of them are impossible to detect, or can never be met while inside a container
# so we eliminate them, simplifying the model until it only has conditions we can check, or none at all
def squash_conditions(model: dict[str, typing.Any]) -> dict[str, typing.Any]:
   model_type = short(model['type'])
   match model_type:
      case 'condition':
         prop = short(model['property'])
         model['on_true'] = squash_conditions(model['on_true'])
         model['on_false'] = squash_conditions(model['on_false'])
         # the compass model ends up simplifying to a check for the lodestone component
         # we could check that with commands
         # but the simplified two models it picks between are the same, so no point in checking
         if model['on_true'] == model['on_false']:
            return model['on_true']
         match prop:
            # most of these can never be true for an item in a static container
            # keybind_down could be true, but we can't check it or update the lore dynamically
            # (and vanilla doesn't use it anyway)
            case 'bundle/has_selected_item' | 'carried' | 'extended_view' | 'fishing_rod/cast' | 'keybind_down' | 'selected' | 'using_item' | 'view_entity':
               return model['on_false']
            case _:
               return model
      case 'select':
         prop = short(model['property'])
         if 'fallback' in model:
            model['fallback'] = squash_conditions(model['fallback'])
         for case in model['cases']:
            case['model'] = squash_conditions(case['model'])
         match prop:
            # there is no context entity in a static container
            # we have no way of checking the local time or updating the lore dynamically
            case 'context_entity_type' | 'local_time':
               return model['fallback']
            # assume we are in the overworld
            # we could check it, but have no way of updating the lore dynamically
            # (vanilla doesn't use it anyway)
            case 'context_dimension':
               for case in model['cases']:
                  if case['when'] == 'overworld' or 'overworld' in case['when']:
                     return case['model']
               return model['fallback']
            # items in a static container are always in the gui context
            case 'display_context':
               for case in model['cases']:
                  if case['when'] == 'gui' or 'gui' in case['when']:
                     return case['model']
                  return model['fallback']
            # assume the player is right-handed
            # we have no way of checking or updating the lore dynamically
            case 'main_hand':
               for case in model['cases']:
                  if case['when'] == 'right' or 'right' in case['when']:
                     return case['model']
                  return model['fallback']
            case _:
               return model
      case 'range_dispatch':
         prop = short(model['property'])
         if 'fallback' in model:
            model['fallback'] = squash_conditions(model['fallback'])
         for case in model['entries']:
            case['model'] = squash_conditions(case['model'])
         match prop:
            # most of these can never be anything other than 0 for an item in a static container
            # we could conceivably check compass direction and time of day
            # but we have no way of updating the lore dynamically
            case 'compass' | 'cooldown' | 'crossbow/pull' | 'time' | 'use_cycle' | 'use_duration':
               for case in model['entries']:
                  if case['threshold'] == 0:
                     return case['model']
               return model['fallback']
            case _:
               return model
      case _:
         return model
   return model

def make_grid(entries: list[tuple[PIL.Image.Image, str]], icon_size: int) -> tuple[PIL.Image.Image, list[list[str | None]]]:
   width, height = grid_dimensions(len(entries))
   image = PIL.Image.new('RGBA', (width * icon_size, height * icon_size))
   path_return: list[list[str | None]] = [[None]*width for _ in range(height)]
   for i, (sprite, path) in enumerate(entries):
      pos_x = i % width
      pos_y = i // width
      path_return[pos_y][pos_x] = path
      x = pos_x * icon_size
      y = pos_y * icon_size
      image.paste(sprite, (x, y, x + icon_size, y + icon_size))
      # to do: with negatives, is this still necessary?
      for corner in (0, icon_size - 1):
         pixel = sprite.getpixel((corner, corner))
         assert type(pixel) is tuple
         r,g,b,a = pixel
         if a == 0:
            r,g,b = (139, 139, 139)
         image.putpixel((x + corner, y + corner), (r, g, b, max(a, 18)))
   return (image, path_return)

def grid_dimensions(area: int) -> tuple[int, int]:
   width = math.ceil(math.sqrt(area))
   height = width
   if width * (height - 1) >= area:
      height -= 1
   return (width, height)

# each item texture added to the font gets 4 characters: one for each container row, and a negative version
# this includes every entry in the grid
# when generating translations for full item models, we may sometimes need to overlay multiple textures
# therefore, it's helpful to be able to lookup the 4 characters from the item texture name
# this class keeps them in sprite_map while also generating the final providers
# note that the block grid for example has named texture entries, but the provider makes no mention of them, just the final grid
GridData = typing.TypedDict('GridData', {'rows': list[list[str]], 'negative': list[str]})
SpriteData = typing.TypedDict('SpriteData', {'rows': list[str], 'negative': str})
class FontManager:
   def __init__(self, rows: int):
      self.rows: int = rows
      self.last_char: int = 0
      self.spaces: dict[int, str] = {}
      self.sprites: dict[str, SpriteData] = {}
      self.grids: dict[str, GridData] = {}
      self.sprite_map: dict[str, SpriteData] = {}
      self.providers: list[dict[str, typing.Any]] = []
   
   def add_sprite(self, texture: str) -> SpriteData:
      if texture not in self.sprite_map:
         data: SpriteData = {'rows': [self.next_char() for _ in range(self.rows)], 'negative': self.next_char()}
         self.sprites[texture] = data
         self.sprite_map[texture] = data
      return self.sprite_map[texture]
   
   def add_grid(self, grid: str, textures: list[list[str | None]]):
      rows: list[list[str]] = [[] for _ in range(self.rows)]
      negative: list[str] = []
      for row in textures:
         for x in rows:
            x.append('')
         negative.append('')
         for texture in row:
            if texture is not None:
               rowchars = []
               for x in rows:
                  ch = self.next_char()
                  x[-1] += ch
                  rowchars.append(ch)
               n = self.next_char()
               negative[-1] += n
               self.sprite_map[texture] = {'rows': rowchars, 'negative': n}
            else:
               for x in rows:
                  x[-1] += '\u0000'
               negative[-1] += '\u0000'
      data: GridData = {'rows': rows, 'negative': negative}
      self.grids[grid] = data
     
   def add_provider(self, provider: dict[str, typing.Any]):
      self.providers.append(provider)
    
   def get_sprite(self, name: str) -> SpriteData:
      return self.sprite_map[name]
   
   def next_char(self):
      char = self.last_char + 1
      for low, high in [(0xd800, 0xdbff), (0xdc00, 0xdfff), (0x05c8, 0x05d2), (0x05e8, 0x06ff), (0x070b, 0x0710), (0x072d, 0x072f), (0x074b, 0x074f), (0x07a4, 0x07a5), (0x07b1, 0x07c2), (0x07f4, 0x07f5), (0x07fa, 0x07fc), (0x07fe, 0x0800), (0x082e, 0x0832), (0x083c, 0x0842), (0x0856, 0x0858), (0x085c, 0x0862), (0x0868, 0x0897), (0x08a0, 0x08a2), (0x08b2, 0x08b8), (0x08c5, 0x08c9), (0xfb34, 0xfb48), (0xfbbf, 0xfbd5), (0xfd8d, 0xfd94), (0xfdc5, 0xfdce), (0xfdf0, 0xfdf2), (0xfe72, 0xfe78), (0xfefa, 0xfefe)]:
         if low <= char <= high:
            char = high + 1
      while char in [0x0000, 0x000a, 0x00a7, 0x0025, 0x0590, 0x05be, 0x05c0, 0x05c3, 0x05c6, 0x0608, 0x060b, 0x060d, 0x0712, 0x081a, 0x0824, 0x0828, 0x200f, 0xfb1d, 0xfb1f] or unicodedata.bidirectional(chr(char)) in ['AL', 'R', 'NSM']:
         char += 1
      self.last_char = char
      return chr(char)
      
   def get_space(self, width: int) -> str:
      if width in self.spaces:
         return self.spaces[width]
      char = self.next_char()
      self.spaces[width] = char
      return char
   
   def build(self) -> beet.Font:
      result = beet.Font()
      providers = []
      if len(self.spaces) > 0:
         spaces = {}
         for width, char in self.spaces.items():
            spaces[char] = width
         providers.append({'type':'space','advances':spaces})
      providers.extend(self.providers)
      for path, data in self.sprites.items():
         for row, entry in enumerate(data['rows']):
            providers.append({'type':'bitmap','file':path,'ascent':-2 + (row * -18),'height':16,'chars':[entry]})
         providers.append({'type':'bitmap','file':path,'ascent':-32768,'height':-16,'chars':[data['negative']]})
      for path, data in self.grids.items():
         for row, entry in enumerate(data['rows']):
            providers.append({'type':'bitmap','file':path,'ascent':-2 + (row * -18),'height':16,'chars':entry})
         providers.append({'type':'bitmap','file':path,'ascent':-32768,'height':-16,'chars':data['negative']})
      result.data['providers'] = providers
      return result

def canon(location: str) -> str:
   return f'minecraft:{location}' if ':' not in location else location

def short(location: str) -> str:
   return location.removeprefix('minecraft:')

# find all the layers of a flat item sprite model
# all models of this kind ultimately parent to the builtin/generated model
# so if we don't find that, this is a 3D model that needs to be rendered instead
def generated_layers(source: beet.NamespaceProxy[beet.Model], model: beet.Model) -> list[str] | None:
   result: list[str | None] = []
   while 'parent' in model.data:
      if 'textures' in model.data:
         for name, path in model.data['textures'].items():
            match = re.match(r'layer(\d+)', name)
            if match:
               index = int(match.group(1))
               if index >= len(result):
                  result.extend([None] * (index - len(result) + 1))
               # child texture references override parent ones
               # so since we're traversing up the hierarchy, ignore layers that were already defined
               # looking for textures in the parent is probably overkill since in vanilla the layers are always on the bottom model
               # also this doesn't handle '#refs' to point to other defined textures
               # but why would a flat item sprite ever do that?
               if result[index] is None:
                  result[index] = canon(path)
      parent = canon(model.data['parent'])
      if parent == 'minecraft:builtin/generated':
         return [x for x in result if x is not None]
      model = source[parent]
   return None
