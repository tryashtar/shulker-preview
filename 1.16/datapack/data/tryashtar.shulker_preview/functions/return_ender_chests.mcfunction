# return to original slot, then remove from list and run recursively again if there's more
execute store result score #slot shulker_preview run data get storage tryashtar:shulker_preview ender_chests[1].Slot
data remove storage tryashtar:shulker_preview ender_chests[1].Slot
data modify block ~ 1 ~ Items[0] set from storage tryashtar:shulker_preview ender_chests[1]
function tryashtar.shulker_preview:return_item
data remove storage tryashtar:shulker_preview ender_chests[1]
execute if data storage tryashtar:shulker_preview ender_chests[1] run function tryashtar.shulker_preview:return_ender_chests
