import json
import math
import os
import pathlib
import subprocess
import typing
import types
import re
import unicodedata
import zipfile
import dataclasses
import PIL.Image
import PIL.ImageChops
import beet
import beet.contrib.vanilla
import model_resolver

@dataclasses.dataclass
class VersionDef:
   version: str
   datapack: int
   resourcepack: int
   data: int

@dataclasses.dataclass
class VersionRange:
   first: VersionDef
   last: VersionDef

def load_version_def(registry: beet.contrib.vanilla.ReleaseRegistry, target: str | dict) -> VersionDef:
   if isinstance(target, str):
      release = registry[target]
      info = version_info(release.client_jar)
      return VersionDef(
         version=info['id'],
         datapack=pack_version(info, 'data'),
         resourcepack=pack_version(info, 'resource'),
         data=info['world_version']
      )
   if isinstance(target, dict):
      if (version := target.get('version')) is not None:
         release = registry[target['version']]
         info = version_info(release.client_jar)
         return VersionDef(
            version=version,
            datapack=target.get('datapack', pack_version(info, 'data')),
            resourcepack=target.get('resourcepack', pack_version(info, 'resource')),
            data=target.get('data', info['world_version'])
         )
   raise ValueError(target)

def pack_version(info: dict[str, typing.Any], key: typing.Literal['data', 'resource']) -> int:
   value = info['pack_version']
   if isinstance(value, int):
      return value
   return value[key]

def load_version_range(registry: beet.contrib.vanilla.ReleaseRegistry, target: str | dict | tuple[str | dict, str | dict] | list[str | dict]) -> VersionRange:
   if isinstance(target, str):
      both = load_version_def(registry, target)
      return VersionRange(first=both, last=both)
   if isinstance(target, tuple) or isinstance(target, list):
      def1 = load_version_def(registry, target[0])
      def2 = load_version_def(registry, target[-1])
      return VersionRange(first=def1, last=def2)
   if isinstance(target, dict):
      if 'from' in target and 'to' in target:
         def1 = load_version_def(registry, target['from'])
         def2 = load_version_def(registry, target['to'])
         return VersionRange(first=def1, last=def2)
      if 'version' in target:
         both = load_version_def(registry, target)
         return VersionRange(first=both, last=both)
   raise ValueError(target)

def version_info(jar: beet.contrib.vanilla.ClientJar) -> dict[str, typing.Any]:
   with zipfile.ZipFile(jar.path) as file:
      return json.load(file.open('version.json'))

def plugin_full(ctx: beet.Context):
   registry = fixed_release_registry(ctx)
   target = load_version_range(registry, ctx.meta['shulker_preview']['target_version'])
   ctx.meta['model_resolver']['minecraft_version'] = target.last.version
   plugin_version = ctx.meta['shulker_preview']['plugin']
   match plugin_version:
      case 1:
         plugin_v1(ctx, registry, target)
      case 2:
         plugin_v2(ctx, registry, target)
      case _:
         raise ValueError(plugin_version)
   export(ctx, target)

def plugin_v1(ctx: beet.Context, registry: beet.contrib.vanilla.ReleaseRegistry, target: VersionRange):
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
      *[(short(name), [0x385dc6]) for name in ['tipped_arrow', 'potion', 'splash_potion', 'lingering_potion']],
      ('firework_star', [None, 0x8a8a8a]),
      ('filled_map', [None, 0x46402e]),
   ])
   flat_items: dict[str, PIL.Image.Image] = {}
   overlays: dict[str, PIL.Image.Image] = {}
   render_models: dict[str, str] = {}
   for item in items:
      model_name = f'minecraft:item/{item}'
      model = vanilla.assets.models[model_name]
      data = model_data(vanilla.assets.models, model)
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
         overlays[f'arrow_dust.{potion_name}'] = colorize(arrow_overlay, rgba(color))
         overlays[f'potion_liquid.{potion_name}'] = colorize(potion_overlay, rgba(color))
   item_image, item_grid = make_grid(flat_items, 16)
   block_image, block_grid = make_grid(block_items, 64)
   overlay_image, overlay_grid = make_grid(overlays, 16)
   resourcepack.textures['item_sheet'] = beet.Texture(item_image)
   resourcepack.textures['block_sheet'] = beet.Texture(block_image)
   resourcepack.textures['overlay_sheet'] = beet.Texture(overlay_image)
   
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
      'chars': [',']
   })
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
   font.add_grid('tryashtar.shulker_preview:overlay_sheet', overlay_grid)
   lang.data['tryashtar.shulker_preview.empty_slot'] = get_space(font, 18)
   lang.data['tryashtar.shulker_preview.row_end'] = get_space(font, -162)

   font_result = font.build()
   font_result.data['providers'][0] = {'comment':'Many thanks to AmberW for this invaluable concept'} | font_result.data['providers'][0]
   ctx.assets.fonts['minecraft:default'] = font_result

