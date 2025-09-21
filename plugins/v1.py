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
from plugins.util import map_2d, short, canon, model_data, LayeredModel, ElementModel, EntityModel, make_grid, FontManager, add_numbers, add_tooltip, get_space, JsonDict, NbtCompound, Identifier, ResourceLocation
from plugins.info import get_fake_model, get_registry, item_durability, legacy_banner_patterns, spawn_egg_colors, item_colors

def main(ctx: beet.Context, registry: beet.contrib.vanilla.ReleaseRegistry, target: VersionRange):
   datapack = ctx.data['tryashtar.shulker_preview']
   resourcepack = ctx.assets['tryashtar.shulker_preview']
   
   target_version = target.last.name
   data_version = target.last.world
   vanilla = registry[target_version]
      
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
            durability[10:14] + '\u0000',
         ]
      })
      for num in range(14):
         lang.data[f"tryashtar.shulker_preview.durability.{num}.{row}"] = get_space(font, -16 + comma_forward) + durability[num] + get_space(font, 2 + comma_back)
   
   items = [canon(x) for x in get_registry(vanilla, 'minecraft:item').keys()]
   items.remove('minecraft:air')
   eggs = spawn_egg_colors(registry['1.21.4'].assets, data_version)
   colored = item_colors(registry['1.21.4'].assets, data_version)
   colormap: dict[Identifier, list[Tint]] = dict([
      *[(short(name), [value.base, value.overlay]) for name, value in eggs.items()],
      *[(short(name), [color]) for name, color in colored.items()],
      *[(short(name), ['dye', None]) for name in ['leather_helmet', 'leather_chestplate', 'leather_leggings', 'leather_boots', 'leather_horse_armor']],
      *[(short(name), ['potion', None]) for name in ['tipped_arrow', 'potion', 'splash_potion', 'lingering_potion']],
      ('filled_map', [None, 'map']),
      ('firework_star', [None, 'firework']),
   ])
   info = ItemSpriteInfo(colormap=colormap)
   for name in items:
      info.import_item(name, vanilla.assets)
   patterns = legacy_banner_patterns(data_version)
   if ctx.meta['shulker_preview']['banners']:
      banner_model = info.render_models[('minecraft:white_banner', 'item')]
      shield_model = info.render_models[('minecraft:shield', 'item')]
      assert isinstance(banner_model, dict)
      assert isinstance(shield_model, dict)
      with open('resources/fake_models/banner_pattern.json', 'r', encoding='utf-8') as file:
         banner_pattern_model: JsonDict = json.load(file)
         banner_pattern_model['display'] = banner_model['display']
      with open('resources/fake_models/shield_pattern.json', 'r', encoding='utf-8') as file:
         shield_pattern_model: JsonDict = json.load(file)
         shield_pattern_model['display'] = shield_model['display']
      banner_vanilla = registry['1.16']
      for pattern in patterns.values():
         banner_model = copy.deepcopy(banner_pattern_model)
         image = banner_vanilla.assets.textures[f'minecraft:entity/banner/{pattern}'].image
         assert isinstance(image, PIL.Image.Image)
         banner_model['textures']['0'] = image
         info.render_models[(f'banner.{pattern}', 'overlay')] = banner_model
         shield_model = copy.deepcopy(shield_pattern_model)
         image = banner_vanilla.assets.textures[f'minecraft:entity/shield/{pattern}'].image
         assert isinstance(image, PIL.Image.Image)
         shield_model['textures']['0'] = image
         info.render_models[(f'shield.{pattern}', 'overlay')] = shield_model
   for (name, kind), layers in info.flat_items.items():
      font_sprites = [font.add_sprite(x) for x in layers.textures]
      for row in range(font.rows):
         text = get_space(font, comma_forward + (-18 if kind == 'overlay' else 0)) + get_space(font, -3).join([x.rows[row] + x.negative for x in font_sprites]) + get_space(font, 15 + comma_back)
         lang.data[f'tryashtar.shulker_preview.{kind}.{name}.{row}'] = text
   block_textures = info.render(ctx, vanilla)
   for sprite, image in block_textures.items():
      alpha = image.split()[3]
      partial = sum(1 if 50 <= x <= 190 else 0 for x in alpha.getdata())
      if partial >= 300:
         print(sprite)
         block_textures[sprite] = dither_transparency(image)
   block_grid = make_grid(block_textures, 64)
   resourcepack.textures['block_sheet'] = beet.Texture(block_grid.image)
   font.add_grid('tryashtar.shulker_preview:block_sheet', map_2d(block_grid.entries, lambda x: None if x is None else x[0]))
   for name, kind in info.render_models.keys():
      sprite = font.get_sprite(name)
      for row in range(font.rows):
         text = get_space(font, comma_forward + (-18 if kind == 'overlay' else 0)) + sprite.rows[row] + sprite.negative + get_space(font, 15 + comma_back)
         lang.data[f'tryashtar.shulker_preview.{kind}.{name}.{row}'] = text
   
   if font.upcoming_char > 0xf8ff:
      raise ValueError(font.upcoming_char)
   font_result = font.build()
   font_result.data['providers'][0] = {'comment':'Many thanks to AmberW for this invaluable concept'} | font_result.data['providers'][0]
   ctx.assets.fonts['minecraft:default'] = font_result

   length_dict: dict[int, list[Identifier]] = collections.defaultdict(list)
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

