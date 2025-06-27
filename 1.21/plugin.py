import beet
import beet.contrib
import beet.contrib.vanilla
import model_resolver

def main(ctx: beet.Context):
   target_version = '1.21.6'
   vanilla = beet.contrib.vanilla.Vanilla(ctx, minecraft_version=target_version)
   ctx.meta['model_resolver'] = model_resolver.ModelResolverOptions(minecraft_version=target_version, preferred_minecraft_generated='java')
   render = model_resolver.Render(ctx)
   for name, entry in vanilla.assets.item_models.items():
      print(name, entry.data)
      render.add_item_task(
         model_resolver.Item(id=name, components={'minecraft:item_model':name}),
         path_ctx=name,
         animation_mode="one_file"
      )
   render.run()