def get_fake_model(item: str) -> dict[str, typing.Any] | None:
   print(item)
   if item == 'shield':
      with open('fake_models/shield.json', 'r', encoding='utf-8') as file:
         model = json.load(file)
      return model
   if item == 'conduit':
      with open('fake_models/conduit.json', 'r', encoding='utf-8') as file:
         model = json.load(file)
      return model
   if item.endswith('shulker_box'):
      color = item.removesuffix('shulker_box').removesuffix('_')
      texture = f'minecraft:entity/shulker/shulker_{color}'
      with open('fake_models/shulker_box.json', 'r', encoding='utf-8') as file:
         model = json.load(file)
      model['textures']['0'] = texture
      return model
   if item.endswith('_banner'):
      color = item.removesuffix('_banner')
      with open('fake_models/banner.json', 'r', encoding='utf-8') as file:
         model = json.load(file)
      return model
   if item.endswith('_bed'):
      color = item.removesuffix('_bed')
      texture = f'minecraft:entity/bed/{color}'
      with open('fake_models/bed.json', 'r', encoding='utf-8') as file:
         model = json.load(file)
      model['textures']['0'] = texture
      return model
   if item.endswith('chest'):
      kind = {'chest':'normal','trapped_chest':'trapped','ender_chest':'ender'}[item]
      texture = f'minecraft:entity/chest/{kind}'
      with open('fake_models/chest.json', 'r', encoding='utf-8') as file:
         model = json.load(file)
      model['textures']['0'] = texture
      return model
   if item.endswith('_head') or item.endswith('_skull'):
      kind = item.removesuffix('_head').removesuffix('_skull')
      match kind:
         case 'player' | 'dragon' | 'piglin' | 'zombie':
            path = kind + '_head'
            texture = None
         case 'creeper':
            path = 'generic_head'
            texture = 'entity/creeper/creeper'
         case 'skeleton':
            path = 'generic_head'
            texture = 'entity/skeleton/skeleton'
         case 'wither_skeleton':
            path = 'generic_head'
            texture = 'entity/skeleton/wither_skeleton'
         case _:
            raise ValueError(kind)
      with open(f'fake_models/{path}.json', 'r', encoding='utf-8') as file:
         model = json.load(file)
      if texture is not None:
         model['textures']['0'] = texture
      return model

def plugin_v2(ctx: beet.Context, registry: beet.contrib.vanilla.ReleaseRegistry, target: VersionRange):
   target_version = target.last.version
   data_version = target.last.data
   vanilla = registry[target_version]
   items = [short(x) for x in get_registry(vanilla, 'minecraft:item').keys()]
   items.remove('air')

def make_grid(entries: dict[str, PIL.Image.Image], icon_size: int) -> tuple[PIL.Image.Image, list[list[str | None]]]:
   width, height = grid_dimensions(len(entries))
   image = PIL.Image.new('RGBA', (width * icon_size, height * icon_size))
   name_return: list[list[str | None]] = [[None] * width for _ in range(height)]
   for i, (name, sprite) in enumerate(entries.items()):
      pos_x = i % width
      pos_y = i // width
      name_return[pos_y][pos_x] = name
      x = pos_x * icon_size
      y = pos_y * icon_size
      image.paste(sprite, (x, y, x + icon_size, y + icon_size))
   return (image, name_return)

def grid_dimensions(area: int) -> tuple[int, int]:
   width = math.ceil(math.sqrt(area))
   height = width
   if width * (height - 1) >= area:
      height -= 1
   return (width, height)

def rgba(color: int):
   r = color // 256 // 256 % 256
   g = color // 256 % 256
   b = color % 256
   return (r, g, b, 255)

def colorize(image: PIL.Image.Image, color) -> PIL.Image.Image:
   return PIL.ImageChops.multiply(image, PIL.Image.new('RGBA', image.size, color))

@dataclasses.dataclass
class LayeredModel:
   display: dict[str, typing.Any]
   layers: list[str]

