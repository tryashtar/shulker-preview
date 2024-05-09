# return to original slot, then remove from list and run recursively again if there's more
execute store result score #slot shulker_preview run data get storage tryashtar.shulker_preview:data items[1].Slot
data modify entity 0-1c9-c369-0-2669 Item set from storage tryashtar.shulker_preview:data items[1]
function tryashtar.shulker_preview:return_item
data remove storage tryashtar.shulker_preview:data items[1]
execute if data storage tryashtar.shulker_preview:data items[1] run function tryashtar.shulker_preview:ender_chest/return
