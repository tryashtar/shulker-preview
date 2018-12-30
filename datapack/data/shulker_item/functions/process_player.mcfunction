data remove block ~ ~ ~ Items
data modify block ~ ~ ~ Items append from entity @s Inventory[{Slot:0b}]
data modify block ~ ~ ~ Items append from entity @s Inventory[{Slot:1b}]
data modify block ~ ~ ~ Items append from entity @s Inventory[{Slot:2b}]
data modify block ~ ~ ~ Items append from entity @s Inventory[{Slot:3b}]
data modify block ~ ~ ~ Items append from entity @s Inventory[{Slot:4b}]
data modify block ~ ~ ~ Items append from entity @s Inventory[{Slot:5b}]
data modify block ~ ~ ~ Items append from entity @s Inventory[{Slot:6b}]
data modify block ~ ~ ~ Items append from entity @s Inventory[{Slot:7b}]
data modify block ~ ~ ~ Items append from entity @s Inventory[{Slot:8b}]
data modify block ~ ~ ~ Items append from entity @s Inventory[{Slot:9b}]
data modify block ~ ~ ~ Items append from entity @s Inventory[{Slot:10b}]
data modify block ~ ~ ~ Items append from entity @s Inventory[{Slot:11b}]
data modify block ~ ~ ~ Items append from entity @s Inventory[{Slot:12b}]
data modify block ~ ~ ~ Items append from entity @s Inventory[{Slot:13b}]
data modify block ~ ~ ~ Items append from entity @s Inventory[{Slot:14b}]
data modify block ~ ~ ~ Items append from entity @s Inventory[{Slot:15b}]
data modify block ~ ~ ~ Items append from entity @s Inventory[{Slot:16b}]
data modify block ~ ~ ~ Items append from entity @s Inventory[{Slot:17b}]
data modify block ~ ~ ~ Items append from entity @s Inventory[{Slot:18b}]
data modify block ~ ~ ~ Items append from entity @s Inventory[{Slot:19b}]
data modify block ~ ~ ~ Items append from entity @s Inventory[{Slot:20b}]
data modify block ~ ~ ~ Items append from entity @s Inventory[{Slot:21b}]
data modify block ~ ~ ~ Items append from entity @s Inventory[{Slot:22b}]
data modify block ~ ~ ~ Items append from entity @s Inventory[{Slot:23b}]
data modify block ~ ~ ~ Items append from entity @s Inventory[{Slot:24b}]
data modify block ~ ~ ~ Items append from entity @s Inventory[{Slot:25b}]
data modify block ~ ~ ~ Items append from entity @s Inventory[{Slot:26b}]