@dataclasses.dataclass
class ElementModel:
   display: dict[str, typing.Any]
   elements: list[dict[str, typing.Any]]

@dataclasses.dataclass
class EntityModel:
   display: dict[str, typing.Any]

def model_data(source: beet.NamespaceProxy[beet.Model], model: beet.Model) -> LayeredModel | ElementModel | EntityModel:
   display: dict[str, typing.Any] = {}
   result: list[str | None] = []
   while True:
      if (model_display := model.data.get('display')) is not None:
         for key, value in model_display.items():
            if key not in display:
               display[key] = value
      if (elements := model.data.get('elements')) is not None:
         return ElementModel(display=display, elements=elements)
      if 'textures' in model.data:
         for name, path in model.data['textures'].items():
            match = re.match(r'layer(\d+)', name)
            if match:
               index = int(match.group(1))
               if index >= len(result):
                  result.extend([None] * (index - len(result) + 1))
               if result[index] is None:
                  result[index] = canon(path)
      if (parent := model.data.get('parent')) is not None:
         parent = canon(parent)
         if parent == 'minecraft:builtin/entity':
            return EntityModel(display=display)
         if parent == 'minecraft:builtin/generated':
            return LayeredModel(display=display, layers=[x for x in result if x is not None])
         model = source[parent]
         continue
      return LayeredModel(display=display, layers=[])

def export(ctx: beet.Context, target: VersionRange):
   ctx.assets.pack_format = target.last.resourcepack
   ctx.assets.supported_formats = [target.first.resourcepack, target.last.resourcepack]
   ctx.assets.description = 'Shulker Box tooltip preview: resource pack'
   ctx.assets.save(path=ctx.directory / 'out/resourcepack', overwrite=True)
   ctx.assets.save(path=ctx.directory / f'out/Shulker Preview Resource Pack ({target.first.version}).zip', zipped=True, overwrite=True)
   ctx.data.pack_format = target.last.datapack
   ctx.data.supported_formats = [target.first.datapack, target.last.datapack]
   ctx.data.description = 'Shulker Box tooltip preview: data pack'
   ctx.data.save(path=ctx.directory / 'out/datapack', overwrite=True)
   ctx.data.save(path=ctx.directory / f'out/Shulker Preview Data Pack ({target.first.version}).zip', zipped=True, overwrite=True)
   dark_theme = beet.ResourcePack(path='in/resourcepack_dark')
   dark_theme.pack_format = ctx.assets.pack_format
   dark_theme.supported_formats = [target.first.resourcepack, target.last.resourcepack]
   dark_theme.description = '(apply this pack above the normal resource pack)'
   dark_theme.save(path=ctx.directory / 'out/dark_theme', overwrite=True)
   dark_theme.save(path=ctx.directory / f'out/Shulker Preview Dark Theme ({target.first.version}).zip', zipped=True, overwrite=True)

def fixed_release_registry(ctx: beet.Context) -> beet.contrib.vanilla.ReleaseRegistry:
   releases = beet.contrib.vanilla.ReleaseRegistry(ctx.cache['vanilla'], None)
   def fix_lookup(self, key: str) -> beet.contrib.vanilla.Release:
      for version in self.manifest.data['versions']:
         if version['id'] == key:
             info = beet.JsonFile(source_path=self.cache.download(version['url']))
             return beet.contrib.vanilla.Release(self.cache, info)
      raise KeyError(key)
   releases.missing = types.MethodType(fix_lookup, releases)
   return releases

def generate_reports(release: beet.contrib.vanilla.Release) -> pathlib.Path:
   info = version_info(release.client_jar)
   data_version = info['world_version']
   version_name = info['id']
   server_jar_url = release.info.data['downloads']['server']['url']
   jar = release.cache.download(server_jar_url)
   path = release.cache.get_path(f'reports for {version_name}')
   if not path.is_dir():
      os.makedirs(path, exist_ok=True)
      if data_version >= 2836: # 21w39a
         data_command = ['java', '-DbundlerMainClass=net.minecraft.data.Main', '-jar', jar, '--reports']
      else:
         data_command = ['java', '-cp', jar, 'net.minecraft.data.Main', '--reports']
      subprocess.run(data_command, cwd=path, check=True)
   return path / 'generated/reports'

