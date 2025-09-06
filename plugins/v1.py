import collections
import copy
import dataclasses
import itertools
import json
import typing
import PIL.Image
import beet
import beet.contrib.vanilla
import model_resolver.render
from plugins.version import VersionRange
from plugins.util import Grid, map_2d, short, canon, model_data, colorize, rgba, LayeredModel, ElementModel, EntityModel, make_grid, invert_dict, FontManager, add_numbers, add_tooltip, get_space, JsonDict, NbtCompound
from plugins.info import dye_colors, get_fake_model, get_registry, item_durability, legacy_banner_patterns, spawn_egg_colors, potion_colors, item_colors

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
   info = ItemSpriteInfo(colormap=colormap)
   for name in items:
      info.import_item(name, vanilla.assets)
   banner_model = info.render_models[('minecraft:white_banner', 'item')]
   assert isinstance(banner_model, dict)
   with open('resources/fake_models/banner_pattern.json', 'r', encoding='utf-8') as file:
      pattern_model: JsonDict = json.load(file)
      pattern_model['display'] = banner_model['display']
   patterns = legacy_banner_patterns(data_version)
   banner_vanilla = registry['1.16']
   for pattern in patterns.values():
      for color, rgb in dye_colors().items():
         model = copy.deepcopy(pattern_model)
         image = banner_vanilla.assets.textures[f'minecraft:entity/banner/{pattern}'].image.convert('RGBA')
         assert isinstance(image, PIL.Image.Image)
         image = colorize(image, rgba(rgb))
         model['textures']['0'] = image
         info.render_models[(f'banner.{pattern}.{color}', 'overlay')] = model
   arrow_overlay = vanilla.assets.textures['minecraft:item/tipped_arrow_head'].image.convert('RGBA')
   potion_overlay = vanilla.assets.textures['minecraft:item/potion_overlay'].image.convert('RGBA')
   potions = invert_dict(potion_colors(data_version))
   for color, potions in potions.items():
      if color is not None:
         potion_name = short(potions[0])
         info.flat_items[(f'arrow.{potion_name}', 'overlay')] = colorize(arrow_overlay, rgba(color))
         info.flat_items[(f'potion.{potion_name}', 'overlay')] = colorize(potion_overlay, rgba(color))
   grids = info.render(ctx, vanilla)
   resourcepack.textures['item_sheet'] = beet.Texture(grids.items.image)
   resourcepack.textures['block_sheet'] = beet.Texture(grids.blocks.image)
   
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
   font.add_grid('tryashtar.shulker_preview:item_sheet', map_2d(grids.items.entries, lambda x: None if x is None else x[0]))
   font.add_grid('tryashtar.shulker_preview:block_sheet', map_2d(grids.blocks.entries, lambda x: None if x is None else x[0]))
   for (name, kind) in itertools.chain(info.flat_items.keys(), info.render_models.keys()):
      sprite = font.get_sprite(name)
      for row in range(font.rows):
         text = get_space(font, comma_forward + (-18 if kind == 'overlay' else 0)) + sprite.rows[row] + sprite.negative + get_space(font, 15 + comma_back)
         lang.data[f'tryashtar.shulker_preview.{kind}.{name}.{row}'] = text
   font_result = font.build()
   font_result.data['providers'][0] = {'comment':'Many thanks to AmberW for this invaluable concept'} | font_result.data['providers'][0]
   ctx.assets.fonts['minecraft:default'] = font_result

   length_dict: dict[int, list[str]] = collections.defaultdict(list)
   for name in items:
      name = canon(name)
      length = len(name)
      length_dict[length].append(name)
   ctx.meta['shulker_preview']['length_dict'] = length_dict
   ctx.meta['shulker_preview']['item_overrides'] = info.item_overrides
   ctx.meta['shulker_preview']['durability_dict'] = item_durability(registry['1.21.4'], data_version)
   ctx.meta['shulker_preview']['patterns'] = patterns

SpriteKind = typing.Literal['item', 'override', 'overlay']

Sprite = tuple[str, SpriteKind]

@dataclasses.dataclass
class ModelOverride:
   sprite: str
   predicate: JsonDict
   kind: typing.Literal['item', 'override']
   
@dataclasses.dataclass
class Grids:
   items: Grid[Sprite]
   blocks: Grid[Sprite]

class ItemSpriteInfo:
   def __init__(self, colormap: dict[str, list[int | None]]):
      self.colormap = colormap
      self.flat_items: dict[Sprite, PIL.Image.Image] = {}
      self.render_models: dict[Sprite, str | JsonDict] = {}
      self.item_overrides: dict[str, list[ModelOverride]] = {}
   
   def import_item(self, item: str, pack: beet.ResourcePack):
      item = canon(item)
      nspace, path = item.split(':')
      model_name = f'{nspace}:item/{path}'
      data = self.handle_model(item, item, model_name, 'item', pack)
      overrides = trim_overrides(data.overrides)
      self.item_overrides[item] = []
      final_override = {}
      for override in overrides:
         sprite_name = item + '.' + '.'.join(override['predicate'].keys())
         self.handle_model(item, sprite_name, override['model'], 'override', pack)
         self.item_overrides[item].append(ModelOverride(sprite=sprite_name, predicate=override['predicate'], kind='override'))
         for key,value in override['predicate'].items():
            final_override[key] = not value
      self.item_overrides[item].append(ModelOverride(sprite=item, predicate=final_override, kind='item'))
   
   def handle_model(self, item: str, name: str, model_name: str, kind: SpriteKind, pack: beet.ResourcePack):
      model = pack.models[canon(model_name)]
      data = model_data(pack.models, model)
      if isinstance(data, LayeredModel):
         image_layers = [pack.textures[x].image.convert('RGBA') for x in data.layers]
         tint_layers = self.colormap.get(short(item))
         image = PIL.Image.new('RGBA', image_layers[0].size)
         for i, layer in enumerate(image_layers):
            if tint_layers is not None and i < len(tint_layers) and (tint := tint_layers[i]) is not None:
               layer = colorize(layer, rgba(tint))
            image.paste(layer, (0, 0), layer)
         self.flat_items[(name, kind)] = image
      elif isinstance(data, ElementModel):
         self.render_models[(name, kind)] = model_name
      elif isinstance(data, EntityModel):
         fake_model = get_fake_model(item)
         if fake_model is None:
            raise ValueError(item)
         fake_model['display'] = data.display
         self.render_models[(name, kind)] = fake_model
      else:
         raise ValueError(model_name)
      return data
   
   def render(self, ctx: beet.Context, pack: beet.contrib.vanilla.Release) -> Grids:
      renderer = model_resolver.render.Render(ctx)
      renderer.getter._vanilla = pack
      renderer.default_render_size = 64
      for model in self.render_models.values():
         if isinstance(model, str):
            renderer.add_model_task(
               model=model,
               animation_mode='one_file',
            )
         else:
            renderer.add_model_dict_task(
               model=model,
               animation_mode='one_file',
            )
      renderer.run()
      block_items: dict[Sprite, PIL.Image.Image] = {}
      for sprite, task in zip(self.render_models.keys(), renderer.tasks):
         assert task.saved_img is not None
         block_items[sprite] = task.saved_img
      block_grid = make_grid(block_items, 64)
      item_grid = make_grid(self.flat_items, 16)
      return Grids(items=item_grid, blocks=block_grid)

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
