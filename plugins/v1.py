import collections
import dataclasses
import PIL.Image
import beet
import beet.contrib.vanilla
import model_resolver
from plugins.version import VersionRange
from plugins.util import short, canon, model_data, colorize, rgba, LayeredModel, ElementModel, EntityModel, make_grid, invert_dict, FontManager, add_numbers, add_tooltip, get_space, JsonDict, NbtCompound
from plugins.info import get_fake_model, get_registry, item_durability, spawn_egg_colors, potion_colors, item_colors

def main(ctx: beet.Context, registry: beet.contrib.vanilla.ReleaseRegistry, target: VersionRange):
   datapack = ctx.data['tryashtar.shulker_preview']
   resourcepack = ctx.assets['tryashtar.shulker_preview']
   
   target_version = target.last.name
   data_version = target.last.world
   vanilla = registry[target_version]
   
   items = [canon(x) for x in get_registry(vanilla, 'minecraft:item').keys()]
   items.remove('minecraft:air')
   eggs = spawn_egg_colors(registry['1.21.4'].assets, data_version)
   colored = item_colors(registry['1.21.4'].assets, data_version)
   colormap: dict[str, list[int | None]] = dict([
      *[(short(name), [value.base, value.overlay]) for name, value in eggs.items()],
      *[(short(name), [color]) for name, color in colored.items()],
      *[(short(name), [0xa06540]) for name in ['leather_helmet', 'leather_chestplate', 'leather_leggings', 'leather_boots', 'leather_horse_armor']],
   ])
   flat_items: dict[str, PIL.Image.Image] = {}
   render_models: dict[str, str] = {}
   def handle_model(name: str, model_name: str):
      model = vanilla.assets.models[canon(model_name)]
      data = model_data(vanilla.assets.models, model)
      if isinstance(data, LayeredModel):
         image_layers = [vanilla.assets.textures[x].image.convert('RGBA') for x in data.layers]
         tint_layers = colormap.get(short(name))
         image = PIL.Image.new('RGBA', image_layers[0].size)
         for i, layer in enumerate(image_layers):
            if tint_layers is not None and i < len(tint_layers) and (tint := tint_layers[i]) is not None:
               layer = colorize(layer, rgba(tint))
            image.paste(layer, (0, 0), layer)
         flat_items[name] = image
      elif isinstance(data, ElementModel):
         render_models[name] = model_name
      elif isinstance(data, EntityModel):
         fake_model = get_fake_model(name)
         if fake_model is None:
            print(f'Unhandled item: {name}')
         else:
            fake_model['display'] = data.display
            ctx.assets.models[f'render:{name}'] = beet.Model(fake_model)
            render_models[name] = f'render:{name}'
      return data
   item_overrides: dict[str, list[ModelOverride]] = {}
   for item in items:
      nspace, path = canon(item).split(':')
      model_name = f'{nspace}:item/{path}'
      data = handle_model(item, model_name)
      overrides = trim_overrides(data.overrides)
      item_overrides[item] = []
      final_override = {}
      for override in overrides:
         sprite_name = item + '.' + '.'.join(override['predicate'].keys())
         handle_model(sprite_name, override['model'])
         item_overrides[item].append(ModelOverride(sprite=sprite_name, predicate=override['predicate']))
         for key,value in override['predicate'].items():
            final_override[key] = not value
      item_overrides[item].append(ModelOverride(sprite=item, predicate=final_override))
   renderer = model_resolver.Render(ctx, vanilla)
   renderer.default_render_size = 64
   for item, model in render_models.items():
      renderer.add_model_task(
         model=model,
         path_ctx=f'render:{item}',
         animation_mode='one_file',
      )
   renderer.run()
   block_items = {item: ctx.assets.textures[f'render:{item}'].image.convert('RGBA') for item, model in render_models.items()}
   overlays: dict[str, PIL.Image.Image] = {}
   arrow_overlay = vanilla.assets.textures['minecraft:item/tipped_arrow_head'].image.convert('RGBA')
   potion_overlay = vanilla.assets.textures['minecraft:item/potion_overlay'].image.convert('RGBA')
   potions = invert_dict(potion_colors(data_version))
   for color, potions in potions.items():
      if color is not None:
         potion_name = short(potions[0])
         overlays[f'arrow.{potion_name}'] = colorize(arrow_overlay, rgba(color))
         overlays[f'potion.{potion_name}'] = colorize(potion_overlay, rgba(color))
   item_image, item_grid = make_grid(flat_items | overlays, 16)
   block_image, block_grid = make_grid(block_items, 64)
   resourcepack.textures['item_sheet'] = beet.Texture(item_image)
   resourcepack.textures['block_sheet'] = beet.Texture(block_image)
   
   lang = beet.Language()
   lang.data['%1$s%418634357$s'] = '%2$s'
   resourcepack.languages['en_us'] = lang
   font = FontManager(rows=3)
   amber_spaces(font)
   font.upcoming_char = ord('\ue000')
   resourcepack.textures['comma'] = beet.Texture(source_path='resources/shared/comma.png')
   resourcepack.textures['durability'] = beet.Texture(source_path='resources/shared/durability_color.png')
   resourcepack.textures['missingno'] = beet.Texture(source_path='resources/shared/missingno.png')
   resourcepack.textures['space'] = beet.Texture(source_path='resources/shared/space.png')
   font.add_provider({
      'type': 'bitmap',
      'file': 'tryashtar.shulker_preview:comma.png',
      'ascent': 7,
      'chars': [','],
   })
   comma_forward = 32767
   comma_back = -32773
   lang.data['tryashtar.shulker_preview.empty_slot'] = get_space(font, 18 + comma_forward + comma_back)
   lang.data['tryashtar.shulker_preview.row_end'] = get_space(font, -162 + comma_forward + comma_back)
   lang.data['tryashtar.shulker_preview.start'] = get_space(font, comma_back)
   for texture, tooltip, bottom in [('shulker_box', 'shulker_tooltip', 20), ('generic_54', 'ender_tooltip', 27)]:
      text = add_tooltip(font, f'minecraft:gui/container/{texture}', bottom)
      lang.data[f'tryashtar.shulker_preview.{tooltip}'] = get_space(font, -4 + comma_forward) + text + get_space(font, 8 + comma_back)
   missing = font.add_sprite('tryashtar.shulker_preview:missingno')
   for row in range(font.rows):
      lang.data[f'tryashtar.shulker_preview.missingno.{row}'] = get_space(font, comma_forward) + missing.rows[row] + missing.negative + get_space(font, 15 + comma_back)
   numbers = add_numbers(font)
   for row in range(font.rows):
      for num in range(1, 10):
         lang.data[f'tryashtar.shulker_preview.number.{num}.{row}'] = get_space(font, -4 + comma_forward) + numbers[num].negative + numbers[num].normal[row] + get_space(font, 1 + comma_back)
         lang.data[f'tryashtar.shulker_preview.number_shadow.{num}.{row}'] = get_space(font, -3 + comma_forward) + numbers[num].negative + numbers[num].shadow[row] + get_space(font, comma_back)
      for num in range(10, 100):
         d1, d2 = divmod(num, 10)
         lang.data[f'tryashtar.shulker_preview.number.{num}.{row}'] = get_space(font, -7 + comma_forward) + numbers[d1].negative + numbers[d2].negative + numbers[d1].normal[row] + numbers[d2].normal[row] + get_space(font, 1 + comma_back)
         lang.data[f'tryashtar.shulker_preview.number_shadow.{num}.{row}'] = get_space(font, -6 + comma_forward) + numbers[d1].negative + numbers[d2].negative + numbers[d1].shadow[row] + numbers[d2].shadow[row] + get_space(font, comma_back)
   for row in range(font.rows):
      durability = ''.join([font.next_char() for _ in range(14)])
      font.add_provider({
         'type': 'bitmap',
         'file': 'tryashtar.shulker_preview:durability.png',
         'ascent': -18 * row - 15,
         'height': 2,
         'chars': [
            durability[0:5],
            durability[5:10],
            durability[10:14] + '\u0000'
         ]})
      for num in range(14):
         lang.data[f"tryashtar.shulker_preview.durability.{num}.{row}"] = get_space(font, -16 + comma_forward) + durability[num] + get_space(font, 2 + comma_back)
   font.add_grid('tryashtar.shulker_preview:item_sheet', item_grid)
   font.add_grid('tryashtar.shulker_preview:block_sheet', block_grid)
   for item in flat_items.keys():
      sprite = font.get_sprite(item)
      for row in range(font.rows):
         text = get_space(font, comma_forward) + sprite.rows[row] + sprite.negative + get_space(font, 15) + get_space(font, comma_back)
         lang.data[f'tryashtar.shulker_preview.item.{canon(item)}.{row}'] = text
   for item in block_items.keys():
      sprite = font.get_sprite(item)
      for row in range(font.rows):
         text = get_space(font, comma_forward) + sprite.rows[row] + sprite.negative + get_space(font, 15) + get_space(font, comma_back)
         lang.data[f'tryashtar.shulker_preview.item.{canon(item)}.{row}'] = text
   for overlay in overlays.keys():
      sprite = font.get_sprite(overlay)
      for row in range(font.rows):
         text = get_space(font, comma_forward) + sprite.rows[row] + sprite.negative + get_space(font, 15) + get_space(font, comma_back)
         lang.data[f'tryashtar.shulker_preview.overlay.{overlay}.{row}'] = text
   font_result = font.build()
   font_result.data['providers'][0] = {'comment':'Many thanks to AmberW for this invaluable concept'} | font_result.data['providers'][0]
   ctx.assets.fonts['minecraft:default'] = font_result

   length_dict: dict[int, list[str]] = collections.defaultdict(list)
   for item in items:
      name = canon(item)
      length = len(name)
      length_dict[length].append(name)
   ctx.meta['shulker_preview']['length_dict'] = length_dict
   ctx.meta['shulker_preview']['item_overrides'] = item_overrides
   ctx.meta['shulker_preview']['durability_dict'] = item_durability(registry['1.21.4'], data_version)

