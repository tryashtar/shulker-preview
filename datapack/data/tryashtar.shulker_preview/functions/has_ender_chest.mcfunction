# scan each ender chest in inventory to see if it's completely new, has a different UUID (new player), or has a different content length (ender contents changed)
execute store result score #uuid shulker_preview run data get entity @s UUID[0]
execute store result score #contents shulker_preview run data get entity @s EnderItems
scoreboard players set #done shulker_preview 0
data modify block ~ 1 ~ Items set value [{id:tnt,Count:1b}]

scoreboard players set #slot shulker_preview 0
data modify block ~ 1 ~ Items[0].tag.shulker_items set value []
execute if score #done shulker_preview matches 0 store success score #done shulker_preview run data modify block ~ 1 ~ Items[0].tag.shulker_items append from entity @s Inventory[{Slot:0b,id:"minecraft:ender_chest"}]
execute if score #done shulker_preview matches 1 run function tryashtar.shulker_preview:check_ender_chest

scoreboard players set #slot shulker_preview 1
data modify block ~ 1 ~ Items[0].tag.shulker_items set value []
execute if score #done shulker_preview matches 0 store success score #done shulker_preview run data modify block ~ 1 ~ Items[0].tag.shulker_items append from entity @s Inventory[{Slot:1b,id:"minecraft:ender_chest"}]
execute if score #done shulker_preview matches 1 run function tryashtar.shulker_preview:check_ender_chest

scoreboard players set #slot shulker_preview 2
data modify block ~ 1 ~ Items[0].tag.shulker_items set value []
execute if score #done shulker_preview matches 0 store success score #done shulker_preview run data modify block ~ 1 ~ Items[0].tag.shulker_items append from entity @s Inventory[{Slot:2b,id:"minecraft:ender_chest"}]
execute if score #done shulker_preview matches 1 run function tryashtar.shulker_preview:check_ender_chest

scoreboard players set #slot shulker_preview 3
data modify block ~ 1 ~ Items[0].tag.shulker_items set value []
execute if score #done shulker_preview matches 0 store success score #done shulker_preview run data modify block ~ 1 ~ Items[0].tag.shulker_items append from entity @s Inventory[{Slot:3b,id:"minecraft:ender_chest"}]
execute if score #done shulker_preview matches 1 run function tryashtar.shulker_preview:check_ender_chest

scoreboard players set #slot shulker_preview 4
data modify block ~ 1 ~ Items[0].tag.shulker_items set value []
execute if score #done shulker_preview matches 0 store success score #done shulker_preview run data modify block ~ 1 ~ Items[0].tag.shulker_items append from entity @s Inventory[{Slot:4b,id:"minecraft:ender_chest"}]
execute if score #done shulker_preview matches 1 run function tryashtar.shulker_preview:check_ender_chest

scoreboard players set #slot shulker_preview 5
data modify block ~ 1 ~ Items[0].tag.shulker_items set value []
execute if score #done shulker_preview matches 0 store success score #done shulker_preview run data modify block ~ 1 ~ Items[0].tag.shulker_items append from entity @s Inventory[{Slot:5b,id:"minecraft:ender_chest"}]
execute if score #done shulker_preview matches 1 run function tryashtar.shulker_preview:check_ender_chest

scoreboard players set #slot shulker_preview 6
data modify block ~ 1 ~ Items[0].tag.shulker_items set value []
execute if score #done shulker_preview matches 0 store success score #done shulker_preview run data modify block ~ 1 ~ Items[0].tag.shulker_items append from entity @s Inventory[{Slot:6b,id:"minecraft:ender_chest"}]
execute if score #done shulker_preview matches 1 run function tryashtar.shulker_preview:check_ender_chest

scoreboard players set #slot shulker_preview 7
data modify block ~ 1 ~ Items[0].tag.shulker_items set value []
execute if score #done shulker_preview matches 0 store success score #done shulker_preview run data modify block ~ 1 ~ Items[0].tag.shulker_items append from entity @s Inventory[{Slot:7b,id:"minecraft:ender_chest"}]
execute if score #done shulker_preview matches 1 run function tryashtar.shulker_preview:check_ender_chest

