# put the ender chest item in the global shulker box, copy the lore, and return it to the player
data modify block ~1 1 ~ RecordItem.tag.ender_chests[0].Slot set value 0b
data modify block ~1 1 ~ RecordItem.tag.ender_chests[0].tag.display.Lore set from block ~1 1 ~ RecordItem.tag.display.Lore
data modify block ~ 1 ~ Items[0] set from block ~1 1 ~ RecordItem.tag.ender_chests[0]
function tryashtar.shulker_preview:copy_item

# loop until all are processed
data remove block ~1 1 ~ RecordItem.tag.ender_chests[0]
execute store result score #slot shulker_preview store success score #has_slot shulker_preview run data get block ~1 1 ~ RecordItem.tag.ender_chests[0].Slot
execute if score #has_slot shulker_preview matches 1 run function tryashtar.shulker_preview:ender_chest/return_loop