@dataclasses.dataclass
class ModelOverride:
   sprite: str
   predicate: JsonDict

def override_check(item: str, predicate: JsonDict, durability: int | None) -> tuple[NbtCompound, NbtCompound | None]:
   item = canon(item)
   if len(predicate) == 0:
      return ({'id':item}, None)
   positive = {'id':item,'tag':{}}
   negative = {'tag':{}}
   for key, value in predicate.items():
      match key:
         case 'broken':
            if durability is not None:
               if value:
                  positive['tag']['Damage'] = durability - 1
               else:
                  negative['tag']['Damage'] = durability - 1
         case 'charged':
            firework = predicate.get('firework', 0)
            if firework:
               positive['tag']['ChargedProjectiles'] = [{'id':"minecraft:firework_rocket"}]
            elif value:
               positive['tag']['ChargedProjectiles'] = [{'id':"minecraft:arrow"}]
            else:
               negative['tag']['ChargedProjectiles'] = [{}]      
         case 'firework':
            pass
         case _:
            raise ValueError(key)
   if len(positive['tag']) == 0:
      del positive['tag']
   if len(negative['tag']) == 0:
      del negative['tag']
   if len(negative) == 0:
      negative = None
   return (positive, negative)

def amber_spaces(font: FontManager):
   font.legacy_space_texture = 'tryashtar.shulker_preview:space'
   font.upcoming_char = ord('\uf800')
   widths = [32768, 1, 2, 3, 4, 5, 6, 7, 8, 16, 32, 64, 128, 256, 512, 1024]
   for width in widths:
      font.get_space(-width)
   font.upcoming_char = ord('\uf820')
   for width in widths:
      font.get_space(width)

def trim_overrides(overrides: list[JsonDict]) -> list[JsonDict]:
   result = []
   for override in overrides:
      pred = override['predicate']
      if not any(x in pred for x in ['pulling', 'pull', 'angle', 'cast', 'time', 'blocking']):
         result.append(override)
   return result
