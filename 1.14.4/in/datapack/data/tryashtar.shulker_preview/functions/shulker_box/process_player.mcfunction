# use the jukebox as a temporary storage location for unprocessed containers in the player's inventory
# checking for shulker box IDs would be too expensive here
data modify block ~1 1 ~ RecordItem set value {id:"tnt",Count:1b}
data modify block ~1 1 ~ RecordItem.tag.shulker_boxes append from entity @s Inventory[{tag:{BlockEntityTag:{Items:[{}]}}}]
data remove block ~1 1 ~ RecordItem.tag.shulker_boxes[{tag:{"shulker_preview.processed":1b}}]

# only process the first shulker box
execute store result score #slot shulker_preview store success score #has_slot shulker_preview run data get block ~1 1 ~ RecordItem.tag.shulker_boxes[0].Slot
execute if score #has_slot shulker_preview matches 1 run function tryashtar.shulker_preview:shulker_box/process_player2
