import typing
import types
import dataclasses
import beet
import beet.contrib.vanilla
from plugins.info import version_info, VersionInfo

def fixed_release_registry(ctx: beet.Context) -> beet.contrib.vanilla.ReleaseRegistry:
   releases = beet.contrib.vanilla.ReleaseRegistry(ctx.cache['vanilla'], None)
   def fix_lookup(self, key: str) -> beet.contrib.vanilla.Release:
      for version in self.manifest.data['versions']:
         if version['id'] == key:
            info_file = beet.JsonFile(source_path=self.cache.download(version['url']))
            return beet.contrib.vanilla.Release(self.cache, info_file)
      raise KeyError(key)
   releases.missing = types.MethodType(fix_lookup, releases)
   return releases

@dataclasses.dataclass
class PackVersion:
   datapack: int
   resourcepack: int

@dataclasses.dataclass
class VersionDef:
   version: str
   pack: PackVersion
   world: int

@dataclasses.dataclass
class VersionRange:
   first: VersionDef
   last: VersionDef

RawVersionDict = typing.TypedDict('RawVersionDict', {'version': str, 'datapack': typing.NotRequired[int], 'resourcepack': typing.NotRequired[int], 'world': typing.NotRequired[int]})
RawVersion = str | RawVersionDict

def load_version_def(registry: beet.contrib.vanilla.ReleaseRegistry, target: RawVersion) -> VersionDef:
   if isinstance(target, str):
      release = registry[target]
      info_data = version_info(release.client_jar)
      pack = pack_version(info_data)
      return VersionDef(
         version=info_data['id'],
         pack=pack,
         world=info_data['world_version']
      )
   if isinstance(target, dict):
      version = target['version']
      datapack = target.get('datapack')
      resourcepack = target.get('resourcepack')
      world = target.get('world')
      if datapack is not None and resourcepack is not None and world is not None:
         return VersionDef(
            version=version,
            pack=PackVersion(datapack=datapack, resourcepack=resourcepack),
            world=world
         )
      release = registry[version]
      info_data = version_info(release.client_jar)
      pack = pack_version(info_data)
      if datapack is not None:
         pack.datapack = datapack
      if resourcepack is not None:
         pack.resourcepack = resourcepack
      if world is None:
         world = info_data['world_version']
      return VersionDef(
         version=version,
         pack=pack,
         world=world
      )
   raise ValueError(target)

def pack_version(info_data: VersionInfo) -> PackVersion:
   value = info_data['pack_version']
   if isinstance(value, int):
      return PackVersion(datapack=value, resourcepack=value)
   return PackVersion(datapack=value['data'], resourcepack=value['resource'])

def load_version_range(registry: beet.contrib.vanilla.ReleaseRegistry, target: RawVersion | tuple[RawVersion, RawVersion] | list[RawVersion]) -> VersionRange:
   if isinstance(target, str):
      both = load_version_def(registry, target)
      return VersionRange(first=both, last=both)
   if isinstance(target, (list, tuple)) and len(target) == 2:
      def1 = load_version_def(registry, target[0])
      def2 = load_version_def(registry, target[1])
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
