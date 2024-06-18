# construct an artificial container that has the player's ender chest items
# populate it by copying one item at a time, since serializing player NBT is slow
# we also need an item entity anyway to run the processing and create the tooltip, which will be copied to every ender chest in the player's inventory
data modify storage tryashtar.shulker_preview:data contents set value [{slot:0,item:0b},{slot:1,item:0b},{slot:2,item:0b},{slot:3,item:0b},{slot:4,item:0b},{slot:5,item:0b},{slot:6,item:0b},{slot:7,item:0b},{slot:8,item:0b},{slot:9,item:0b},{slot:10,item:0b},{slot:11,item:0b},{slot:12,item:0b},{slot:13,item:0b},{slot:14,item:0b},{slot:15,item:0b},{slot:16,item:0b},{slot:17,item:0b},{slot:18,item:0b},{slot:19,item:0b},{slot:20,item:0b},{slot:21,item:0b},{slot:22,item:0b},{slot:23,item:0b},{slot:24,item:0b},{slot:25,item:0b},{slot:26,item:0b}]
summon item ~ -10000 ~ {Invulnerable:1b,NoGravity:1b,Silent:1b,UUID:[I;1936225644,1801810464,1886545270,1768257343],Item:{id:"tnt",count:1}}

# it's possible a chest minecart is better here, since it would only be one NBT serialize
# however, the resulting NBT would need some processing to match the container format
# I haven't tested to compare performance!
item replace entity 7368756c-6b65-7220-7072-65766965773f contents from entity @s enderchest.0
data modify storage tryashtar.shulker_preview:data contents[0].item set from entity 7368756c-6b65-7220-7072-65766965773f Item
item replace entity 7368756c-6b65-7220-7072-65766965773f contents from entity @s enderchest.1
data modify storage tryashtar.shulker_preview:data contents[1].item set from entity 7368756c-6b65-7220-7072-65766965773f Item
item replace entity 7368756c-6b65-7220-7072-65766965773f contents from entity @s enderchest.2
data modify storage tryashtar.shulker_preview:data contents[2].item set from entity 7368756c-6b65-7220-7072-65766965773f Item
item replace entity 7368756c-6b65-7220-7072-65766965773f contents from entity @s enderchest.3
data modify storage tryashtar.shulker_preview:data contents[3].item set from entity 7368756c-6b65-7220-7072-65766965773f Item
item replace entity 7368756c-6b65-7220-7072-65766965773f contents from entity @s enderchest.4
data modify storage tryashtar.shulker_preview:data contents[4].item set from entity 7368756c-6b65-7220-7072-65766965773f Item
item replace entity 7368756c-6b65-7220-7072-65766965773f contents from entity @s enderchest.5
data modify storage tryashtar.shulker_preview:data contents[5].item set from entity 7368756c-6b65-7220-7072-65766965773f Item
item replace entity 7368756c-6b65-7220-7072-65766965773f contents from entity @s enderchest.6
data modify storage tryashtar.shulker_preview:data contents[6].item set from entity 7368756c-6b65-7220-7072-65766965773f Item
item replace entity 7368756c-6b65-7220-7072-65766965773f contents from entity @s enderchest.7
data modify storage tryashtar.shulker_preview:data contents[7].item set from entity 7368756c-6b65-7220-7072-65766965773f Item
item replace entity 7368756c-6b65-7220-7072-65766965773f contents from entity @s enderchest.8
data modify storage tryashtar.shulker_preview:data contents[8].item set from entity 7368756c-6b65-7220-7072-65766965773f Item
item replace entity 7368756c-6b65-7220-7072-65766965773f contents from entity @s enderchest.9
data modify storage tryashtar.shulker_preview:data contents[9].item set from entity 7368756c-6b65-7220-7072-65766965773f Item
item replace entity 7368756c-6b65-7220-7072-65766965773f contents from entity @s enderchest.10
data modify storage tryashtar.shulker_preview:data contents[10].item set from entity 7368756c-6b65-7220-7072-65766965773f Item
item replace entity 7368756c-6b65-7220-7072-65766965773f contents from entity @s enderchest.11
data modify storage tryashtar.shulker_preview:data contents[11].item set from entity 7368756c-6b65-7220-7072-65766965773f Item
item replace entity 7368756c-6b65-7220-7072-65766965773f contents from entity @s enderchest.12
data modify storage tryashtar.shulker_preview:data contents[12].item set from entity 7368756c-6b65-7220-7072-65766965773f Item
item replace entity 7368756c-6b65-7220-7072-65766965773f contents from entity @s enderchest.13
data modify storage tryashtar.shulker_preview:data contents[13].item set from entity 7368756c-6b65-7220-7072-65766965773f Item
item replace entity 7368756c-6b65-7220-7072-65766965773f contents from entity @s enderchest.14
data modify storage tryashtar.shulker_preview:data contents[14].item set from entity 7368756c-6b65-7220-7072-65766965773f Item
item replace entity 7368756c-6b65-7220-7072-65766965773f contents from entity @s enderchest.15
data modify storage tryashtar.shulker_preview:data contents[15].item set from entity 7368756c-6b65-7220-7072-65766965773f Item
item replace entity 7368756c-6b65-7220-7072-65766965773f contents from entity @s enderchest.16
data modify storage tryashtar.shulker_preview:data contents[16].item set from entity 7368756c-6b65-7220-7072-65766965773f Item
item replace entity 7368756c-6b65-7220-7072-65766965773f contents from entity @s enderchest.17
data modify storage tryashtar.shulker_preview:data contents[17].item set from entity 7368756c-6b65-7220-7072-65766965773f Item
item replace entity 7368756c-6b65-7220-7072-65766965773f contents from entity @s enderchest.18
data modify storage tryashtar.shulker_preview:data contents[18].item set from entity 7368756c-6b65-7220-7072-65766965773f Item
item replace entity 7368756c-6b65-7220-7072-65766965773f contents from entity @s enderchest.19
data modify storage tryashtar.shulker_preview:data contents[19].item set from entity 7368756c-6b65-7220-7072-65766965773f Item
item replace entity 7368756c-6b65-7220-7072-65766965773f contents from entity @s enderchest.20
data modify storage tryashtar.shulker_preview:data contents[20].item set from entity 7368756c-6b65-7220-7072-65766965773f Item
item replace entity 7368756c-6b65-7220-7072-65766965773f contents from entity @s enderchest.21
data modify storage tryashtar.shulker_preview:data contents[21].item set from entity 7368756c-6b65-7220-7072-65766965773f Item
item replace entity 7368756c-6b65-7220-7072-65766965773f contents from entity @s enderchest.22
data modify storage tryashtar.shulker_preview:data contents[22].item set from entity 7368756c-6b65-7220-7072-65766965773f Item
item replace entity 7368756c-6b65-7220-7072-65766965773f contents from entity @s enderchest.23
data modify storage tryashtar.shulker_preview:data contents[23].item set from entity 7368756c-6b65-7220-7072-65766965773f Item
item replace entity 7368756c-6b65-7220-7072-65766965773f contents from entity @s enderchest.24
data modify storage tryashtar.shulker_preview:data contents[24].item set from entity 7368756c-6b65-7220-7072-65766965773f Item
item replace entity 7368756c-6b65-7220-7072-65766965773f contents from entity @s enderchest.25
data modify storage tryashtar.shulker_preview:data contents[25].item set from entity 7368756c-6b65-7220-7072-65766965773f Item
item replace entity 7368756c-6b65-7220-7072-65766965773f contents from entity @s enderchest.26
data modify storage tryashtar.shulker_preview:data contents[26].item set from entity 7368756c-6b65-7220-7072-65766965773f Item

# remove empty slots, so the "X more..." fallback tooltip is correct
data remove storage tryashtar.shulker_preview:data contents[{item:0b}]

# in the likely case the last ender chest slot is empty, restore a real item so the entity can receive lore
# run the processing and save the lore to be copied identically to every ender chest
item replace entity 7368756c-6b65-7220-7072-65766965773f contents with ender_chest
execute as 7368756c-6b65-7220-7072-65766965773f run function tryashtar.shulker_preview:process
data modify storage tryashtar.shulker_preview:data lore set from entity 7368756c-6b65-7220-7072-65766965773f Item.components."minecraft:lore"
kill 7368756c-6b65-7220-7072-65766965773f

# the tooltip is generated, copy it to every ender chest in the player's inventory
execute if items entity @s hotbar.* ender_chest run function tryashtar.shulker_preview:ender_chest/to_hotbar
execute if items entity @s inventory.* ender_chest run function tryashtar.shulker_preview:ender_chest/to_inventory
execute if items entity @s enderchest.* ender_chest run function tryashtar.shulker_preview:ender_chest/to_enderchest
