import collections
import PIL.Image
import beet
import beet.contrib.vanilla
import model_resolver
from plugins.version import VersionRange
from plugins.util import short, canon, model_data, colorize, rgba, LayeredModel, ElementModel, EntityModel, make_grid, invert_dict, FontManager, add_numbers, add_tooltip, get_space
from plugins.info import get_fake_model, get_registry, item_durability, spawn_egg_colors, potion_colors, item_colors

def main(ctx: beet.Context, registry: beet.contrib.vanilla.ReleaseRegistry, target: VersionRange):
   datapack = ctx.data['tryashtar.shulker_preview']
   resourcepack = ctx.assets['tryashtar.shulker_preview']
   
   target_version = target.last.version
   data_version = target.last.data
   vanilla = registry[target_version]
   
   items = [short(x) for x in get_registry(vanilla, 'minecraft:item').keys()]
   items.remove('air')
   eggs = spawn_egg_colors(registry['1.21.4'].assets, data_version)
   colored = item_colors(registry['1.21.4'].assets, data_version)
   colormap: dict[str, list[int | None]] = dict([
      *[(short(name), [value.base, value.overlay]) for name, value in eggs.items()],
      *[(short(name), [color]) for name, color in colored.items()],
      *[(short(name), [0xa06540]) for name in ['leather_helmet', 'leather_chestplate', 'leather_leggings', 'leather_boots', 'leather_horse_armor']],
   ])
   flat_items: dict[str, PIL.Image.Image] = {}
   overlays: dict[str, PIL.Image.Image] = {}
   render_models: dict[str, str] = {}
   for item in items:
      model_name = f'minecraft:item/{item}'
      model = vanilla.assets.models[model_name]
      data = model_data(vanilla.assets.models, model)
      overrides = trim_overrides(data.overrides)
      if len(overrides) > 0:
         print(item, overrides)
      if isinstance(data, LayeredModel):
         image_layers = [vanilla.assets.textures[x].image.convert('RGBA') for x in data.layers]
         image = PIL.Image.new('RGBA', image_layers[0].size)
         for i, layer in enumerate(image_layers):
            if (tints := colormap.get(short(item))) is not None:
               if i < len(tints) and (tint := tints[i]) is not None:
                  layer = colorize(layer, rgba(tint))
            image.paste(layer, (0, 0), layer)
         flat_items[item] = image
      elif isinstance(data, ElementModel):
         render_models[item] = model_name
      elif isinstance(data, EntityModel):
         fake_model = get_fake_model(item)
         if fake_model is None:
            print(f'Unhandled item: {item}')
         else:
            fake_model['display'] = data.display
            ctx.assets.models[f'render:{item}'] = beet.Model(fake_model)
            render_models[item] = f'render:{item}'
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
   
   lang = resourcepack.languages['en_us']
   font = FontManager(rows=3)
   font.legacy_space_texture = 'tryashtar.shulker_preview:space'
   font.upcoming_char = ord('\uf800')
   widths = [32768, 1, 2, 3, 4, 5, 6, 7, 8, 16, 32, 64, 128, 256, 512, 1024]
   for width in widths:
      font.get_space(-width)
   font.upcoming_char = ord('\uf820')
   for width in widths:
      font.get_space(width)
   font.upcoming_char = ord('\ue000')
   font.add_provider({
      'type': 'bitmap',
      'file': 'tryashtar.shulker_preview:comma.png',
      'ascent': 7,
      'chars': [','],
   })
   lang.data['tryashtar.shulker_preview.empty_slot'] = get_space(font, 18)
   lang.data['tryashtar.shulker_preview.row_end'] = get_space(font, -162)
   for texture, tooltip, bottom in [('shulker_box', 'shulker_tooltip', 20), ('generic_54', 'ender_tooltip', 27)]:
      text = add_tooltip(font, f'minecraft:gui/container/{texture}', bottom)
      lang.data[f'tryashtar.shulker_preview.{tooltip}'] = get_space(font, -4) + text + get_space(font, 8)
   missing = font.add_sprite('tryashtar.shulker_preview:missingno')
   for row in range(font.rows):
      lang.data[f'tryashtar.shulker_preview.missingno.{row}'] = missing.rows[row] + missing.negative + get_space(font, 15)
   numbers = add_numbers(font)
   for row in range(font.rows):
      for num in range(1, 10):
         lang.data[f'tryashtar.shulker_preview.number.{num}.{row}'] = get_space(font, -4) + numbers[num].negative + numbers[num].normal[row] + get_space(font, 1)
         lang.data[f'tryashtar.shulker_preview.number_shadow.{num}.{row}'] = get_space(font, -3) + numbers[num].negative + numbers[num].shadow[row]
      for num in range(10, 100):
         d1 = num // 10
         d2 = num % 10
         lang.data[f'tryashtar.shulker_preview.number.{num}.{row}'] = get_space(font, -7) + numbers[d1].negative + numbers[d2].negative + numbers[d1].normal[row] + numbers[d2].normal[row] + get_space(font, 1)
         lang.data[f'tryashtar.shulker_preview.number_shadow.{num}.{row}'] = get_space(font, -6) + numbers[d1].negative + numbers[d2].negative + numbers[d1].shadow[row] + numbers[d2].shadow[row]
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
         lang.data[f"tryashtar.shulker_preview.durability.{num}.{row}"] = get_space(font, -16) + durability[num] + get_space(font, 2)
   font.add_grid('tryashtar.shulker_preview:item_sheet', item_grid)
   font.add_grid('tryashtar.shulker_preview:block_sheet', block_grid)
   for item in flat_items.keys():
      sprite = font.get_sprite(item)
      for row in range(font.rows):
         text = sprite.rows[row] + sprite.negative + get_space(font, 15)
         lang.data[f'tryashtar.shulker_preview.item.{canon(item)}.{row}'] = text
   for item in block_items.keys():
      sprite = font.get_sprite(item)
      for row in range(font.rows):
         text = sprite.rows[row] + sprite.negative + get_space(font, 15)
         lang.data[f'tryashtar.shulker_preview.item.{canon(item)}.{row}'] = text
   for overlay in overlays.keys():
      sprite = font.get_sprite(overlay)
      for row in range(font.rows):
         text = sprite.rows[row] + sprite.negative + get_space(font, 15)
         lang.data[f'tryashtar.shulker_preview.overlay.{overlay}.{row}'] = text
   font_result = font.build()
   font_result.data['providers'][0] = {'comment':'Many thanks to AmberW for this invaluable concept'} | font_result.data['providers'][0]
   ctx.assets.fonts['minecraft:default'] = font_result

   length_dict: dict[int, list[str]] = collections.defaultdict(list)
   for item in items:
      name = canon(item)
      length = len(name)
      length_dict[length].append(name)
   durability_dict = item_durability(registry['1.21.4'], data_version)
   for row in range(font.rows):
      process_item = [
         "# get the length of this item and call the appropriate function",
         'execute store result score #length shulker_preview run data get block ~1 1 ~ RecordItem.id',
      ]
      for length in sorted(length_dict.keys()):
         process_item.append(f'execute if score #length shulker_preview matches {length} run function tryashtar.shulker_preview:render/row_{row}/item/length_{length}')
         lines = process_item_lines(length_dict[length], row, durability_dict)
         datapack.functions[f'render/row_{row}/item/length_{length}'] = beet.Function(lines)
      datapack.functions[f'render/row_{row}/item'] = beet.Function(process_item)

