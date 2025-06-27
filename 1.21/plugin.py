import beet
import beet.contrib
import beet.contrib.vanilla

def main(ctx: beet.Context):
   vanilla = ctx.inject(beet.contrib.vanilla.Vanilla)
   for name, entry in vanilla.assets.item_models.items():
      print(name, entry.data)