scoreboard players set #slot shulker_preview 8
data modify block ~ 1 ~ Items[0].tag.shulker_items set value []
execute if score #done shulker_preview matches 0 store success score #done shulker_preview run data modify block ~ 1 ~ Items[0].tag.shulker_items append from entity @s Inventory[{Slot:8b,id:"minecraft:ender_chest"}]
execute if score #done shulker_preview matches 1 run function tryashtar.shulker_preview:check_ender_chest

scoreboard players set #slot shulker_preview 9
data modify block ~ 1 ~ Items[0].tag.shulker_items set value []
execute if score #done shulker_preview matches 0 store success score #done shulker_preview run data modify block ~ 1 ~ Items[0].tag.shulker_items append from entity @s Inventory[{Slot:9b,id:"minecraft:ender_chest"}]
execute if score #done shulker_preview matches 1 run function tryashtar.shulker_preview:check_ender_chest

scoreboard players set #slot shulker_preview 10
data modify block ~ 1 ~ Items[0].tag.shulker_items set value []
execute if score #done shulker_preview matches 0 store success score #done shulker_preview run data modify block ~ 1 ~ Items[0].tag.shulker_items append from entity @s Inventory[{Slot:10b,id:"minecraft:ender_chest"}]
execute if score #done shulker_preview matches 1 run function tryashtar.shulker_preview:check_ender_chest

scoreboard players set #slot shulker_preview 11
data modify block ~ 1 ~ Items[0].tag.shulker_items set value []
execute if score #done shulker_preview matches 0 store success score #done shulker_preview run data modify block ~ 1 ~ Items[0].tag.shulker_items append from entity @s Inventory[{Slot:11b,id:"minecraft:ender_chest"}]
execute if score #done shulker_preview matches 1 run function tryashtar.shulker_preview:check_ender_chest

scoreboard players set #slot shulker_preview 12
data modify block ~ 1 ~ Items[0].tag.shulker_items set value []
execute if score #done shulker_preview matches 0 store success score #done shulker_preview run data modify block ~ 1 ~ Items[0].tag.shulker_items append from entity @s Inventory[{Slot:12b,id:"minecraft:ender_chest"}]
execute if score #done shulker_preview matches 1 run function tryashtar.shulker_preview:check_ender_chest

scoreboard players set #slot shulker_preview 13
data modify block ~ 1 ~ Items[0].tag.shulker_items set value []
execute if score #done shulker_preview matches 0 store success score #done shulker_preview run data modify block ~ 1 ~ Items[0].tag.shulker_items append from entity @s Inventory[{Slot:13b,id:"minecraft:ender_chest"}]
execute if score #done shulker_preview matches 1 run function tryashtar.shulker_preview:check_ender_chest

scoreboard players set #slot shulker_preview 14
data modify block ~ 1 ~ Items[0].tag.shulker_items set value []
execute if score #done shulker_preview matches 0 store success score #done shulker_preview run data modify block ~ 1 ~ Items[0].tag.shulker_items append from entity @s Inventory[{Slot:14b,id:"minecraft:ender_chest"}]
execute if score #done shulker_preview matches 1 run function tryashtar.shulker_preview:check_ender_chest

scoreboard players set #slot shulker_preview 15
data modify block ~ 1 ~ Items[0].tag.shulker_items set value []
execute if score #done shulker_preview matches 0 store success score #done shulker_preview run data modify block ~ 1 ~ Items[0].tag.shulker_items append from entity @s Inventory[{Slot:15b,id:"minecraft:ender_chest"}]
execute if score #done shulker_preview matches 1 run function tryashtar.shulker_preview:check_ender_chest

scoreboard players set #slot shulker_preview 16
data modify block ~ 1 ~ Items[0].tag.shulker_items set value []
execute if score #done shulker_preview matches 0 store success score #done shulker_preview run data modify block ~ 1 ~ Items[0].tag.shulker_items append from entity @s Inventory[{Slot:16b,id:"minecraft:ender_chest"}]
execute if score #done shulker_preview matches 1 run function tryashtar.shulker_preview:check_ender_chest

scoreboard players set #slot shulker_preview 17
data modify block ~ 1 ~ Items[0].tag.shulker_items set value []
execute if score #done shulker_preview matches 0 store success score #done shulker_preview run data modify block ~ 1 ~ Items[0].tag.shulker_items append from entity @s Inventory[{Slot:17b,id:"minecraft:ender_chest"}]
execute if score #done shulker_preview matches 1 run function tryashtar.shulker_preview:check_ender_chest

