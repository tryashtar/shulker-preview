import typing
import types
import dataclasses
import beet
import beet.contrib.vanilla
import plugins.info

def full(ctx: beet.Context):
   registry = fixed_release_registry(ctx)
   target = load_version_range(registry, ctx.meta['shulker_preview']['target_version'])
   ctx.meta['model_resolver']['minecraft_version'] = target.last.version
   plugin_version = ctx.meta['shulker_preview']['plugin']
   match plugin_version:
      case 1:
         import plugins.v1
         plugins.v1.main(ctx, registry, target)
      case 2:
         import plugins.v2
         plugins.v2.main(ctx, registry, target)
      case _:
         raise ValueError(plugin_version)
   export(ctx, target)

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
      info_data = plugins.info.version_info(release.client_jar)
      return VersionDef(
         version=info_data['id'],
         datapack=pack_version(info_data, 'data'),
         resourcepack=pack_version(info_data, 'resource'),
         data=info_data['world_version']
      )
   if isinstance(target, dict):
      if (version := target.get('version')) is not None:
         release = registry[target['version']]
         info_data = plugins.info.version_info(release.client_jar)
         return VersionDef(
            version=version,
            datapack=target.get('datapack', pack_version(info_data, 'data')),
            resourcepack=target.get('resourcepack', pack_version(info_data, 'resource')),
            data=target.get('data', info_data['world_version'])
         )
   raise ValueError(target)

def pack_version(info_data: dict[str, typing.Any], key: typing.Literal['data', 'resource']) -> int:
   value = info_data['pack_version']
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
