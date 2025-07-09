# copy all boxes in inventory (not cursor) to list
data modify storage tryashtar.shulker_preview:data items set value []
data modify storage tryashtar.shulker_preview:data items append from entity @s Inventory[{tag:{BlockEntityTag:{Items:[{}]}}}]

# filter out boxes that have already been processed
data remove storage tryashtar.shulker_preview:data items[{tag:{shulker_processed:1b}}]
scoreboard players set #header_type shulker_preview 0

# proceed if there is at least one
execute store result score #slot shulker_preview store success score #success shulker_preview run data get storage tryashtar.shulker_preview:data items[0].Slot
execute if score #success shulker_preview matches 1 run function tryashtar.shulker_preview:shulker_box/process