scoreboard players set #slot shulker_preview 18
data modify block ~ 1 ~ Items[0].tag.shulker_items set value []
execute if score #done shulker_preview matches 0 store success score #done shulker_preview run data modify block ~ 1 ~ Items[0].tag.shulker_items append from entity @s Inventory[{Slot:18b,id:"minecraft:ender_chest"}]
execute if score #done shulker_preview matches 1 run function tryashtar.shulker_preview:check_ender_chest

scoreboard players set #slot shulker_preview 19
data modify block ~ 1 ~ Items[0].tag.shulker_items set value []
execute if score #done shulker_preview matches 0 store success score #done shulker_preview run data modify block ~ 1 ~ Items[0].tag.shulker_items append from entity @s Inventory[{Slot:19b,id:"minecraft:ender_chest"}]
execute if score #done shulker_preview matches 1 run function tryashtar.shulker_preview:check_ender_chest

scoreboard players set #slot shulker_preview 20
data modify block ~ 1 ~ Items[0].tag.shulker_items set value []
execute if score #done shulker_preview matches 0 store success score #done shulker_preview run data modify block ~ 1 ~ Items[0].tag.shulker_items append from entity @s Inventory[{Slot:20b,id:"minecraft:ender_chest"}]
execute if score #done shulker_preview matches 1 run function tryashtar.shulker_preview:check_ender_chest

scoreboard players set #slot shulker_preview 21
data modify block ~ 1 ~ Items[0].tag.shulker_items set value []
execute if score #done shulker_preview matches 0 store success score #done shulker_preview run data modify block ~ 1 ~ Items[0].tag.shulker_items append from entity @s Inventory[{Slot:21b,id:"minecraft:ender_chest"}]
execute if score #done shulker_preview matches 1 run function tryashtar.shulker_preview:check_ender_chest

scoreboard players set #slot shulker_preview 22
data modify block ~ 1 ~ Items[0].tag.shulker_items set value []
execute if score #done shulker_preview matches 0 store success score #done shulker_preview run data modify block ~ 1 ~ Items[0].tag.shulker_items append from entity @s Inventory[{Slot:22b,id:"minecraft:ender_chest"}]
execute if score #done shulker_preview matches 1 run function tryashtar.shulker_preview:check_ender_chest

scoreboard players set #slot shulker_preview 23
data modify block ~ 1 ~ Items[0].tag.shulker_items set value []
execute if score #done shulker_preview matches 0 store success score #done shulker_preview run data modify block ~ 1 ~ Items[0].tag.shulker_items append from entity @s Inventory[{Slot:23b,id:"minecraft:ender_chest"}]
execute if score #done shulker_preview matches 1 run function tryashtar.shulker_preview:check_ender_chest

scoreboard players set #slot shulker_preview 24
data modify block ~ 1 ~ Items[0].tag.shulker_items set value []
execute if score #done shulker_preview matches 0 store success score #done shulker_preview run data modify block ~ 1 ~ Items[0].tag.shulker_items append from entity @s Inventory[{Slot:24b,id:"minecraft:ender_chest"}]
execute if score #done shulker_preview matches 1 run function tryashtar.shulker_preview:check_ender_chest

scoreboard players set #slot shulker_preview 25
data modify block ~ 1 ~ Items[0].tag.shulker_items set value []
execute if score #done shulker_preview matches 0 store success score #done shulker_preview run data modify block ~ 1 ~ Items[0].tag.shulker_items append from entity @s Inventory[{Slot:25b,id:"minecraft:ender_chest"}]
execute if score #done shulker_preview matches 1 run function tryashtar.shulker_preview:check_ender_chest

scoreboard players set #slot shulker_preview 26
data modify block ~ 1 ~ Items[0].tag.shulker_items set value []
execute if score #done shulker_preview matches 0 store success score #done shulker_preview run data modify block ~ 1 ~ Items[0].tag.shulker_items append from entity @s Inventory[{Slot:26b,id:"minecraft:ender_chest"}]
execute if score #done shulker_preview matches 1 run function tryashtar.shulker_preview:check_ender_chest

scoreboard players set #slot shulker_preview 27
data modify block ~ 1 ~ Items[0].tag.shulker_items set value []
execute if score #done shulker_preview matches 0 store success score #done shulker_preview run data modify block ~ 1 ~ Items[0].tag.shulker_items append from entity @s Inventory[{Slot:27b,id:"minecraft:ender_chest"}]
execute if score #done shulker_preview matches 1 run function tryashtar.shulker_preview:check_ender_chest

