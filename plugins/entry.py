import beet
import plugins.v1
import plugins.v2
from plugins.version import fixed_release_registry, load_version_range, VersionRange

def main(ctx: beet.Context):
   registry = fixed_release_registry(ctx)
   target = load_version_range(registry, ctx.meta['shulker_preview']['target_version'])
   ctx.meta['model_resolver']['minecraft_version'] = target.last.version
   plugin_version = ctx.meta['shulker_preview']['plugin']
   match plugin_version:
      case 1:
         plugins.v1.main(ctx, registry, target)
      case 2:
         plugins.v2.main(ctx, registry, target)
      case _:
         raise ValueError(plugin_version)
   export(ctx, target)

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
