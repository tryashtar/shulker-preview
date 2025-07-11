import json
import os
import pathlib
import subprocess
import typing
import types
import re
import zipfile
import dataclasses
import PIL.Image
import PIL.ImageChops
import beet
import beet.contrib.vanilla

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

def plugin_v1_full(ctx: beet.Context):
   registry = fixed_release_registry(ctx)
   target = load_version_range(registry, ctx.meta['shulker_preview']['target_version'])
   plugin_v1(ctx, registry, target)
   export(ctx, target)

def plugin_v1(ctx: beet.Context, registry: beet.contrib.vanilla.ReleaseRegistry, target: VersionRange):
   target_version = target.last.version
   data_version = target.last.data
   ctx.meta['model_resolver']['minecraft_version'] = target_version
   vanilla = registry[target_version]
   items = [short(x) for x in get_registry(vanilla, 'minecraft:item').keys()]
   items.remove('air')
   eggs = spawn_egg_colors(registry['1.21.4'].assets, data_version)
   durability = item_durability(registry['1.21.4'], data_version)
   flat_items: dict[str, PIL.Image.Image] = {}
   overlays: dict[str, PIL.Image.Image] = {}
   block_items: list[str] = []
   for item in items:
      model = vanilla.assets.models[f'minecraft:item/{item}']
      layers = generated_layers(vanilla.assets.models, model)
      if layers is None or len(layers) == 0:
         block_items.append(item)
      else:
         image_layers = [vanilla.assets.textures[x].image.convert('RGBA') for x in layers]
         image = PIL.Image.new('RGBA', image_layers[0].size)
         for i, layer in enumerate(image_layers):
            if (color := eggs.get(canon(item))) is not None:
               color = eggs[canon(item)]
               if i == 0:
                  layer = colorize(layer, rgba(color.base))
               elif i == 1:
                  layer = colorize(layer, rgba(color.overlay))
            image.paste(layer, (0, 0), layer)
         flat_items[item] = image

def rgba(color: int):
   r = color // 256 // 256 % 256
   g = color // 256 % 256
   b = color % 256
   return (r, g, b, 255)

def colorize(image: PIL.Image.Image, color) -> PIL.Image.Image:
   return PIL.ImageChops.multiply(image, PIL.Image.new('RGBA', image.size, color))

def generated_layers(source: beet.NamespaceProxy[beet.Model], model: beet.Model) -> list[str] | None:
   result: list[str | None] = []
   while 'parent' in model.data:
      if 'elements' in model.data:
         return None
      if 'textures' in model.data:
         for name, path in model.data['textures'].items():
            match = re.match(r'layer(\d+)', name)
            if match:
               index = int(match.group(1))
               if index >= len(result):
                  result.extend([None] * (index - len(result) + 1))
               if result[index] is None:
                  result[index] = canon(path)
      parent = canon(model.data['parent'])
      if parent == 'minecraft:builtin/generated' or parent == 'minecraft:builtin/entity':
         return [x for x in result if x is not None]
      model = source[parent]
   if 'elements' in model.data:
      return None
   return []

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

@dataclasses.dataclass
class PotionEffect:
   id: str
   level: int