scoreboard players set #slot shulker_preview 28
data modify block ~ 1 ~ Items[0].tag.shulker_items set value []
execute if score #done shulker_preview matches 0 store success score #done shulker_preview run data modify block ~ 1 ~ Items[0].tag.shulker_items append from entity @s Inventory[{Slot:28b,id:"minecraft:ender_chest"}]
execute if score #done shulker_preview matches 1 run function tryashtar.shulker_preview:check_ender_chest

scoreboard players set #slot shulker_preview 29
data modify block ~ 1 ~ Items[0].tag.shulker_items set value []
execute if score #done shulker_preview matches 0 store success score #done shulker_preview run data modify block ~ 1 ~ Items[0].tag.shulker_items append from entity @s Inventory[{Slot:29b,id:"minecraft:ender_chest"}]
execute if score #done shulker_preview matches 1 run function tryashtar.shulker_preview:check_ender_chest

scoreboard players set #slot shulker_preview 30
data modify block ~ 1 ~ Items[0].tag.shulker_items set value []
execute if score #done shulker_preview matches 0 store success score #done shulker_preview run data modify block ~ 1 ~ Items[0].tag.shulker_items append from entity @s Inventory[{Slot:30b,id:"minecraft:ender_chest"}]
execute if score #done shulker_preview matches 1 run function tryashtar.shulker_preview:check_ender_chest

scoreboard players set #slot shulker_preview 31
data modify block ~ 1 ~ Items[0].tag.shulker_items set value []
execute if score #done shulker_preview matches 0 store success score #done shulker_preview run data modify block ~ 1 ~ Items[0].tag.shulker_items append from entity @s Inventory[{Slot:31b,id:"minecraft:ender_chest"}]
execute if score #done shulker_preview matches 1 run function tryashtar.shulker_preview:check_ender_chest

scoreboard players set #slot shulker_preview 32
data modify block ~ 1 ~ Items[0].tag.shulker_items set value []
execute if score #done shulker_preview matches 0 store success score #done shulker_preview run data modify block ~ 1 ~ Items[0].tag.shulker_items append from entity @s Inventory[{Slot:32b,id:"minecraft:ender_chest"}]
execute if score #done shulker_preview matches 1 run function tryashtar.shulker_preview:check_ender_chest

scoreboard players set #slot shulker_preview 33
data modify block ~ 1 ~ Items[0].tag.shulker_items set value []
execute if score #done shulker_preview matches 0 store success score #done shulker_preview run data modify block ~ 1 ~ Items[0].tag.shulker_items append from entity @s Inventory[{Slot:33b,id:"minecraft:ender_chest"}]
execute if score #done shulker_preview matches 1 run function tryashtar.shulker_preview:check_ender_chest

scoreboard players set #slot shulker_preview 34
data modify block ~ 1 ~ Items[0].tag.shulker_items set value []
execute if score #done shulker_preview matches 0 store success score #done shulker_preview run data modify block ~ 1 ~ Items[0].tag.shulker_items append from entity @s Inventory[{Slot:34b,id:"minecraft:ender_chest"}]
execute if score #done shulker_preview matches 1 run function tryashtar.shulker_preview:check_ender_chest

scoreboard players set #slot shulker_preview 35
data modify block ~ 1 ~ Items[0].tag.shulker_items set value []
execute if score #done shulker_preview matches 0 store success score #done shulker_preview run data modify block ~ 1 ~ Items[0].tag.shulker_items append from entity @s Inventory[{Slot:35b,id:"minecraft:ender_chest"}]
execute if score #done shulker_preview matches 1 run function tryashtar.shulker_preview:check_ender_chest

scoreboard players set #slot shulker_preview -106
data modify block ~ 1 ~ Items[0].tag.shulker_items set value []
execute if score #done shulker_preview matches 0 store success score #done shulker_preview run data modify block ~ 1 ~ Items[0].tag.shulker_items append from entity @s Inventory[{Slot:-106b,id:"minecraft:ender_chest"}]
execute if score #done shulker_preview matches 1 run function tryashtar.shulker_preview:check_ender_chest

execute if score #done shulker_preview matches 0 run tag @s remove shulker_preview.ender_chest
