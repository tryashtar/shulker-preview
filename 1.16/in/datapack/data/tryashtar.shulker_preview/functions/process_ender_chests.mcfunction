# generate lore for the first ender chest
function tryashtar.shulker_preview:from_player

# copy the identical lore to any remaining ender chests and return them quickly
data modify storage tryashtar:shulker_preview ender_chests[].tag.display.Lore set from block ~ 1 ~ Items[0].tag.display.Lore
data modify storage tryashtar:shulker_preview ender_chests[].tag.HideFlags set value 32
data modify storage tryashtar:shulker_preview ender_chests[].tag.shulker_processed set value 1b
execute if data storage tryashtar:shulker_preview ender_chests[1] run function tryashtar.shulker_preview:return_ender_chests