def potion_effects(data_version: int) -> dict[str, list[PotionEffect]]:
   if data_version < 100:
      raise ValueError(data_version)
   result: dict[str, list[PotionEffect]] = {
      'minecraft:empty': [],
      'minecraft:water': [],
      'minecraft:mundane': [],
      'minecraft:thick': [],
      'minecraft:awkward': [],
      'minecraft:night_vision': [PotionEffect(id='minecraft:night_vision', level=1)],
      'minecraft:long_night_vision': [PotionEffect(id='minecraft:night_vision', level=1)],
      'minecraft:invisibility': [PotionEffect(id='minecraft:invisibility', level=1)],
      'minecraft:long_invisibility': [PotionEffect(id='minecraft:invisibility', level=1)],
      'minecraft:leaping': [PotionEffect(id='minecraft:jump_boost', level=1)],
      'minecraft:long_leaping': [PotionEffect(id='minecraft:jump_boost', level=1)],
      'minecraft:strong_leaping': [PotionEffect(id='minecraft:jump_boost', level=2)],
      'minecraft:fire_resistance': [PotionEffect(id='minecraft:fire_resistance', level=1)],
      'minecraft:long_fire_resistance': [PotionEffect(id='minecraft:fire_resistance', level=1)],
      'minecraft:swiftness': [PotionEffect(id='minecraft:speed', level=1)],
      'minecraft:long_swiftness': [PotionEffect(id='minecraft:speed', level=1)],
      'minecraft:strong_swiftness': [PotionEffect(id='minecraft:speed', level=2)],
      'minecraft:slowness': [PotionEffect(id='minecraft:slowness', level=1)],
      'minecraft:long_slowness': [PotionEffect(id='minecraft:slowness', level=1)],
      'minecraft:strong_slowness': [PotionEffect(id='minecraft:slowness', level=5)],
      'minecraft:water_breathing': [PotionEffect(id='minecraft:water_breathing', level=1)],
      'minecraft:long_water_breathing': [PotionEffect(id='minecraft:water_breathing', level=1)],
      'minecraft:healing': [PotionEffect(id='minecraft:instant_health', level=1)],
      'minecraft:strong_healing': [PotionEffect(id='minecraft:instant_health', level=2)],
      'minecraft:harming': [PotionEffect(id='minecraft:instant_damage', level=1)],
      'minecraft:strong_harming': [PotionEffect(id='minecraft:instant_damage', level=2)],
      'minecraft:poison': [PotionEffect(id='minecraft:poison', level=1)],
      'minecraft:long_poison': [PotionEffect(id='minecraft:poison', level=1)],
      'minecraft:strong_poison': [PotionEffect(id='minecraft:poison', level=2)],
      'minecraft:regeneration': [PotionEffect(id='minecraft:regeneration', level=1)],
      'minecraft:long_regeneration': [PotionEffect(id='minecraft:regeneration', level=1)],
      'minecraft:strong_regeneration': [PotionEffect(id='minecraft:regeneration', level=2)],
      'minecraft:strength': [PotionEffect(id='minecraft:strength', level=1)],
      'minecraft:long_strength': [PotionEffect(id='minecraft:strength', level=1)],
      'minecraft:strong_strength': [PotionEffect(id='minecraft:strength', level=2)],
      'minecraft:weakness': [PotionEffect(id='minecraft:weakness', level=1)],
      'minecraft:long_weakness': [PotionEffect(id='minecraft:weakness', level=1)]
   }
   if data_version >= 143: # 15w44b
      result['minecraft:luck'] = [PotionEffect(id='minecraft:luck', level=1)]
   if data_version >= 1467: # 18w07a
      result['minecraft:turtle_master'] = [PotionEffect(id='minecraft:slowness', level=4), PotionEffect(id='minecraft:resistance', level=4)]
      result['minecraft:long_turtle_master'] = [PotionEffect(id='minecraft:slowness', level=4), PotionEffect(id='minecraft:resistance', level=4)]
      result['minecraft:strong_turtle_master'] = [PotionEffect(id='minecraft:slowness', level=6), PotionEffect(id='minecraft:resistance', level=6)]
   if data_version >= 1479: # 18w14a
      result['minecraft:slow_falling'] = [PotionEffect(id='minecraft:slow_falling', level=1)]
      result['minecraft:long_slow_falling'] = [PotionEffect(id='minecraft:slow_falling', level=1)]
   if data_version >= 1483: # 18w16a
      result['minecraft:turtle_master'] = [PotionEffect(id='minecraft:slowness', level=4), PotionEffect(id='minecraft:resistance', level=3)]
      result['minecraft:long_turtle_master'] = [PotionEffect(id='minecraft:slowness', level=4), PotionEffect(id='minecraft:resistance', level=3)]
      result['minecraft:strong_turtle_master'] = [PotionEffect(id='minecraft:slowness', level=6), PotionEffect(id='minecraft:resistance', level=4)]
   if data_version >= 1484: # 18w19a
      result['minecraft:strong_slowness'] = [PotionEffect(id='minecraft:slowness', level=4)]
   if data_version >= 3826: # 24w13a
      result['minecraft:wind_charged'] = [PotionEffect(id='minecraft:wind_charged', level=1)]
      result['minecraft:weaving'] = [PotionEffect(id='minecraft:weaving', level=1)]
      result['minecraft:oozing'] = [PotionEffect(id='minecraft:oozing', level=1)]
      result['minecraft:infested'] = [PotionEffect(id='minecraft:infested', level=1)]
   return result

