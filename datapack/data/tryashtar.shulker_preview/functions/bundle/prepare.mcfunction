# copy all bundles in inventory (not cursor) to list
data modify storage tryashtar:shulker_preview items set value []
data modify storage tryashtar:shulker_preview items append from entity @s Inventory[{id:"minecraft:bundle"}]

# filter out bundles that haven't changed in size
function tryashtar.shulker_preview:bundle/filter
scoreboard players set #header_type shulker_preview 2

# proceed if there is at least one
execute store result score #slot shulker_preview store success score #bundles shulker_preview run data get storage tryashtar:shulker_preview items[0].Slot
execute if score #bundles shulker_preview matches 1 run function tryashtar.shulker_preview:bundle/process

# if not, stop scanning
execute if score #bundles shulker_preview matches 0 run tag @s remove shulker_preview.bundle
