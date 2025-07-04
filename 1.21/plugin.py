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
   ctx.meta['model_resolver'] = {
      'minecraft_version': target_version,
      'preferred_minecraft_generated': 'java',
      'special_rendering': True,
      'use_cache': True
   }
   
   # every item texture needs to be added to the font
   # flat models (using builtin/generated) are composed of one or more atlas entries as layers
   # we can find these texture paths and reference them directly, adding each one to the font
   atlas_sprites: list[str] = []
   # 3D models like blocks need to be rendered and stored separately in the pack
   # we'll put them in a big grid like a normal font provider
   rendered_item_sprites: dict[str, str] = {}
   rendered_model_sprites: dict[str, str] = {}
   rendered_fake_sprites: dict[str, dict[str, typing.Any]] = {}
   
   # if an item model just consists of sprites, we can layer those sprites into one lang file entry
   model_translations: dict[str, list[str]] = {}
   # if the item model needs extra sprites drawn conditionally or with color, we need discrete entries for those
   overlay_translations: dict[str, list[str]] = {}
   
   # even among models that can't be drawn with a simple macro, there are common patterns
   # to make the item-drawing function more efficient, we want to detect these models in groups and do the special logic
   # so collect models into these groups with known strategies for special drawing
   PropertyEntry = typing.TypedDict('PropertyEntry', {'check': str, 'true': str, 'false': str})
   Trim = typing.TypedDict('Trim', {'texture': str, 'color': int | None, 'name': str})
   ArmorTrims = typing.TypedDict('ArmorTrims', {'model': str, 'dye': int | None, 'overrides': dict[str, Trim]})
   ArmorEntry = typing.TypedDict('ArmorEntry', {'trims': dict[str, Trim], 'models': list[ArmorTrims]})
   ModelSprite = typing.TypedDict('ModelSprite', {'sprite': str, 'tint': dict[str, typing.Any] | None})
   PropertyCheck = typing.TypedDict('PropertyCheck', {'check': typing.Callable[[str], str], 'values': list[str]})
   simple_tinted: dict[str, int] = {}
   simple_dye: dict[int, list[str]] = {}
   simple_property: dict[str, PropertyEntry] = {}
   dyed_overlays: list[str] = []
   potionlike: dict[int, dict[str, list[str]]] = {}
   firework: dict[int, list[str]] = {}
   maps: dict[int, list[str]] = {}
   armor: list[ArmorEntry] = []
   case_property: dict[str, PropertyCheck] = {}
   banners: dict[str, typing.Literal['banner', 'shield']] = {}
   pots: list[str] = []
   
   # we're going to enumerate every item model in vanilla, to collect their sprites and sort into patterns
   # what follows are some functions for handling particular item models
   vanilla = beet.contrib.vanilla.Vanilla(ctx, minecraft_version=target_version)
   block_atlas = vanilla.assets.atlases['minecraft:blocks']
   
   BannerShield = typing.TypedDict('BannerShield', {'banner': str, 'shield': str})
   banner_patterns: dict[str, BannerShield] = {}
   banner_atlas = vanilla.assets.atlases['minecraft:banner_patterns']
   shield_atlas = vanilla.assets.atlases['minecraft:shield_patterns']
   for pattern, file in vanilla.data.banner_patterns.items():
      asset = file.data['asset_id']
      namespace, path = canon(asset).split(':')
      final_banner = f'{namespace}:entity/banner/{path}'
      final_shield = f'{namespace}:entity/shield/{path}'
      banner_result = get_texture_from_atlas_entry(vanilla.assets.textures, banner_atlas, final_banner)
      shield_result = get_texture_from_atlas_entry(vanilla.assets.textures, shield_atlas, final_shield)
      if banner_result is not None and shield_result is not None:
         banner = banner_result['texture']
         shield = shield_result['texture']
         banner_patterns[pattern] = {'banner':banner, 'shield':shield}
   
   # pot patterns aren't data driven, we have to guess them from item names
   pot_patterns: dict[str, str] = {}
   pot_atlas = vanilla.assets.atlases['minecraft:decorated_pot']
   components = model_resolver.utils.get_default_components(ctx)
   blank = get_texture_from_atlas_entry(vanilla.assets.textures, pot_atlas, 'entity/decorated_pot/decorated_pot_side')
   if blank is not None:
      pot_patterns['minecraft:brick'] = blank['texture']
   for item in components.keys():
      item = short(item)
      if item.endswith('_pottery_sherd'):
         pattern = item.removesuffix('_pottery_sherd')
         texture = get_texture_from_atlas_entry(vanilla.assets.textures, pot_atlas, f'entity/decorated_pot/{pattern}_pottery_pattern')
         if texture is not None:
            pot_patterns[canon(item)] = texture['texture']

   # if this item model just consists of sprites (i.e. no conditions), return said sprites
   # many models are like this, and they're easier to render and check for in patterns
   def get_model_sprites(item_model: dict[str, typing.Any]) -> list[ModelSprite] | None:
      model_type = short(item_model['type'])
      match model_type:
         case 'model':
            # most item models are this, just a simple model
            # it could be a 3D model we need to render, or a flat item made of one or more layers
            tints: list[dict[str, typing.Any]] = item_model.get('tints', [])
            model_name = canon(item_model['model'])
            model = vanilla.assets.models[model_name]
            layers = generated_layers(vanilla.assets.models, model)
            if layers is None:
               # this is a 3D model, render it and use that texture as the single sprite
               gen_name = model_name + '.model'
               rendered_model_sprites[gen_name] = model_name
               layers = [gen_name]
            else:
               # this is a flat item, its sprites come from the atlas
               for layer in layers:
                  if layer not in atlas_sprites:
                     atlas_sprites.append(layer)
            # I don't really understand tints super well
            # I think each tint matches a layer, so it's correct to zip them like this?
            if len(tints) > len(layers):
               return None
            filtered_tints = [None if short(x['type']) == 'constant' and x['value'] == -1 else x for x in tints]
            return [{'sprite':layers[i], 'tint':filtered_tints[i] if i < len(tints) else None} for i in range(len(layers))]
         case 'special':
            # some special models are simple and can just be one sprite
            match short(item_model['model']['type']):
               case 'chest' | 'conduit' | 'head' | 'player_head' | 'shulker_box' | 'bed':
                  gen_name = name + '.item'
                  rendered_item_sprites[gen_name] = name
                  return [{'sprite':gen_name, 'tint':None}]
               case _:
                  return None
         case 'composite':
            # if all the models in this composite are made of sprites,
            # then the entire thing is just made of sprites
            # this codepath doesn't trigger in vanilla right now
            combined = []
            for entry in item_model['models']:
               result = get_model_sprites(entry)
               if result is None:
                  return None
               combined.extend(result)
            return combined
         case _:
            return None
   
   # when a model is made entirely of sprites, it may fall into one of a few patterns depending on whether or how they're tinted
   def handle_layered(name: str, layers: list[ModelSprite]) -> bool:
      tinted_layer_indices = [i for i, layer in enumerate(layers) if layer['tint'] is not None]
      if len(tinted_layer_indices) == 0:
         # none of the layers are tinted
         # great, we can just layer all the sprites into one entry
         model_translations[name] = [layer['sprite'] for layer in layers]
         return True
      if tinted_layer_indices == [0]:
         # only the first layer is tinted
         # we'll use one lang entry for the bottom layer,
         # and one more for everything on top
         model_translations[name] = [layers[0]['sprite']]
         if len(layers) > 1:
            overlay_translations[name] = [layer['sprite'] for layer in layers[1:]]
         tint = layers[0]['tint']
         assert tint is not None
         # simple trick, vanilla items use this exact configuration which we can precompute
         if short(tint['type']) == 'grass':
            if tint['downfall'] == 1.0 and tint['temperature'] == 0.5:
               tint['type'] = 'minecraft:constant'
               tint['value'] = 0xff7bbd6b
         match (short(tint['type']), len(layers)):
            case ('constant', 1):
               # only one layer tinted with a hardcoded color, very easy
               simple_tinted[name] = tint['value']
               return True
            case ('dye', 1):
               # only one layer tinted with dye color
               default = tint['default']
               if default not in simple_dye:
                  simple_dye[default] = []
               simple_dye[default].append(name)
               return True
            case ('potion', 2):
               # one layer tinted with potion tint, and one untinted layer on top
               # potions and tipped arrows match this pattern
               if tint['default'] not in potionlike:
                  potionlike[tint['default']] = {}
               potionlike[tint['default']][name] = [layer['sprite'] for layer in layers]
               return True
            case _:
               return False
      if len(layers) == 2 and layers[0]['tint'] is None and layers[1]['tint'] is not None:
         # one entry for the bottom layer, one for the top
         model_translations[name] = [layers[0]['sprite']]
         overlay_translations[name] = [layers[1]['sprite']]
         tint = layers[1]['tint']
         match short(tint['type']):
            case 'firework':
               default = tint['default']
               if default not in firework:
                  firework[default] = []
               firework[default].append(name)
               return True
            case 'map_color':
               default = tint['default']
               if default not in maps:
                  maps[default] = []
               maps[default].append(name)
               return True
            case _:
               return False
      return False
   
   # models that switch based on a property fall into a few patterns
   # we don't even necessarily need to implement a similar switch if the pattern is easier done another way
   def handle_select(name: str, item_model: dict[str, typing.Any]) -> bool:
      prop = short(item_model['property'])
      match prop:
         case 'trim_material':
            # armor tends to follow a specific pattern
            # with no trim, it renders some sprites
            # with a trim, it renders those same sprites with one trim sprite on top
            # (and a slightly different trim texture when the material matches)
            # check that this item matches this exact pattern
            # if it does, we can render it by always drawing the base, then checking the material to draw the trim
            common_base: list[ModelSprite]
            trims: dict[str, Trim] = {}
            layers = get_model_sprites(item_model['fallback'])
            if layers is None:
               return False
            common_base = layers
            for case in item_model['cases']:
               layers = get_model_sprites(case['model'])
               if layers is None:
                  return False
               if len(layers) != len(common_base) + 1:
                  return False
               if layers[:len(common_base)] != common_base:
                  return False
               texture = get_texture_from_atlas_entry(vanilla.assets.textures, block_atlas, layers[-1]['sprite'])
               if texture is None:
                  return False
               trim_name = short(texture['texture'])
               if trim_name.startswith('trims/items/') and trim_name.endswith('_trim'):
                  trim_name = 'trim.' + trim_name.removeprefix('trims/items/').removesuffix('_trim')
               trims[canon(case['when'])] = {'color':texture['color'], 'texture':texture['texture'], 'name':trim_name}
            if all(x['tint'] is None for x in common_base):
               # use one lang entry for the base sprites
               model_translations[name] = [x['sprite'] for x in common_base]
               default_color = None
            elif len(common_base) >= 1:
               tint = common_base[0]['tint']
               if tint is None:
                  return False
               if short(tint['type']) != 'dye':
                  return False
               if not all(x['tint'] is None for x in common_base[1:]):
                  return False
               default_color = tint['default']
               # dyeable leather armor matches this pattern
               # use one lang entry for the base dyed texture
               # and one more for everything on top
               model_translations[name] = [common_base[0]['sprite']]
               if len(common_base) > 1:
                  overlay_translations[name] = [x['sprite'] for x in common_base[1:]]
            else:
               return False
            for trim in trims.values():
               # use one lang entry for the trim sprite
               overlay_translations[trim['name']] = [trim['texture']]
            # each entry in the armor list has a map of trims, and list of models that use those trims
            # for example, all boot models use a trim map that points to the boot trim texture
            # if this model's trims match one we already have, add to its list, otherwise add a new entry
            # since matching materials use a darker color, there's usually one different trim in an otherwise perfect match
            # instead of creating a whole new entry, just keep that single override
            for entry in armor:
               difference = dict_diff(trims, entry['trims'])
               if len(difference) <= 1:
                  entry['models'].append({'model':name, 'dye': default_color, 'overrides':difference})
                  return True
            armor.append({'trims':trims, 'models':[{'model':name, 'dye': default_color, 'overrides':{}}]})
            return True
         case 'block_state' | 'charge_type':
            # all of these in vanilla just render completely different sprites
            # so we have no better strategy than adding all of them as lang entries and picking the right one
            fallback = get_model_sprites(item_model['fallback'])
            if fallback is None:
               return False
            if not all(x['tint'] is None for x in fallback):
               return False
            fallback_spr = [x['sprite'] for x in fallback]
            model_translations[name] = fallback_spr
            # the arrow charge type matches when there is any non-rocket item in the charged projectiles
            # checking for this is awkward with only one subcommand
            # it's easier to just let the rocket case come first so we don't have to
            if prop == 'charge_type':
               item_model['cases'].sort(key=lambda x: x['when'] == 'rocket', reverse=True)
            for case in item_model['cases']:
               layers = get_model_sprites(case['model'])
               if layers is None:
                  return False
               if not all(x['tint'] is None for x in layers):
                  return False
               case_spr = [x['sprite'] for x in layers]
               model_translations[name + '.' + case['when']] = case_spr
            match prop:
               case 'block_state':
                  block_prop = item_model['block_state_property']
                  check = lambda x: f'"minecraft:block_state"{{{block_prop}:"{x}"}}'
               case 'charge_type':
                  def charge_check(val: str) -> str:
                     match val:
                        case 'arrow':
                           return '"minecraft:charged_projectiles"[0]'
                        case 'rocket':
                           return '"minecraft:charged_projectiles"[{id:"minecraft:firework_rocket"}]'
                     raise ValueError(val)
                  check = charge_check
            case_property[name] = {'check': check, 'values': [case['when'] for case in item_model['cases']]}
            return True
         case _:
            return False
   
   # models that switch based on a condition
   # we need to decide what to do based on how complex the two options are
   def handle_condition(name: str, item_model: dict[str, typing.Any]) -> bool:
      prop = short(item_model['property'])
      match prop:
         case 'broken':
            # used by elytra in vanilla
            check = 'max_damage,!unbreakable,damage~{durability:{max:1}}'
            true_name = name + '.broken'
         case 'has_component':
            # used by wolf armor in vanilla
            component = item_model['component']
            check = short(component)
            true_name = name + '.' + check
         case 'component':
            # not used in vanilla
            # I don't even bother converting the predicate to SNBT here
            component = item_model['predicate']
            predicate = item_model['value']
            check = f'{short(component)}~{predicate}'
            true_name = name + '.check'
            print(f'Model {name} is using component condition! {item_model}')
         case 'damaged':
            # not used in vanilla
            check = 'max_damage,!unbreakable,damage~{damage:{min:1}}'
            true_name = name + '.damaged'
         case _:
            return False
      on_true = get_model_sprites(item_model['on_true'])
      on_false = get_model_sprites(item_model['on_false'])
      if on_true is not None and on_false is not None:
         # if both alternate models are simply sprites with no tinting, we can simply add lang entries for both
         # elytra does this
         if all(x['tint'] is None for x in on_true) and all(x['tint'] is None for x in on_false):
            false_name = name
            model_translations[true_name] = [x['sprite'] for x in on_true]
            model_translations[false_name] = [x['sprite'] for x in on_false]
            simple_property[name] = {'check':check, 'true': true_name, 'false': false_name}
            return True
         # pattern where both alternate models share a common base, but the other has an extra tinted layer
         # wolf armor does this
         if len(on_true) == len(on_false) + 1 and all(x['tint'] is None for x in on_false) and on_true[:len(on_false)] == on_false and on_true[-1]['tint'] is not None:
            tint = on_true[-1]['tint']
            if short(tint['type']) == 'dye' and prop == 'has_component' and short(item_model['component']) == 'dyed_color':
               model_translations[name] = [x['sprite'] for x in on_false]
               overlay_translations[name] = [on_true[-1]['sprite']]
               dyed_overlays.append(name)
               return True
      return False
   
   # some special models that render extra stuff based on certain components
   def handle_special(name: str, item_model: dict[str, typing.Any]) -> bool:
      special = short(item_model['model']['type'])
      match special:
         case 'banner' | 'shield':
            gen_name_left = name + '.item'
            rendered_item_sprites[gen_name_left] = name
            # use one lang entry for the base model
            model_translations[name] = [gen_name_left]
            for pattern, textures in banner_patterns.items():
               match special:
                  case 'banner':
                     fake_model = {
                        "parent": item_model['base'],
                        "textures": {
                           "0": textures['banner']
                        },
                        "elements": [
                           {
                              "from": [8.66667, 2.66667, 1.33333],
                              "to": [9.66667, 29.33333, 14.66667],
                              "rotation": {"angle": -90, "axis": "y", "origin": [8, 0, 8]},
                              "faces": {
                                 "north": {"uv": [5.25, 0.25, 5.5, 10.25], "texture": "#0"},
                                 "east": {"uv": [0.25, 0.25, 5.25, 10.25], "texture": "#0"},
                                 "south": {"uv": [0, 0.25, 0.25, 10.25], "texture": "#0"},
                                 "west": {"uv": [5.5, 0.25, 10.5, 10.25], "texture": "#0"},
                                 "up": {"uv": [5.25, 0, 0.25, 0.25], "rotation": 90, "texture": "#0"},
                                 "down": {"uv": [10.25, 0, 5.25, 0.25], "rotation": 270, "texture": "#0"}
                              }
                           }
                        ]
                     }
                  case 'shield':
                     fake_model = {
                        "parent": item_model['base'],
                        "textures": {
                           "0": textures['shield']
                        },
                        "elements": [
                           {
                              "from": [-6, -11, 1],
                              "to": [6, 11, 2],
                              "faces": {
                                 "south": {
                                    "uv": [0.25, 0.25, 3.25, 5.75],
                                    "texture": "#0"
                                 }
                              }
                           }
                        ]
                     }
               gen_name_left = pattern + '.' + special
               rendered_fake_sprites[gen_name_left] = fake_model
               overlay_translations[special + '.' + pattern] = [gen_name_left]
            banners[name] = special
            return True
         case 'decorated_pot':
            gen_name_left = name + '.item'
            rendered_item_sprites[gen_name_left] = name
            # use one lang entry for the base model
            model_translations[name] = [gen_name_left]
            for item, pattern in pot_patterns.items():
               fake_left = {
                  "parent": item_model['base'],
                  "textures": {
                     "0": pattern
                  },
                  "elements": [
                     {
		               	"from": [1, 0, 1],
		               	"to": [1, 16, 15],
		               	"rotation": {"angle": 0, "axis": "y", "origin": [1, 0, 1]},
		               	"faces": {
		               		"west": {"uv": [1, 0, 15, 16], "texture": "#0"}
		               	}
		               }
                  ]
               }
               fake_right = {
                  "parent": item_model['base'],
                  "textures": {
                     "0": pattern
                  },
                  "elements": [
                     {
		               	"from": [1, 0, 15],
		               	"to": [15, 16, 15],
		               	"rotation": {"angle": 0, "axis": "y", "origin": [1, 0, 1]},
		               	"faces": {
		               		"south": {"uv": [1, 0, 15, 16], "texture": "#0"}
		               	}
		               }
                  ]
               }
               gen_name_left = pattern + '.left'
               gen_name_right = pattern + '.right'
               rendered_fake_sprites[gen_name_left] = fake_left
               rendered_fake_sprites[gen_name_right] = fake_right
               overlay_translations['pot.' + item + '.left'] = [gen_name_left]
               overlay_translations['pot.' + item + '.right'] = [gen_name_right]
            pots.append(name)
            return True
         case _:
            return False
   
   for name, entry in vanilla.assets.item_models.items():
      name = canon(name)
      squashed_model = squash_conditions(entry.data['model'])
      result = get_model_sprites(squashed_model)
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
            case 'special':
               handled = handle_special(name, squashed_model)
            case _:
               handled = False
      if not handled:
         print(f'Unhandled item model {name}: {squashed_model}')

   # the renderer doesn't provide a simple model -> image API
   # instead, we feed it many models with output paths, then it saves them all to the pack at once
   # but we don't want them in the pack, we want them in a big grid
   # so we keep track of the output paths so we can load the generated images, then delete them from the pack
   for gen_name, fake_model in rendered_fake_sprites.items():
      model_file = beet.Model(fake_model)
      ctx.assets.models[gen_name] = model_file
   render = model_resolver.Render(ctx=ctx)
   render.default_render_size = 64
   for gen_name, model_name in rendered_model_sprites.items():
      render.add_model_task(
         model = model_name,
         path_ctx = gen_name,
         animation_mode = 'one_file'
      )
   for gen_name, item_model in rendered_item_sprites.items():
      render.add_item_task(
         item = model_resolver.Item(id=item_model, components={'minecraft:item_model':item_model}),
         path_ctx = gen_name,
         animation_mode = 'one_file'
      )
   for gen_name in rendered_fake_sprites.keys():
      render.add_model_task(
         model = gen_name,
         path_ctx = gen_name,
         animation_mode = 'one_file'
      )
   render.run()
   all_rendered = [*rendered_model_sprites.keys(), *rendered_item_sprites.keys(), *rendered_fake_sprites.keys()]
   generated_entries = [(ctx.assets.textures[x].image, x) for x in all_rendered]
   grid_img, grid_refs = make_grid(generated_entries, render.default_render_size)
   for gen_name in all_rendered:
      del ctx.assets.textures[gen_name]
   for gen_name in rendered_fake_sprites.keys():
      del ctx.assets.models[gen_name]
   resourcepack.textures['block_sheet'] = beet.Texture(grid_img)
   
   font = FontManager(rows=3)
   next_slot = font.get_space(15)
   empty_slot = font.get_space(18)
   overlay = font.get_space(-3)
   prev_slot = font.get_space(-18)
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

   font.add_grid('tryashtar.shulker_preview:block_sheet', grid_refs)
   for entry in atlas_sprites:
      asset = get_texture_from_atlas_entry(vanilla.assets.textures, block_atlas, entry)
      if asset is not None:
         font.add_sprite(asset['texture'])
      else:
         print(f'Texture not found in atlas {asset}')
   resourcepack.fonts['preview'] = font.build()
   
   for model, sprites in model_translations.items():
      data = [font.get_sprite(x) for x in sprites]
      for row in range(font.rows):
         lang.data[f'tryashtar.shulker_preview.item.{model}.{row}'] = overlay.join([x['rows'][row] + x['negative'] for x in data]) + next_slot

   for name, sprites in overlay_translations.items():
      data = [font.get_sprite(x) for x in sprites]
      for row in range(font.rows):
         lang.data[f'tryashtar.shulker_preview.overlay.{name}.{row}'] = prev_slot + overlay.join([x['rows'][row] + x['negative'] for x in data]) + next_slot

   # we need the item_model component in a string to run the macro
   # but there's no way to do this if the component is set to the default for that item type (which it almost always is)
   # so we need to bake into the pack a way to convert an item type to an item_model component
   # fortunately, for every vanilla item, its default item_model component is identical to its ID
   # so this is a very easy default strategy
   # here we look for any item types that don't have this property
   # any that do can be specifically checked for and the correct item_model string assigned
   unusual_default_models = {}
   for item, defaults in components.items():
      if defaults['minecraft:item_model'] != item:
         unusual_default_models[item] = defaults['minecraft:item_model']
   
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
      
      model_fn.append(f'execute {check_model([*simple_property.keys(), *case_property.keys(), *dyed_overlays])} run return run function tryashtar.shulker_preview:render/row_{row}/model/property')
      property_fn = [
         "# models that change based on a component property",
      ]
      for model, entry in simple_property.items():
         property_fn.extend([
            f'execute {check_model([model], entry['check'])} run return run data modify storage tryashtar.shulker_preview:data tooltip append value {{translate:"tryashtar.shulker_preview.item.{entry['true']}.{row}",fallback:"%s",with:[{{translate:"tryashtar.shulker_preview.missingno.{row}"}}]}}',
            f'execute {check_model([model])} run return run data modify storage tryashtar.shulker_preview:data tooltip append value {{translate:"tryashtar.shulker_preview.item.{entry['false']}.{row}",fallback:"%s",with:[{{translate:"tryashtar.shulker_preview.missingno.{row}"}}]}}',
         ])
      for model, data in case_property.items():
         for value in data['values']:
            property_fn.append(f'execute {check_model([model])} if data storage tryashtar.shulker_preview:data item.components.{data['check'](value)} run return run data modify storage tryashtar.shulker_preview:data tooltip append value {{translate:"tryashtar.shulker_preview.item.{model}.{value}.{row}",fallback:"%s",with:[{{translate:"tryashtar.shulker_preview.missingno.{row}"}}]}}')
         property_fn.append(f'execute {check_model([model])} run return run data modify storage tryashtar.shulker_preview:data tooltip append value {{translate:"tryashtar.shulker_preview.item.{model}.{row}",fallback:"%s",with:[{{translate:"tryashtar.shulker_preview.missingno.{row}"}}]}}')
      for model in dyed_overlays:
         property_fn.extend([
            f'execute {check_model([model], 'dyed_color')} store result score #color shulker_preview run data get storage tryashtar.shulker_preview:data item.components."minecraft:dyed_color"',
            f'execute {check_model([model], 'dyed_color')} run function tryashtar.shulker_preview:render/convert_color',
            f'execute {check_model([model], 'dyed_color')} run return run function tryashtar.shulker_preview:render/row_{row}/model/color_overlay.macro with storage tryashtar.shulker_preview:data item',
            f'execute {check_model([model])} run return run data modify storage tryashtar.shulker_preview:data tooltip append value {{translate:"tryashtar.shulker_preview.item.{model}.{row}",fallback:"%s",with:[{{translate:"tryashtar.shulker_preview.missingno.{row}"}}]}}',
         ])

      datapack.functions[f'render/row_{row}/model/property'] = beet.Function(property_fn)
      
      model_fn.append(f'execute {check_model(simple_tinted.keys())} run return run function tryashtar.shulker_preview:render/row_{row}/model/tinted')
      tinted_fn = [
         "# models with a hardcoded color",
      ]
      for model, tint in simple_tinted.items():
         tinted_fn.append(f'execute {check_model([model])} run return run data modify storage tryashtar.shulker_preview:data tooltip append value {{translate:"tryashtar.shulker_preview.item.{model}.{row}",color:"{color_hex(tint)}",fallback:"%s",with:[{{translate:"tryashtar.shulker_preview.missingno.{row}"}}]}}')
      datapack.functions[f'render/row_{row}/model/tinted'] = beet.Function(tinted_fn)
      
      for default_color, entries in simple_dye.items():
         fn_name = f'render/row_{row}/model/dye' if len(firework) == 1 else f'render/row_{row}/model/dye/{default_color}'
         model_fn.append(f'execute {check_model(entries)} run return run function tryashtar.shulker_preview:{fn_name}')
         color = color_hex(default_color)
         dye_fn = [
            '# models with a single dyed layer',
            f'data modify storage tryashtar.shulker_preview:data item merge value {{red:"{color[1:3]}",green:"{color[3:5]}","blue":"{color[5:7]}"}}',
            'execute store success score #has_color shulker_preview store result score #color shulker_preview run data get storage tryashtar.shulker_preview:data item.components."minecraft:dyed_color"',
            'execute if score #has_color shulker_preview matches 1 run function tryashtar.shulker_preview:render/convert_color',
            f'function tryashtar.shulker_preview:render/row_{row}/model/color.macro with storage tryashtar.shulker_preview:data item',
         ]
         datapack.functions[fn_name] = beet.Function(dye_fn)

      
      for default_color, entries in firework.items():
         fn_name = f'render/row_{row}/model/star' if len(firework) == 1 else f'render/row_{row}/model/star/{default_color}'
         model_fn.append(f'execute {check_model(entries)} run return run function tryashtar.shulker_preview:{fn_name}')
         color = color_hex(default_color)
         firework_fn = [
            '# firework stars can be any color, so a macro is needed',
            f'data modify storage tryashtar.shulker_preview:data item merge value {{red:"{color[1:3]}",green:"{color[3:5]}","blue":"{color[5:7]}"}}',
            'function tryashtar.shulker_preview:render/star_color',
            f'function tryashtar.shulker_preview:render/row_{row}/model/color_overlay.macro with storage tryashtar.shulker_preview:data item',
         ]
         datapack.functions[fn_name] = beet.Function(firework_fn)
      for default_color, entries in maps.items():
         fn_name = f'render/row_{row}/model/map' if len(maps) == 1 else f'render/row_{row}/model/map/{default_color}'
         model_fn.append(f'execute {check_model(entries)} run return run function tryashtar.shulker_preview:{fn_name}')
         color = color_hex(default_color)
         map_fn = [
            '# maps can be any color, so a macro is needed',
            f'data modify storage tryashtar.shulker_preview:data item merge value {{red:"{color[1:3]}",green:"{color[3:5]}","blue":"{color[5:7]}"}}',
            'execute store success score #has_color shulker_preview store result score #color shulker_preview run data get storage tryashtar.shulker_preview:data item.components."minecraft:map_color"',
            'execute if score #has_color shulker_preview matches 1 run function tryashtar.shulker_preview:render/convert_color',
            f'function tryashtar.shulker_preview:render/row_{row}/model/color_overlay.macro with storage tryashtar.shulker_preview:data item',
         ]
         datapack.functions[fn_name] = beet.Function(map_fn)
      
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
            f'function tryashtar.shulker_preview:render/row_{row}/model/color_base.macro with storage tryashtar.shulker_preview:data item',
         ]
         datapack.functions[fn_name] = beet.Function(potionlike_fn)
      
      model_fn.append(f'execute {check_model([model['model'] for entry in armor for model in entry['models']])} run return run function tryashtar.shulker_preview:render/row_{row}/model/armor')
      armor_fn = [
         "# armor starts with the base model",
         f'function tryashtar.shulker_preview:render/row_{row}/model/armor/base',
         '',
         "# then the trim overlay if present",
      ]
      armor_base = [
         "# render the base depending on if the model has colored layers or not",
      ]
      dye_configs: dict[int, list[str]] = {}
      for entry in armor:
         for model in entry['models']:
            dye = model['dye']
            if dye is not None:
               if dye not in dye_configs:
                  dye_configs[dye] = []
               dye_configs[dye].append(model['model'])
      for default_color, entries in dye_configs.items():
         group_name = short(entries[0]).split('_')[0]
         color = color_hex(default_color)
         armor_base.append(f'execute {check_model(entries)} run return run function tryashtar.shulker_preview:render/row_{row}/model/armor/base/{group_name}')
         group_fn = [
            "# dyeable items can be any color, so a macro is needed",
            f'data modify storage tryashtar.shulker_preview:data item merge value {{red:"{color[1:3]}",green:"{color[3:5]}","blue":"{color[5:7]}"}}',
            'execute store success score #has_color shulker_preview store result score #color shulker_preview run data get storage tryashtar.shulker_preview:data item.components."minecraft:dyed_color"',
            'execute if score #has_color shulker_preview matches 1 run function tryashtar.shulker_preview:render/convert_color',
            f'function tryashtar.shulker_preview:render/row_{row}/model/color_base.macro with storage tryashtar.shulker_preview:data item',
         ]
         datapack.functions[f'render/row_{row}/model/armor/base/{group_name}'] = beet.Function(group_fn)
      armor_base.append(f'function tryashtar.shulker_preview:render/row_{row}/model/simple.macro with storage tryashtar.shulker_preview:data item')
      for entry in armor:
         # kinda lazy way to come up with a name for the categories
         slot_name = entry['models'][0]['model'].split('_')[1]
         armor_fn.append(f'execute {check_model([model['model'] for model in entry['models']], 'trim')} run return run function tryashtar.shulker_preview:render/row_{row}/model/armor/trim/{slot_name}')
         slot_fn = [
            "# render the armor trim overlay based on the material color",
            "# it's not as accurate as the true items which use paletted permutations",
            "# items of a matching material use a darker color",
         ]
         for model in entry['models']:
            for material, asset in model['overrides'].items():
               color = f',color:"{color_hex(asset['color'])}"' if asset['color'] is not None else ''
               slot_fn.append(f'execute {check_model([model['model']], f'trim~{{material:"{short(material)}"}}')} run return run data modify storage tryashtar.shulker_preview:data tooltip append value {{translate:"tryashtar.shulker_preview.overlay.{asset['name']}.{row}"{color},fallback:"%s",with:[{{translate:"tryashtar.shulker_preview.missingno.{row}"}}]}}')
         for material, asset in entry['trims'].items():
            color = f',color:"{color_hex(asset['color'])}"' if asset['color'] is not None else ''
            slot_fn.append(f'execute if items entity @s contents *[trim~{{material:"{short(material)}"}}] run return run data modify storage tryashtar.shulker_preview:data tooltip append value {{translate:"tryashtar.shulker_preview.overlay.{asset['name']}.{row}"{color},fallback:"%s",with:[{{translate:"tryashtar.shulker_preview.missingno.{row}"}}]}}')
         datapack.functions[f'render/row_{row}/model/armor/trim/{slot_name}'] = beet.Function(slot_fn)
      datapack.functions[f'render/row_{row}/model/armor'] = beet.Function(armor_fn)
      datapack.functions[f'render/row_{row}/model/armor/base'] = beet.Function(armor_base)
      
      model_fn.append(f'execute {check_model(banners.keys())} run return run function tryashtar.shulker_preview:render/row_{row}/model/banner')
      shieldlike = [model for model, kind in banners.items() if kind == 'shield']
      banner_fn = [
         "# banners and shields start with the base model",
         f'function tryashtar.shulker_preview:render/row_{row}/model/simple.macro with storage tryashtar.shulker_preview:data item',
         '',
         "# shields have a possible base color overlay",
         f'execute {check_model(shieldlike)} run data modify storage tryashtar.shulker_preview:data item.base set from storage tryashtar.shulker_preview:data item.components."minecraft:base_color"',
         f'execute {check_model(shieldlike)} if data storage tryashtar.shulker_preview:data item.base run function tryashtar.shulker_preview:render/shield_color with storage tryashtar.shulker_preview:data item',
         f'execute {check_model(shieldlike)} if data storage tryashtar.shulker_preview:data item.base run function tryashtar.shulker_preview:render/row_{row}/model/banner/shield_base with storage tryashtar.shulker_preview:data item',
         '',
         "# then the pattern overlays",
         "# set a macro value to banner or shield accordingly, to use the matching translation",
         'execute unless data storage tryashtar.shulker_preview:data item.components."minecraft:banner_patterns"[0] run return fail',
         'data modify storage tryashtar.shulker_preview:data item.components."minecraft:banner_patterns"[].kind set value "banner"',
         f'execute {check_model(shieldlike)} run data modify storage tryashtar.shulker_preview:data item.components."minecraft:banner_patterns"[].kind set value "shield"',
         f'function tryashtar.shulker_preview:render/row_{row}/model/banner/pattern_loop',
      ]
      shield_base = [
         "# render the base of a shield with a dye-specific color",
         f'$data modify storage tryashtar.shulker_preview:data tooltip append value {{translate:"tryashtar.shulker_preview.overlay.shield.minecraft:base.{row}",color:"$(base)",fallback:"%s",with:[{{translate:"tryashtar.shulker_preview.missingno.{row}"}}]}}'
      ]
      banner_loop = [
         "# recursively render banner patterns using a macro",
         'function tryashtar.shulker_preview:render/banner_color with storage tryashtar.shulker_preview:data item.components."minecraft:banner_patterns"[0]',
         f'function tryashtar.shulker_preview:render/row_{row}/model/banner/pattern with storage tryashtar.shulker_preview:data item.components."minecraft:banner_patterns"[0]',
         'data remove storage tryashtar.shulker_preview:data item.components."minecraft:banner_patterns"[0]',
         f'execute if data storage tryashtar.shulker_preview:data item.components."minecraft:banner_patterns"[0] run function tryashtar.shulker_preview:render/row_{row}/model/banner/pattern_loop',
      ]
      banner_one = [
         "# render one banner pattern with a dye-specific color",
         f'$data modify storage tryashtar.shulker_preview:data tooltip append value {{translate:"tryashtar.shulker_preview.overlay.$(kind).$(pattern).{row}",color:"$(color)",fallback:"%s",with:[{{translate:"tryashtar.shulker_preview.missingno.{row}"}}]}}'
      ]
      datapack.functions[f'render/row_{row}/model/banner'] = beet.Function(banner_fn)
      datapack.functions[f'render/row_{row}/model/banner/shield_base'] = beet.Function(shield_base)
      datapack.functions[f'render/row_{row}/model/banner/pattern_loop'] = beet.Function(banner_loop)
      datapack.functions[f'render/row_{row}/model/banner/pattern'] = beet.Function(banner_one)
      
      model_fn.append(f'execute {check_model(pots)} run return run function tryashtar.shulker_preview:render/row_{row}/model/pot')
      pot_fn = [
         "# pots start with the base model",
         f'function tryashtar.shulker_preview:render/row_{row}/model/simple.macro with storage tryashtar.shulker_preview:data item',
         '',
         "# then the pattern overlays",
         "# only the second and fourth are visible on the left and right, respectively",
         "# each ID is an item name of either a sherd or brick",
         'execute unless data storage tryashtar.shulker_preview:data item.components."minecraft:pot_decorations"[3] run return fail',
         'data modify storage tryashtar.shulker_preview:data item.left set from storage tryashtar.shulker_preview:data item.components."minecraft:pot_decorations"[1]',
         'data modify storage tryashtar.shulker_preview:data item.right set from storage tryashtar.shulker_preview:data item.components."minecraft:pot_decorations"[3]',
         f'function tryashtar.shulker_preview:render/row_{0}/model/pot/patterns with storage tryashtar.shulker_preview:data item',
      ]
      pattern_fn = [
         "# render both patterns at once with a macro",
         f'$data modify storage tryashtar.shulker_preview:data tooltip append value [{{translate:"tryashtar.shulker_preview.overlay.pot.$(left).left.{row}",fallback:"%s",with:[{{translate:"tryashtar.shulker_preview.missingno.{row}"}}]}},{{translate:"tryashtar.shulker_preview.overlay.pot.$(right).right.{row}",fallback:"%s",with:[{{translate:"tryashtar.shulker_preview.missingno.{row}"}}]}}]'
      ]
      datapack.functions[f'render/row_{row}/model/pot'] = beet.Function(pot_fn)
      datapack.functions[f'render/row_{row}/model/pot/patterns'] = beet.Function(pattern_fn)
      
      model_fn.extend([
         '',
         f'function tryashtar.shulker_preview:render/row_{row}/model/simple.macro with storage tryashtar.shulker_preview:data item'
      ])
      simple_fn = [
         "# macro for simple models that are just one or more uncolored layers",
         f'$data modify storage tryashtar.shulker_preview:data tooltip append value {{translate:"tryashtar.shulker_preview.item.$(model).{row}",fallback:"%s",with:[{{translate:"tryashtar.shulker_preview.missingno.{row}"}}]}}'
      ]
      color_fn = [
         "# macro for models that are just one colored layer",
         f'$data modify storage tryashtar.shulker_preview:data tooltip append value {{translate:"tryashtar.shulker_preview.item.$(model).{row}",color:"#$(red)$(green)$(blue)",fallback:"%s",with:[{{translate:"tryashtar.shulker_preview.missingno.{row}"}}]}}'
      ]
      color_base = [
         '# macro for models that render with a colored base and one or more uncolored overlays',
         f'$data modify storage tryashtar.shulker_preview:data tooltip append value [{{translate:"tryashtar.shulker_preview.item.$(model).{row}",color:"#$(red)$(green)$(blue)",fallback:"%s",with:[{{translate:"tryashtar.shulker_preview.missingno.{row}"}}]}},{{translate:"tryashtar.shulker_preview.overlay.$(model).{row}",color:"white",fallback:"%s",with:[{{translate:"tryashtar.shulker_preview.missingno.{row}"}}]}}]',
      ]
      color_overlay = [
         '# macro for models that render with an uncolored base and a colored overlay',
         f'$data modify storage tryashtar.shulker_preview:data tooltip append value [{{translate:"tryashtar.shulker_preview.item.$(model).{row}",fallback:"%s",with:[{{translate:"tryashtar.shulker_preview.missingno.{row}"}}]}},{{translate:"tryashtar.shulker_preview.overlay.$(model).{row}",color:"#$(red)$(green)$(blue)",fallback:"%s",with:[{{translate:"tryashtar.shulker_preview.missingno.{row}"}}]}}]',
      ]

      datapack.functions[f'render/row_{row}/model/simple.macro'] = beet.Function(simple_fn)
      datapack.functions[f'render/row_{row}/model/color.macro'] = beet.Function(color_fn)
      datapack.functions[f'render/row_{row}/model/color_base.macro'] = beet.Function(color_base)
      datapack.functions[f'render/row_{row}/model/color_overlay.macro'] = beet.Function(color_overlay)
      
      datapack.functions[f'render/row_{row}/item'] = beet.Function(item_fn)
      datapack.functions[f'render/row_{row}/model'] = beet.Function(model_fn)

# all textures referenced by item models are entries in the blocks atlas
# that means they may have different names from the textures they came from
# (in practice, this only applies to trim textures)
# regardless, in order to get the texture the entry came from (so the font can reference it),
# we need to find the atlas source that imported it
TextureColor = typing.TypedDict('TextureColor', {'texture': str, 'color': int | None})
def get_texture_from_atlas_entry(textures: beet.NamespaceProxy[beet.Texture], atlas: beet.Atlas, entry: str) -> TextureColor | None:
   entry = canon(entry)
   _namespace, path = entry.split(':')
   for source in atlas.data['sources']:
      match short(source['type']):
         case 'single':
            resource = canon(source['resource'])
            if entry == resource:
               return {'texture': entry, 'color': None}
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

def dict_diff(d1: dict, d2: dict) -> dict:
   result = {}
   for key, value in d1.items():
      if key not in d2 or d2[key] != value:
         result[key] = value
   return result

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
            # (vanilla doesn't use this anyway)
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
            # (vanilla doesn't use this anyway)
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
         self.sprites[texture + '.png'] = data
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
      self.grids[grid + '.png'] = data
     
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
