data modify storage tryashtar.shulker_preview:data contents set from entity @s EnderItems

# process the first ender chest
function tryashtar.shulker_preview:from_player

# copy the identical lore to any remaining ender chests and return them quickly
data modify storage tryashtar.shulker_preview:data items[].tag.display.Lore set from entity 0-1c9-c369-0-2669 Item.tag.display.Lore
data modify storage tryashtar.shulker_preview:data items[].tag.HideFlags set value 32
data modify storage tryashtar.shulker_preview:data items[].tag.shulker_processed set value 1b
execute if data storage tryashtar.shulker_preview:data items[1] run function tryashtar.shulker_preview:ender_chest/return

kill 0-1c9-c369-0-2669