def get_registry(release: beet.contrib.vanilla.Release, registry: str) -> dict[str, typing.Any]:
   path = generate_reports(release)
   with open(path / 'registries.json', encoding='utf-8') as file:
      data = json.load(file)[registry]['entries']
   return data

def get_item_components(release: beet.contrib.vanilla.Release) -> dict[str, typing.Any]:
   path = generate_reports(release)
   with open(path / 'items.json', encoding='utf-8') as file:
      items = json.load(file)
   return {name: value['components'] for name, value in items.items()}

def canon(location: str) -> str:
   return f'minecraft:{location}' if ':' not in location else location

def short(location: str) -> str:
   return location.removeprefix('minecraft:')

def potion_effects(data_version: int) -> dict[str, dict[str, int]]:
   if data_version < 100:
      raise ValueError(data_version)
   result: dict[str, dict[str, int]] = {
      'empty': {},
      'water': {},
      'mundane': {},
      'thick': {},
      'awkward': {},
      'night_vision': {'night_vision': 1},
      'long_night_vision': {'night_vision': 1},
      'invisibility': {'invisibility': 1},
      'long_invisibility': {'invisibility': 1},
      'leaping': {'jump_boost': 1},
      'long_leaping': {'jump_boost': 1},
      'strong_leaping': {'jump_boost': 2},
      'fire_resistance': {'fire_resistance': 1},
      'long_fire_resistance': {'fire_resistance': 1},
      'swiftness': {'speed': 1},
      'long_swiftness': {'speed': 1},
      'strong_swiftness': {'speed': 2},
      'slowness': {'slowness': 1},
      'long_slowness': {'slowness': 1},
      'strong_slowness': {'slowness': 5},
      'water_breathing': {'water_breathing': 1},
      'long_water_breathing': {'water_breathing': 1},
      'healing': {'instant_health': 1},
      'strong_healing': {'instant_health': 2},
      'harming': {'instant_damage': 1},
      'strong_harming': {'instant_damage': 2},
      'poison': {'poison': 1},
      'long_poison': {'poison': 1},
      'strong_poison': {'poison': 2},
      'regeneration': {'regeneration': 1},
      'long_regeneration': {'regeneration': 1},
      'strong_regeneration': {'regeneration': 2},
      'strength': {'strength': 1},
      'long_strength': {'strength': 1},
      'strong_strength': {'strength': 2},
      'weakness': {'weakness': 1},
      'long_weakness': {'weakness': 1}
   }
   if data_version >= 143: # 15w44b
      result['luck'] = {'luck': 1}
   if data_version >= 1467: # 18w07a
      result['turtle_master'] = {'slowness': 4, 'resistance': 4}
      result['long_turtle_master'] = {'slowness': 4, 'resistance': 4}
      result['strong_turtle_master'] = {'slowness': 6, 'resistance': 6}
   if data_version >= 1479: # 18w14a
      result['slow_falling'] = {'slow_falling': 1}
      result['long_slow_falling'] = {'slow_falling': 1}
   if data_version >= 1483: # 18w16a
      result['turtle_master'] = {'slowness': 4, 'resistance': 3}
      result['long_turtle_master'] = {'slowness': 4, 'resistance': 3}
      result['strong_turtle_master'] = {'slowness': 6, 'resistance': 4}
   if data_version >= 1484: # 18w19a
      result['strong_slowness'] = {'slowness': 4}
   if data_version >= 3826: # 24w13a
      result['wind_charged'] = {'wind_charged': 1}
      result['weaving'] = {'weaving': 1}
      result['oozing'] = {'oozing': 1}
      result['infested'] = {'infested': 1}
   return {canon(name): {canon(effect): level for effect, level in value.items()} for name, value in result.items()}

def dye_colors() -> dict[str, int]:
   return {
      'white': 0xf9fffe,
      'light_gray': 0x9d9d97,
      'gray': 0x474f52,
      'black': 0x1d1d21,
      'brown': 0x835432,
      'red': 0xb02e26,
      'orange': 0xf9801d,
      'yellow': 0xfed83d,
      'lime': 0x80c71f,
      'green': 0x5e7c16,
      'cyan': 0x169c9c,
      'light_blue': 0x3ab3da,
      'blue': 0x3c44aa,
      'purple': 0x8932b8,
      'magenta': 0xc74ebd,
      'pink': 0xf38baa,
   }

