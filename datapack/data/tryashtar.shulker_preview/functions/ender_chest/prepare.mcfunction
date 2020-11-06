# copy all ender chests in inventory (not cursor) to list
data modify storage tryashtar.shulker_preview:data items set value []
data modify storage tryashtar.shulker_preview:data items append from entity @s Inventory[{id:"minecraft:ender_chest"}] 

scoreboard players set #header_type shulker_preview 1

# proceed if there is at least one
execute store result score #slot shulker_preview store success score #success shulker_preview run data get storage tryashtar.shulker_preview:data items[0].Slot
execute if score #success shulker_preview matches 1 run function tryashtar.shulker_preview:ender_chest/process
