import beet
import beet.contrib.vanilla
from plugins.util import short
from plugins.version import VersionRange
from plugins.info import get_registry

def main(ctx: beet.Context, registry: beet.contrib.vanilla.ReleaseRegistry, target: VersionRange):
   target_version = target.last.name
   data_version = target.last.world
   vanilla = registry[target_version]
   items = [short(x) for x in get_registry(vanilla, 'minecraft:item').keys()]
   items.remove('air')