def trim_overrides(overrides: list) -> list:
   result = []
   for override in overrides:
      pred = override['predicate']
      for impossible in ['pulling', 'pull', 'angle', 'cast', 'time', 'blocking']:
         if impossible in pred:
            break
      else:
         result.append(override)
   return result

def process_item_lines(items: list[str], row: int, durability_info: dict[str, int]) -> list[str]:
   lines: list[str] = []
   has_potion = False
   has_arrow = False
   has_durability = False
   for item in items:
      if_item = f'if block ~1 1 ~ jukebox{{RecordItem:{{id:"{canon(item)}"}}}}'
      if short(item) == 'elytra':
         damage = durability_info['minecraft:elytra']
         lines.extend([
            f'execute if block ~1 1 ~ jukebox{{RecordItem:{{id:"minecraft:elytra",tag:{{Damage:{damage - 1}}}}}}} run summon area_effect_cloud ~ ~ ~ {{Tags:["tryashtar.shulker_preview"],CustomName:\'{{"translate":"tryashtar.shulker_preview.item.broken_elytra.{row}"}}\'}}',
            f'execute {if_item} unless block ~1 1 ~ jukebox{{RecordItem:{{id:"minecraft:elytra",tag:{{Damage:431}}}}}} run summon area_effect_cloud ~ ~ ~ {{Tags:["tryashtar.shulker_preview"],CustomName:\'{{"translate":"tryashtar.shulker_preview.item.elytra.{row}"}}\'}}',
         ])
      elif short(item) == "crossbow":
         lines.extend([
            f'execute if block ~1 1 ~ jukebox{{RecordItem:{{id:"minecraft:crossbow",tag:{{ChargedProjectiles:[{{id:"minecraft:arrow"}}]}}}}}} run summon area_effect_cloud ~ ~ ~ {{Tags:["tryashtar.shulker_preview"],CustomName:\'{{"translate":"tryashtar.shulker_preview.item.crossbow_arrow.{row}"}}\'}}',
            f'execute if block ~1 1 ~ jukebox{{RecordItem:{{id:"minecraft:crossbow",tag:{{ChargedProjectiles:[{{id:"minecraft:firework_rocket"}}]}}}}}} run summon area_effect_cloud ~ ~ ~ {{Tags:["tryashtar.shulker_preview"],CustomName:\'{{"translate":"tryashtar.shulker_preview.item.crossbow_firework.{row}"}}\'}}',
            f'execute {if_item} unless block ~1 1 ~ jukebox{{RecordItem:{{id:"minecraft:crossbow",tag:{{ChargedProjectiles:[{{}}]}}}}}} run summon area_effect_cloud ~ ~ ~ {{Tags:["tryashtar.shulker_preview"],CustomName:\'{{"translate":"tryashtar.shulker_preview.item.crossbow.{row}"}}\'}}',
         ])
      else:
         lines.append(f'execute {if_item} run summon area_effect_cloud ~ ~ ~ {{Tags:["tryashtar.shulker_preview"],CustomName:\'{{"translate":"tryashtar.shulker_preview.item.{canon(item)}.{row}"}}\'}}')
      if item in ('potion', 'splash_potion', 'lingering_potion'):
         has_potion = True
      if item == 'tipped_arrow':
         has_arrow = True
      if (durability := durability_info.get(item)) is not None:
         lines.append(f'execute {if_item} run scoreboard players set #max shulker_preview {durability}')
         has_durability = True
   if has_potion:
      lines.append(f'execute if data block ~1 1 ~ RecordItem.tag.Potion run function tryashtar.shulker_preview:render/row_{row}/overlay/potion')
   if has_arrow:
      lines.append(f'execute if data block ~1 1 ~ RecordItem.tag.Potion run function tryashtar.shulker_preview:render/row_{row}/overlay/arrow')
   if has_durability:
      lines.extend([
         'execute store result score #durability shulker_preview run data get block ~1 1 ~ RecordItem.tag.Damage',
         f'execute if data block ~1 1 ~ RecordItem.tag.Damage run function tryashtar.shulker_preview:render/row_{row}/overlay/durability',
      ])
   return lines