execute if data block ~ ~ ~ Items[{Slot:0b,id:"minecraft:shulker_box"}] unless data block ~ ~ ~ Items[{Slot:0b,tag:{shulker_processed:1b}}] run function shulker_item:process_box/0
execute if data block ~ ~ ~ Items[{Slot:1b,id:"minecraft:shulker_box"}] unless data block ~ ~ ~ Items[{Slot:1b,tag:{shulker_processed:1b}}] run function shulker_item:process_box/1
execute if data block ~ ~ ~ Items[{Slot:2b,id:"minecraft:shulker_box"}] unless data block ~ ~ ~ Items[{Slot:2b,tag:{shulker_processed:1b}}] run function shulker_item:process_box/2
execute if data block ~ ~ ~ Items[{Slot:3b,id:"minecraft:shulker_box"}] unless data block ~ ~ ~ Items[{Slot:3b,tag:{shulker_processed:1b}}] run function shulker_item:process_box/3
execute if data block ~ ~ ~ Items[{Slot:4b,id:"minecraft:shulker_box"}] unless data block ~ ~ ~ Items[{Slot:4b,tag:{shulker_processed:1b}}] run function shulker_item:process_box/4
execute if data block ~ ~ ~ Items[{Slot:5b,id:"minecraft:shulker_box"}] unless data block ~ ~ ~ Items[{Slot:5b,tag:{shulker_processed:1b}}] run function shulker_item:process_box/5
execute if data block ~ ~ ~ Items[{Slot:6b,id:"minecraft:shulker_box"}] unless data block ~ ~ ~ Items[{Slot:6b,tag:{shulker_processed:1b}}] run function shulker_item:process_box/6
execute if data block ~ ~ ~ Items[{Slot:7b,id:"minecraft:shulker_box"}] unless data block ~ ~ ~ Items[{Slot:7b,tag:{shulker_processed:1b}}] run function shulker_item:process_box/7
execute if data block ~ ~ ~ Items[{Slot:8b,id:"minecraft:shulker_box"}] unless data block ~ ~ ~ Items[{Slot:8b,tag:{shulker_processed:1b}}] run function shulker_item:process_box/8
execute if data block ~ ~ ~ Items[{Slot:9b,id:"minecraft:shulker_box"}] unless data block ~ ~ ~ Items[{Slot:9b,tag:{shulker_processed:1b}}] run function shulker_item:process_box/9
execute if data block ~ ~ ~ Items[{Slot:10b,id:"minecraft:shulker_box"}] unless data block ~ ~ ~ Items[{Slot:10b,tag:{shulker_processed:1b}}] run function shulker_item:process_box/10
execute if data block ~ ~ ~ Items[{Slot:11b,id:"minecraft:shulker_box"}] unless data block ~ ~ ~ Items[{Slot:11b,tag:{shulker_processed:1b}}] run function shulker_item:process_box/11
execute if data block ~ ~ ~ Items[{Slot:12b,id:"minecraft:shulker_box"}] unless data block ~ ~ ~ Items[{Slot:12b,tag:{shulker_processed:1b}}] run function shulker_item:process_box/12
execute if data block ~ ~ ~ Items[{Slot:13b,id:"minecraft:shulker_box"}] unless data block ~ ~ ~ Items[{Slot:13b,tag:{shulker_processed:1b}}] run function shulker_item:process_box/13
execute if data block ~ ~ ~ Items[{Slot:14b,id:"minecraft:shulker_box"}] unless data block ~ ~ ~ Items[{Slot:14b,tag:{shulker_processed:1b}}] run function shulker_item:process_box/14
execute if data block ~ ~ ~ Items[{Slot:15b,id:"minecraft:shulker_box"}] unless data block ~ ~ ~ Items[{Slot:15b,tag:{shulker_processed:1b}}] run function shulker_item:process_box/15
execute if data block ~ ~ ~ Items[{Slot:16b,id:"minecraft:shulker_box"}] unless data block ~ ~ ~ Items[{Slot:16b,tag:{shulker_processed:1b}}] run function shulker_item:process_box/16
execute if data block ~ ~ ~ Items[{Slot:17b,id:"minecraft:shulker_box"}] unless data block ~ ~ ~ Items[{Slot:17b,tag:{shulker_processed:1b}}] run function shulker_item:process_box/17
execute if data block ~ ~ ~ Items[{Slot:18b,id:"minecraft:shulker_box"}] unless data block ~ ~ ~ Items[{Slot:18b,tag:{shulker_processed:1b}}] run function shulker_item:process_box/18
execute if data block ~ ~ ~ Items[{Slot:19b,id:"minecraft:shulker_box"}] unless data block ~ ~ ~ Items[{Slot:19b,tag:{shulker_processed:1b}}] run function shulker_item:process_box/19
execute if data block ~ ~ ~ Items[{Slot:20b,id:"minecraft:shulker_box"}] unless data block ~ ~ ~ Items[{Slot:20b,tag:{shulker_processed:1b}}] run function shulker_item:process_box/20
execute if data block ~ ~ ~ Items[{Slot:21b,id:"minecraft:shulker_box"}] unless data block ~ ~ ~ Items[{Slot:21b,tag:{shulker_processed:1b}}] run function shulker_item:process_box/21
execute if data block ~ ~ ~ Items[{Slot:22b,id:"minecraft:shulker_box"}] unless data block ~ ~ ~ Items[{Slot:22b,tag:{shulker_processed:1b}}] run function shulker_item:process_box/22
execute if data block ~ ~ ~ Items[{Slot:23b,id:"minecraft:shulker_box"}] unless data block ~ ~ ~ Items[{Slot:23b,tag:{shulker_processed:1b}}] run function shulker_item:process_box/23
execute if data block ~ ~ ~ Items[{Slot:24b,id:"minecraft:shulker_box"}] unless data block ~ ~ ~ Items[{Slot:24b,tag:{shulker_processed:1b}}] run function shulker_item:process_box/24
execute if data block ~ ~ ~ Items[{Slot:25b,id:"minecraft:shulker_box"}] unless data block ~ ~ ~ Items[{Slot:25b,tag:{shulker_processed:1b}}] run function shulker_item:process_box/25
execute if data block ~ ~ ~ Items[{Slot:26b,id:"minecraft:shulker_box"}] unless data block ~ ~ ~ Items[{Slot:26b,tag:{shulker_processed:1b}}] run function shulker_item:process_box/26

loot replace entity @s hotbar.0 27 mine ~ ~ ~ golden_pickaxe{drop_contents:true}
