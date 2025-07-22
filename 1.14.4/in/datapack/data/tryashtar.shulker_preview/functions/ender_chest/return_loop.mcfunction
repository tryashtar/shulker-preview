# we need to remove the slot tag
execute if score #slot shulker_preview matches 0 run data modify block ~1 1 ~ RecordItem.tag.item set from entity @s Inventory[{Slot:0b}]
execute if score #slot shulker_preview matches 1 run data modify block ~1 1 ~ RecordItem.tag.item set from entity @s Inventory[{Slot:1b}]
execute if score #slot shulker_preview matches 2 run data modify block ~1 1 ~ RecordItem.tag.item set from entity @s Inventory[{Slot:2b}]
execute if score #slot shulker_preview matches 3 run data modify block ~1 1 ~ RecordItem.tag.item set from entity @s Inventory[{Slot:3b}]
execute if score #slot shulker_preview matches 4 run data modify block ~1 1 ~ RecordItem.tag.item set from entity @s Inventory[{Slot:4b}]
execute if score #slot shulker_preview matches 5 run data modify block ~1 1 ~ RecordItem.tag.item set from entity @s Inventory[{Slot:5b}]
execute if score #slot shulker_preview matches 6 run data modify block ~1 1 ~ RecordItem.tag.item set from entity @s Inventory[{Slot:6b}]
execute if score #slot shulker_preview matches 7 run data modify block ~1 1 ~ RecordItem.tag.item set from entity @s Inventory[{Slot:7b}]
execute if score #slot shulker_preview matches 8 run data modify block ~1 1 ~ RecordItem.tag.item set from entity @s Inventory[{Slot:8b}]
execute if score #slot shulker_preview matches 9 run data modify block ~1 1 ~ RecordItem.tag.item set from entity @s Inventory[{Slot:9b}]
execute if score #slot shulker_preview matches 10 run data modify block ~1 1 ~ RecordItem.tag.item set from entity @s Inventory[{Slot:10b}]
execute if score #slot shulker_preview matches 11 run data modify block ~1 1 ~ RecordItem.tag.item set from entity @s Inventory[{Slot:11b}]
execute if score #slot shulker_preview matches 12 run data modify block ~1 1 ~ RecordItem.tag.item set from entity @s Inventory[{Slot:12b}]
execute if score #slot shulker_preview matches 13 run data modify block ~1 1 ~ RecordItem.tag.item set from entity @s Inventory[{Slot:13b}]
execute if score #slot shulker_preview matches 14 run data modify block ~1 1 ~ RecordItem.tag.item set from entity @s Inventory[{Slot:14b}]
execute if score #slot shulker_preview matches 15 run data modify block ~1 1 ~ RecordItem.tag.item set from entity @s Inventory[{Slot:15b}]
execute if score #slot shulker_preview matches 16 run data modify block ~1 1 ~ RecordItem.tag.item set from entity @s Inventory[{Slot:16b}]
execute if score #slot shulker_preview matches 17 run data modify block ~1 1 ~ RecordItem.tag.item set from entity @s Inventory[{Slot:17b}]
execute if score #slot shulker_preview matches 18 run data modify block ~1 1 ~ RecordItem.tag.item set from entity @s Inventory[{Slot:18b}]
execute if score #slot shulker_preview matches 19 run data modify block ~1 1 ~ RecordItem.tag.item set from entity @s Inventory[{Slot:19b}]
execute if score #slot shulker_preview matches 20 run data modify block ~1 1 ~ RecordItem.tag.item set from entity @s Inventory[{Slot:20b}]
execute if score #slot shulker_preview matches 21 run data modify block ~1 1 ~ RecordItem.tag.item set from entity @s Inventory[{Slot:21b}]
execute if score #slot shulker_preview matches 22 run data modify block ~1 1 ~ RecordItem.tag.item set from entity @s Inventory[{Slot:22b}]
execute if score #slot shulker_preview matches 23 run data modify block ~1 1 ~ RecordItem.tag.item set from entity @s Inventory[{Slot:23b}]
execute if score #slot shulker_preview matches 24 run data modify block ~1 1 ~ RecordItem.tag.item set from entity @s Inventory[{Slot:24b}]
execute if score #slot shulker_preview matches 25 run data modify block ~1 1 ~ RecordItem.tag.item set from entity @s Inventory[{Slot:25b}]
execute if score #slot shulker_preview matches 26 run data modify block ~1 1 ~ RecordItem.tag.item set from entity @s Inventory[{Slot:26b}]
execute if score #slot shulker_preview matches 27 run data modify block ~1 1 ~ RecordItem.tag.item set from entity @s Inventory[{Slot:27b}]
execute if score #slot shulker_preview matches 28 run data modify block ~1 1 ~ RecordItem.tag.item set from entity @s Inventory[{Slot:28b}]
execute if score #slot shulker_preview matches 29 run data modify block ~1 1 ~ RecordItem.tag.item set from entity @s Inventory[{Slot:29b}]
execute if score #slot shulker_preview matches 30 run data modify block ~1 1 ~ RecordItem.tag.item set from entity @s Inventory[{Slot:30b}]
execute if score #slot shulker_preview matches 31 run data modify block ~1 1 ~ RecordItem.tag.item set from entity @s Inventory[{Slot:31b}]
execute if score #slot shulker_preview matches 32 run data modify block ~1 1 ~ RecordItem.tag.item set from entity @s Inventory[{Slot:32b}]
execute if score #slot shulker_preview matches 33 run data modify block ~1 1 ~ RecordItem.tag.item set from entity @s Inventory[{Slot:33b}]
execute if score #slot shulker_preview matches 34 run data modify block ~1 1 ~ RecordItem.tag.item set from entity @s Inventory[{Slot:34b}]
execute if score #slot shulker_preview matches 35 run data modify block ~1 1 ~ RecordItem.tag.item set from entity @s Inventory[{Slot:35b}]
execute if score #slot shulker_preview matches -106 run data modify block ~1 1 ~ RecordItem.tag.item set from entity @s Inventory[{Slot:-106b}]

data modify block ~1 1 ~ RecordItem.tag.item.Slot set value 0b
data modify block ~1 1 ~ RecordItem.tag.item.tag.display.Lore set from block ~1 1 ~ RecordItem.tag.display.Lore
data modify block ~ 1 ~ Items[0] set from block ~1 1 ~ RecordItem.tag.item

function tryashtar.shulker_preview:copy_item
data remove block ~1 1 ~ RecordItem.tag.ender_chests[0]
execute store result score #slot shulker_preview store success score #has_slot shulker_preview run data get block ~1 1 ~ RecordItem.tag.ender_chests[0].Slot
execute if score #has_slot shulker_preview matches 1 run function tryashtar.shulker_preview:ender_chest/return_loop