def effect_colors(data_version: int) -> dict[str, int]:
   result: dict[str, int] = {
      'speed': 0x33ebff,
      'slowness': 0x8bafe0,
      'haste': 0xd9c043,
      'mining_fatigue': 0x4a4217,
      'strength': 0xffc700,
      'instant_health': 0xf82423,
      'instant_damage': 0xa9656a,
      'jump_boost': 0xfdff84,
      'nausea': 0x551d4a,
      'regeneration': 0xcd5cab,
      'resistance': 0x9146f0,
      'fire_resistance': 0xff9900,
      'water_breathing': 0x98dac0,
      'invisibility': 0xf6f6f6,
      'blindness': 0x1f1f23,
      'night_vision': 0xc2ff66,
      'hunger': 0x587653,
      'weakness': 0x484d48,
      'poison': 0x87a363,
      'wither': 0x736156,
      'health_boost': 0xf87d23,
      'absorption': 0x2552a5,
      'saturation': 0xf82423,
      'glowing': 0x94a061,
      'levitation': 0xceffff,
      'luck': 0x59c106,
      'unluck': 0xc0a44d,
      'slow_falling': 0xf3cfb9,
      'conduit_power': 0x1dc2d1,
      'dolphins_grace': 0x88a3be,
      'bad_omen': 0xb6138,
      'hero_of_the_village': 0x44ff44,
      'darkness': 0x292721,
      'trial_omen': 0x16a6a6,
      'raid_omen': 0xde4058,
      'wind_charged': 0xbdc9ff,
      'weaving': 0x78695a,
      'oozing': 0x99ffa3,
      'infested': 0x8c9b8c,
   }
   if data_version < 3332: # 1.19.4-pre3
      result |= {
         'speed': 0x7cafc6,
         'slowness': 0x5a6c81,
         'strength': 0x932423,
         'instant_damage': 0x430a09,
         'jump_boost': 0x22ff4c,
         'resistance': 0x99453a,
         'fire_resistance': 0xe49a3a,
         'water_breathing': 0x2e5299,
         'invisibility': 0x7f8392,
         'night_vision': 0x1f1fa1,
         'poison': 0x4e9331,
         'luck': 0x339900,
      }
   return {canon(name): color for name, color in result.items()}