def effect_colors(data_version: int) -> dict[str, int]:
   result: dict[str, int] = {
      'minecraft:speed': 0x33ebff,
      'minecraft:slowness': 0x8bafe0,
      'minecraft:haste': 0xd9c043,
      'minecraft:mining_fatigue': 0x4a4217,
      'minecraft:strength': 0xffc700,
      'minecraft:instant_health': 0xf82423,
      'minecraft:instant_damage': 0xa9656a,
      'minecraft:jump_boost': 0xfdff84,
      'minecraft:nausea': 0x551d4a,
      'minecraft:regeneration': 0xcd5cab,
      'minecraft:resistance': 0x9146f0,
      'minecraft:fire_resistance': 0xff9900,
      'minecraft:water_breathing': 0x98dac0,
      'minecraft:invisibility': 0xf6f6f6,
      'minecraft:blindness': 0x1f1f23,
      'minecraft:night_vision': 0xc2ff66,
      'minecraft:hunger': 0x587653,
      'minecraft:weakness': 0x484d48,
      'minecraft:poison': 0x87a363,
      'minecraft:wither': 0x736156,
      'minecraft:health_boost': 0xf87d23,
      'minecraft:absorption': 0x2552a5,
      'minecraft:saturation': 0xf82423,
      'minecraft:glowing': 0x94a061,
      'minecraft:levitation': 0xceffff,
      'minecraft:luck': 0x59c106,
      'minecraft:unluck': 0xc0a44d,
      'minecraft:slow_falling': 0xf3cfb9,
      'minecraft:conduit_power': 0x1dc2d1,
      'minecraft:dolphins_grace': 0x88a3be,
      'minecraft:bad_omen': 0xb6138,
      'minecraft:hero_of_the_village': 0x44ff44,
      'minecraft:darkness': 0x292721,
      'minecraft:trial_omen': 0x16a6a6,
      'minecraft:raid_omen': 0xde4058,
      'minecraft:wind_charged': 0xbdc9ff,
      'minecraft:weaving': 0x78695a,
      'minecraft:oozing': 0x99ffa3,
      'minecraft:infested': 0x8c9b8c,
   }
   if data_version < 3332: # 1.19.4-pre3
      result['minecraft:speed'] = 0x7cafc6
      result['minecraft:slowness'] = 0x5a6c81
      result['minecraft:strength'] = 0x932423
      result['minecraft:instant_damage'] = 0x430a09
      result['minecraft:jump_boost'] = 0x22ff4c
      result['minecraft:resistance'] = 0x99453a
      result['minecraft:fire_resistance'] = 0xe49a3a
      result['minecraft:water_breathing'] = 0x2e5299
      result['minecraft:invisibility'] = 0x7f8392
      result['minecraft:night_vision'] = 0x1f1fa1
      result['minecraft:poison'] = 0x4e9331
      result['minecraft:luck'] = 0x339900
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

def item_durability(release: beet.contrib.vanilla.Release, data_version: int) -> dict[str, int]:
   entries = get_item_components(release)
   result: dict[str, int] = {}
   for item, components in entries.items():
      if (damage := components.get('minecraft:max_damage')) is not None:
         result[item] = damage
   if data_version < 2834: # 21w37a
      result['minecraft:crossbow'] = 465
   return result
