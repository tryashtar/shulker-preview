# the processing function works on a single item, so we need to spawn an item entity to run it
# we can copy the player's box to and from it quickly
summon item ~ -10000 ~ {Invulnerable:1b,NoGravity:1b,Silent:1b,UUID:[I;1936225644,1801810464,1886545270,1768257343],Item:{id:"tnt",count:1}}
function tryashtar.shulker_preview:shulker_box/from_inventory
data modify storage tryashtar.shulker_preview:data contents set from entity 7368756c-6b65-7220-7072-65766965773f Item.components."minecraft:container"

# process the item, creating the tooltip
# copy it back to the player
execute as 7368756c-6b65-7220-7072-65766965773f run function tryashtar.shulker_preview:process
function tryashtar.shulker_preview:shulker_box/to_inventory
kill 7368756c-6b65-7220-7072-65766965773f