def potion_colors(data_version: int) -> dict[str, int | None]:
   result: dict[str, int | None] = {}
   potions = potion_effects(data_version)
   colors = effect_colors(data_version)
   for potion, contents in potions.items():
      if len(contents) == 0:
         result[potion] = None
      else:
         red, green, blue, total = (0, 0, 0, 0)
         for name, level in contents.items():
            r, g, b, _ = rgba(colors[name])
            red += r * level
            green += g * level
            blue += b * level
            total += level
         result[potion] = (red * 256 * 256 // total) + (green * 256 // total) + (blue // total)
   return result

K = typing.TypeVar('K')
V = typing.TypeVar('V')
def invert_dict(dictionary: dict[K, V]) -> dict[V, list[K]]:
   result: dict[V, list[K]] = {}
   for key, value in dictionary.items():
      if value not in result:
         result[value] = []
      result[value].append(key)
   return result

@dataclasses.dataclass
class DoubleTint:
   base: int
   overlay: int

def spawn_egg_colors(pack: beet.ResourcePack, data_version: int) -> dict[str, DoubleTint]:
   if data_version < 100:
      raise ValueError(data_version)
   result: dict[str, DoubleTint] = {}
   for name, model in pack.item_models.items():
      if name.endswith('_spawn_egg'):
         tints = model.data['model']['tints']
         result[canon(name)] = DoubleTint(base=tints[0]['value'], overlay=tints[1]['value'])
   if data_version < 1484: # 18w19a
      result['minecraft:phantom_spawn_egg'] = DoubleTint(base=0x353043, overlay=0x79be46)
   if data_version < 2210: # 19w41a
      result['minecraft:bee_spawn_egg'] = DoubleTint(base=0xffe55e, overlay=0x262630)
   if data_version < 2506: # 20w07a
      result['minecraft:hoglin_spawn_egg'] = DoubleTint(base=0xea9393, overlay=0x4c7129)
   if data_version < 3206: # 22w43a
      result['minecraft:camel_spawn_egg'] = DoubleTint(base=0x9c6a1a, overlay=0xe3b771)
   if data_version < 3207: # 22w44a
      result['minecraft:polar_bear_spawn_egg'] = DoubleTint(base=0xf2f2f2, overlay=0x959590)
   if data_version < 3330: # 1.19.4-pre1
      result['minecraft:sniffer_spawn_egg'] = DoubleTint(base=0x962930, overlay=0x4d9960)
   if data_version < 3804: # 24w03a
      result['minecraft:armadillo_spawn_egg'] = DoubleTint(base=0xa67775, overlay=0x734b4f)
   return result

def item_colors(pack: beet.ResourcePack, data_version: int) -> dict[str, int]:
   result: dict[str, int] = {}
   for name, model in pack.item_models.items():
      if (tints := model.data['model'].get('tints')) is not None and len(tints) == 1:
         tint = tints[0]
         if short(tint['type']) == 'grass':
            if tint['downfall'] == 1.0 and tint['temperature'] == 0.5:
               tint['type'] = 'minecraft:constant'
               tint['value'] = 0xff7bbd6b
         if short(tint['type']) == 'constant':
            final_name = short(name)
            if data_version < 3693: # 1.20.3-pre1
               if final_name == 'short_grass':
                  final_name = 'grass'
            result[canon(final_name)] = tint['value']
   return result

def item_durability(release: beet.contrib.vanilla.Release, data_version: int) -> dict[str, int]:
   entries = get_item_components(release)
   result: dict[str, int] = {}
   for item, components in entries.items():
      if (damage := components.get('minecraft:max_damage')) is not None:
         result[item] = damage
   if data_version < 2834: # 21w37a
      result['minecraft:crossbow'] = 465
   return result

@dataclasses.dataclass
class GridData:
   rows: list[list[str]]
   negative: list[str]

@dataclasses.dataclass
class SpriteData:
   rows: list[str]
   negative: str

class FontManager:
   def __init__(self, rows: int):
      self.legacy_space_texture: str | None = None
      self.rows: int = rows
      self.upcoming_char: int = 1
      self.spaces: dict[int, str] = {}
      self.sprites: dict[str, SpriteData] = {}
      self.grids: dict[str, GridData] = {}
      self.sprite_map: dict[str, SpriteData] = {}
      self.providers: list[dict[str, typing.Any]] = []
   
   def add_sprite(self, texture: str) -> SpriteData:
      if texture not in self.sprite_map:
         data = SpriteData(rows=[self.next_char() for _ in range(self.rows)], negative=self.next_char())
         self.sprites[texture + '.png'] = data
         self.sprite_map[texture] = data
      return self.sprite_map[texture]
   
   def add_grid(self, grid: str, textures: list[list[str | None]]) -> GridData:
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
               self.sprite_map[texture] = SpriteData(rows=rowchars, negative=n)
            else:
               for x in rows:
                  x[-1] += '\u0000'
               negative[-1] += '\u0000'
      data = GridData(rows=rows, negative=negative)
      self.grids[grid + '.png'] = data
      return data
   
   def add_provider(self, provider: dict[str, typing.Any]):
      self.providers.append(provider)
      
   def get_sprite(self, name: str) -> SpriteData:
      return self.sprite_map[name]
   
   def next_char(self):
      char = self.upcoming_char
      for low, high in [(0xd800, 0xdbff), (0xdc00, 0xdfff), (0x05c8, 0x05d2), (0x05e8, 0x06ff), (0x070b, 0x0710), (0x072d, 0x072f), (0x074b, 0x074f), (0x07a4, 0x07a5), (0x07b1, 0x07c2), (0x07f4, 0x07f5), (0x07fa, 0x07fc), (0x07fe, 0x0800), (0x082e, 0x0832), (0x083c, 0x0842), (0x0856, 0x0858), (0x085c, 0x0862), (0x0868, 0x0897), (0x08a0, 0x08a2), (0x08b2, 0x08b8), (0x08c5, 0x08c9), (0xfb34, 0xfb48), (0xfbbf, 0xfbd5), (0xfd8d, 0xfd94), (0xfdc5, 0xfdce), (0xfdf0, 0xfdf2), (0xfe72, 0xfe78), (0xfefa, 0xfefe)]:
         if low <= char <= high:
            char = high + 1
      while char in [0x0000, 0x000a, 0x00a7, 0x0025, 0x0590, 0x05be, 0x05c0, 0x05c3, 0x05c6, 0x0608, 0x060b, 0x060d, 0x0712, 0x081a, 0x0824, 0x0828, 0x200f, 0xfb1d, 0xfb1f] or unicodedata.bidirectional(chr(char)) in ['AL', 'R', 'NSM']:
         char += 1
      self.upcoming_char = char + 1
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
         if self.legacy_space_texture is None:
            spaces = {}
            for width, char in self.spaces.items():
               spaces[char] = width
            providers.append({'type':'space','advances':spaces})
         else:
            for width, char in self.spaces.items():
               height = width - 1 if width >= 0 else width - 2
               providers.append({
                  'type':'bitmap',
                  'file': self.legacy_space_texture + '.png',
                  'ascent': -65536,
                  'height': height,
                  'chars': [char],
               })
      providers.extend(self.providers)
      for path, data in self.sprites.items():
         for row, entry in enumerate(data.rows):
            providers.append({'type':'bitmap','file':path,'ascent':-2 + (row * -18),'height':16,'chars':[entry]})
         providers.append({'type':'bitmap','file':path,'ascent':-32768,'height':-16,'chars':[data.negative]})
      for path, data in self.grids.items():
         for row, entry in enumerate(data.rows):
            providers.append({'type':'bitmap','file':path,'ascent':-2 + (row * -18),'height':16,'chars':entry})
         providers.append({'type':'bitmap','file':path,'ascent':-32768,'height':-16,'chars':data.negative})
      result.data['providers'] = providers
      return result

def add_tooltip(font: FontManager, texture: str, bottom: int) -> str:
   ascent = 8
   slices: list[tuple[int, list[int]]] = [(8, [0]), (8, [2,3,4,5,6,7,8,bottom])]
   text = ''
   for height, ranges in slices:
      for include in ranges:
         positive = ['\u0000'] * (256 // height)
         negative = ['\u0000'] * (256 // height)
         pos = font.next_char()
         neg = font.next_char()
         positive[include] = pos
         negative[include] = neg
         font.add_provider({
            'type': 'bitmap',
            'file': texture + '.png',
            'ascent': ascent,
            'height': height,
            'chars': positive
         })
         font.add_provider({
            'type': 'bitmap',
            'file': texture + '.png',
            'ascent': -32768,
            'height': height,
            'chars': negative
         })
         ascent -= height
         text += pos + neg + get_space(font, -3)
   return text

@dataclasses.dataclass
class NumberData:
   normal: list[str]
   shadow: list[str]
   negative: str

def add_numbers(font: FontManager) -> list[NumberData]:
   result: list[NumberData] = []
   for _ in range(10):
      data = NumberData(
         normal=[font.next_char() for _ in range(font.rows)],
         shadow=[font.next_char() for _ in range(font.rows)],
         negative=font.next_char(),
      )
      result.append(data)
   empty_row = '\u0000' * 16
   negatives = ''.join([x.negative for x in result])
   for row in range(font.rows):
      normals = ''.join([x.normal[row] for x in result])
      shadows = ''.join([x.shadow[row] for x in result])
      def get_grid(numbers: str):
         return [*([empty_row] * 3), numbers + ('\u0000' * 6), *([empty_row] * 12)]
      font.add_provider({
         'type': 'bitmap',
         'file': 'minecraft:font/ascii.png',
         'ascent': -(18 * row) - 11,
         'height': 8,
         'chars': get_grid(normals)
      })
      font.add_provider({
         'type': 'bitmap',
         'file': 'minecraft:font/ascii.png',
         'ascent': -(18 * row) - 12,
         'height': 8,
         'chars': get_grid(shadows)
      })
      font.add_provider({
         'type': 'bitmap',
         'file': 'minecraft:font/ascii.png',
         'ascent': -32768,
         'height': -8,
         'chars': get_grid(negatives)
      })
   return result

def get_space(font: FontManager, width: int) -> str:
   if (exact := font.spaces.get(width)) is not None:
      return exact
   current_width = 0
   result_str = ''
   if width > 0:
      while current_width < width:
         small_enough = [(w, char) for w, char in font.spaces.items() if current_width + w <= width]
         if len(small_enough) == 0:
            raise ValueError(width)
         w, char = max(small_enough, key=lambda tup: tup[0])
         if w < 1:
            raise ValueError(width)
         current_width += w
         result_str += char
      return result_str
   if width < 0:
      while current_width > width:
         small_enough = [(w, char) for w, char in font.spaces.items() if current_width + w >= width]
         if len(small_enough) == 0:
            raise ValueError(width)
         w, char = min(small_enough, key=lambda tup: tup[0])
         if w > -1:
            raise ValueError(width)
         current_width += w
         result_str += char
      return result_str
   return ''
