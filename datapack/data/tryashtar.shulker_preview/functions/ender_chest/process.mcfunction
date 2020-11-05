data modify storage tryashtar:shulker_preview contents set from entity @s EnderItems

# generate lore for the first ender chest
function tryashtar.shulker_preview:from_player

# copy the identical lore to any remaining ender chests and return them quickly
data modify storage tryashtar:shulker_preview items[].tag.display.Lore set from storage tryashtar:shulker_preview items[0].tag.display.Lore
data modify storage tryashtar:shulker_preview items[].tag.HideFlags set value 32
data modify storage tryashtar:shulker_preview items[].tag.shulker_processed set value 1b
execute if data storage tryashtar:shulker_preview items[1] run function tryashtar.shulker_preview:ender_chest/return