Tint = typing.Union[int, typing.Literal['dye', 'potion', 'map', 'firework'], None]

@dataclasses.dataclass
class TextureLayer:
   texture: ResourceLocation
   tint: Tint

@dataclasses.dataclass
class FlattenedLayers:
   textures: list[ResourceLocation]
   tint: Tint

@dataclasses.dataclass
class ModelOverride:
   sprite: str
   predicate: JsonDict
   kind: typing.Literal['item', 'override']

class ItemSpriteInfo:
   def __init__(self, colormap: dict[Identifier, list[Tint]]):
      self.colormap = colormap
      self.flat_items: dict[Sprite, FlattenedLayers] = {}
      self.render_models: dict[Sprite, ResourceLocation | JsonDict] = {}
      self.item_overrides: dict[Identifier, list[ModelOverride]] = {}
   
   def import_item(self, item: Identifier, pack: beet.ResourcePack):
      item = canon(item)
      nspace, path = item.split(':')
      model_name: ResourceLocation = f'{nspace}:item/{path}'
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
   
   def handle_model(self, item: Identifier, name: str, model_name: ResourceLocation, kind: SpriteKind, pack: beet.ResourcePack):
      model = pack.models[canon(model_name)]
      data = model_data(pack.models, model)
      if isinstance(data, LayeredModel):
         colors = self.colormap.get(short(item), [])
         layers = flatten_layers(data.layers, colors)
         if len(layers) > 0:
            self.flat_items[(name, kind)] = layers[0]
            if len(layers) == 2:
               self.flat_items[(name, 'overlay')] = layers[1]
            else:
               for i, layer in enumerate(layers[1:]):
                  self.flat_items[(f'{name}.{i + 1}', 'overlay')] = layer
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
   
   def render(self, ctx: beet.Context, pack: beet.contrib.vanilla.Release) -> dict[Sprite, PIL.Image.Image]:
      renderer = model_resolver.render.Render(ctx)
      renderer.getter._vanilla = pack
      renderer.default_render_size = 64
      for model in self.render_models.values():
         if isinstance(model, Identifier):
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
      return block_items

def flatten_layers(textures: list[ResourceLocation], colors: list[Tint]) -> list[FlattenedLayers]:
   result: list[FlattenedLayers] = []
   last_color: Tint = None
   current_layers: list[ResourceLocation] | None = None
   zipped = itertools.zip_longest(textures, colors, fillvalue=None)
   for texture, color in zipped:
      if texture is None:
         break
      if last_color != color:
         if current_layers is not None:
            result.append(FlattenedLayers(textures=current_layers, tint=last_color))
         last_color = color
         current_layers = []
      if current_layers is None:
         current_layers = []
      current_layers.append(texture)
   if current_layers is not None:
      result.append(FlattenedLayers(textures=current_layers, tint=last_color))
   return result

def dither_transparency(image: PIL.Image.Image) -> PIL.Image.Image:
   img = image.convert('RGBA')
   alpha = img.split()[3]
   dithered = alpha.convert(mode='1', dither=PIL.Image.Dither.FLOYDSTEINBERG)
   img.putalpha(dithered)
   return img

def override_check(item: Identifier, predicate: JsonDict, durability: int | None) -> tuple[NbtCompound, NbtCompound | None]:
   item = canon(item)
   if len(predicate) == 0:
      return ({'id':item}, None)
   positive: NbtCompound = {'id':item,'tag':{}}
   negative: NbtCompound = {'tag':{}}
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
      return (positive, None)
   return (positive, negative)

def fake_dye_color(dye: str) -> str:
   colors: dict[str, str] = {
      'white': 'white',
      'orange': 'gold',
      'magenta': 'light_purple',
      'light_blue': 'aqua',
      'yellow': 'yellow',
      'lime': 'green',
      'pink': 'light_purple',
      'gray': 'dark_gray',
      'light_gray': 'gray',
      'cyan': 'dark_aqua',
      'purple': 'dark_purple',
      'blue': 'blue',
      'brown': 'dark_red',
      'green': 'dark_green',
      'red': 'red',
      'black': 'black',
   }
   return colors[dye]

def fake_potion_color(effect: str) -> str:
   colors: dict[str, str] = {
      'strength': 'dark_red',
      'slow_falling': 'white',
      'luck': 'dark_green',
      'weakness': 'dark_gray',
      'regeneration': 'light_purple',
      'harming': 'dark_red',
      'poison': 'dark_green',
      'healing': 'red',
      'water_breathing': 'blue',
      'turtle_master': 'dark_gray',
      'slowness': 'dark_gray',
      'swiftness': 'aqua',
      'fire_resistance': 'gold',
      'leaping': 'green',
      'invisibility': 'gray',
      'night_vision': 'dark_blue',
   }
   return colors[effect]

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
