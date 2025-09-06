import json
import os
import pathlib
import subprocess
import typing
import dataclasses
import beet
import beet.contrib.vanilla
import zipfile
import model_resolver.item_model.tint_source
from plugins.util import short, canon, rgba, JsonDict

PackVersionInfo = typing.TypedDict('PackVersionInfo', {'resource': int, 'data': int})
VersionInfo = typing.TypedDict('VersionInfo', {'id': str, 'world_version': int, 'pack_version': int | PackVersionInfo})
def version_info(jar: beet.contrib.vanilla.ClientJar) -> VersionInfo:
   with zipfile.ZipFile(jar.path) as file:
      return json.load(file.open('version.json'))

def get_fake_model(item: str) -> JsonDict | None:
   item = short(item)
   if item == 'shield':
      with open('resources/fake_models/shield.json', 'r', encoding='utf-8') as file:
         model = json.load(file)
      return model
   if item == 'conduit':
      with open('resources/fake_models/conduit.json', 'r', encoding='utf-8') as file:
         model = json.load(file)
      return model
   if item.endswith('shulker_box'):
      if item == 'shulker_box':
         texture = 'minecraft:entity/shulker/shulker'
      else:
         color = item.removesuffix('shulker_box').removesuffix('_')
         texture = f'minecraft:entity/shulker/shulker_{color}'
      with open('resources/fake_models/shulker_box.json', 'r', encoding='utf-8') as file:
         model = json.load(file)
      model['textures']['0'] = texture
      return model
   if item.endswith('_banner'):
      color = item.removesuffix('_banner')
      tint = dye_colors()[color]
      with open('resources/fake_models/banner.json', 'r', encoding='utf-8') as file:
         model = json.load(file)
      tint = model_resolver.item_model.tint_source.TintSourceConstant(type='constant', value=tint)
      model['textures']['1'] = tuple([(model['textures']['1'], tint)])
      return model
   if item.endswith('_bed'):
      color = item.removesuffix('_bed')
      texture = f'minecraft:entity/bed/{color}'
      with open('resources/fake_models/bed.json', 'r', encoding='utf-8') as file:
         model = json.load(file)
      model['textures']['0'] = texture
      return model
   if item.endswith('chest'):
      kind = {'chest':'normal','trapped_chest':'trapped','ender_chest':'ender'}[item]
      texture = f'minecraft:entity/chest/{kind}'
      with open('resources/fake_models/chest.json', 'r', encoding='utf-8') as file:
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
      with open(f'resources/fake_models/{path}.json', 'r', encoding='utf-8') as file:
         model = json.load(file)
      if texture is not None:
         model['textures']['0'] = texture
      return model

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

def get_registry(release: beet.contrib.vanilla.Release, registry: str) -> JsonDict:
   path = generate_reports(release)
   with open(path / 'registries.json', encoding='utf-8') as file:
      data: JsonDict = json.load(file)[registry]['entries']
   return data

def get_item_components(release: beet.contrib.vanilla.Release) -> JsonDict:
   path = generate_reports(release)
   with open(path / 'items.json', encoding='utf-8') as file:
      items: JsonDict = json.load(file)
   return {name: value['components'] for name, value in items.items()}

def legacy_banner_patterns(data_version: int) -> dict[str, str]:
   result: dict[str, str] = {
      'b': 'base',
      'bs': 'stripe_bottom',
      'ts': 'stripe_top',
      'ls': 'stripe_left',
      'rs': 'stripe_right',
      'cs': 'stripe_center',
      'ms': 'stripe_middle',
      'drs': 'stripe_downright',
      'dls': 'stripe_downleft',
      'ss': 'small_stripes',
      'cr': 'cross',
      'sc': 'straight_cross',
      'ld': 'diagonal_left',
      'rud': 'diagonal_right',
      'lud': 'diagonal_up_left',
      'rd': 'diagonal_up_right',
      'vh': 'half_vertical',
      'vhr': 'half_vertical_right',
      'hh': 'half_horizontal',
      'hhb': 'half_horizontal_bottom',
      'bl': 'square_bottom_left',
      'br': 'square_bottom_right',
      'tl': 'square_top_left',
      'tr': 'square_top_right',
      'bt': 'triangle_bottom',
      'tt': 'triangle_top',
      'bts': 'triangles_bottom',
      'tts': 'triangles_top',
      'mc': 'circle',
      'mr': 'rhombus',
      'bo': 'border',
      'cbo': 'curly_border',
      'bri': 'bricks',
      'gra': 'gradient',
      'gru': 'gradient_up',
      'cre': 'creeper',
      'sku': 'skull',
      'flo': 'flower',
      'moj': 'mojang',
      'glb': 'globe'
   }
   if data_version >= 2525: # 20w15a
      result['pig'] = 'piglin'
   return result

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
      'orange': 0xf9801d,
      'magenta': 0xc74ebd,
      'light_blue': 0x3ab3da,
      'yellow': 0xfed83d,
      'lime': 0x80c71f,
      'pink': 0xf38baa,
      'gray': 0x474f52,
      'light_gray': 0x9d9d97,
      'cyan': 0x169c9c,
      'purple': 0x8932b8,
      'blue': 0x3c44aa,
      'brown': 0x835432,
      'green': 0x5e7c16,
      'red': 0xb02e26,
      'black': 0x1d1d21,
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
