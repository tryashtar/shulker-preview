# summon tooltip background
execute if data storage tryashtar:shulker_preview items[0].tag.display.Name run summon area_effect_cloud ~ 1 ~ {Tags:["tryashtar.shulker_preview"],CustomName:'{"translate":"tryashtar.shulker_preview.shulker_tooltip"}'}
execute if score #header_type shulker_preview matches 0 unless data storage tryashtar:shulker_preview items[0].tag.display.Name run summon area_effect_cloud ~ 1 ~ {Tags:["tryashtar.shulker_preview"],CustomName:'{"translate":"tryashtar.shulker_preview.shulker_tooltip_header"}'}
execute if score #header_type shulker_preview matches 1 unless data storage tryashtar:shulker_preview items[0].tag.display.Name run summon area_effect_cloud ~ 1 ~ {Tags:["tryashtar.shulker_preview"],CustomName:'{"translate":"tryashtar.shulker_preview.ender_tooltip"}'}
execute if score #header_type shulker_preview matches 2 unless data storage tryashtar:shulker_preview items[0].tag.display.Name run summon area_effect_cloud ~ 1 ~ {Tags:["tryashtar.shulker_preview"],CustomName:'{"translate":"tryashtar.shulker_preview.bundle_tooltip"}'}

# copy and analyze contents one by one
data modify storage tryashtar:shulker_preview item set from storage tryashtar:shulker_preview contents[{Slot:0b}]
execute if data storage tryashtar:shulker_preview contents[{Slot:0b}] positioned ~ 2 ~ run function tryashtar.shulker_preview:row_0/process_item
execute unless data storage tryashtar:shulker_preview contents[{Slot:0b}] run summon area_effect_cloud ~ 2 ~ {Tags:["tryashtar.shulker_preview"],CustomName:'{"translate":"tryashtar.shulker_preview.empty_slot"}'}

data modify storage tryashtar:shulker_preview item set from storage tryashtar:shulker_preview contents[{Slot:1b}]
execute if data storage tryashtar:shulker_preview contents[{Slot:1b}] positioned ~ 3 ~ run function tryashtar.shulker_preview:row_0/process_item
execute unless data storage tryashtar:shulker_preview contents[{Slot:1b}] run summon area_effect_cloud ~ 3 ~ {Tags:["tryashtar.shulker_preview"],CustomName:'{"translate":"tryashtar.shulker_preview.empty_slot"}'}

data modify storage tryashtar:shulker_preview item set from storage tryashtar:shulker_preview contents[{Slot:2b}]
execute if data storage tryashtar:shulker_preview contents[{Slot:2b}] positioned ~ 4 ~ run function tryashtar.shulker_preview:row_0/process_item
execute unless data storage tryashtar:shulker_preview contents[{Slot:2b}] run summon area_effect_cloud ~ 4 ~ {Tags:["tryashtar.shulker_preview"],CustomName:'{"translate":"tryashtar.shulker_preview.empty_slot"}'}

data modify storage tryashtar:shulker_preview item set from storage tryashtar:shulker_preview contents[{Slot:3b}]
execute if data storage tryashtar:shulker_preview contents[{Slot:3b}] positioned ~ 5 ~ run function tryashtar.shulker_preview:row_0/process_item
execute unless data storage tryashtar:shulker_preview contents[{Slot:3b}] run summon area_effect_cloud ~ 5 ~ {Tags:["tryashtar.shulker_preview"],CustomName:'{"translate":"tryashtar.shulker_preview.empty_slot"}'}

data modify storage tryashtar:shulker_preview item set from storage tryashtar:shulker_preview contents[{Slot:4b}]
execute if data storage tryashtar:shulker_preview contents[{Slot:4b}] positioned ~ 6 ~ run function tryashtar.shulker_preview:row_0/process_item
execute unless data storage tryashtar:shulker_preview contents[{Slot:4b}] run summon area_effect_cloud ~ 6 ~ {Tags:["tryashtar.shulker_preview"],CustomName:'{"translate":"tryashtar.shulker_preview.empty_slot"}'}

data modify storage tryashtar:shulker_preview item set from storage tryashtar:shulker_preview contents[{Slot:5b}]
execute if data storage tryashtar:shulker_preview contents[{Slot:5b}] positioned ~ 7 ~ run function tryashtar.shulker_preview:row_0/process_item
execute unless data storage tryashtar:shulker_preview contents[{Slot:5b}] run summon area_effect_cloud ~ 7 ~ {Tags:["tryashtar.shulker_preview"],CustomName:'{"translate":"tryashtar.shulker_preview.empty_slot"}'}

data modify storage tryashtar:shulker_preview item set from storage tryashtar:shulker_preview contents[{Slot:6b}]
execute if data storage tryashtar:shulker_preview contents[{Slot:6b}] positioned ~ 8 ~ run function tryashtar.shulker_preview:row_0/process_item
execute unless data storage tryashtar:shulker_preview contents[{Slot:6b}] run summon area_effect_cloud ~ 8 ~ {Tags:["tryashtar.shulker_preview"],CustomName:'{"translate":"tryashtar.shulker_preview.empty_slot"}'}

data modify storage tryashtar:shulker_preview item set from storage tryashtar:shulker_preview contents[{Slot:7b}]
execute if data storage tryashtar:shulker_preview contents[{Slot:7b}] positioned ~ 9 ~ run function tryashtar.shulker_preview:row_0/process_item
execute unless data storage tryashtar:shulker_preview contents[{Slot:7b}] run summon area_effect_cloud ~ 9 ~ {Tags:["tryashtar.shulker_preview"],CustomName:'{"translate":"tryashtar.shulker_preview.empty_slot"}'}

data modify storage tryashtar:shulker_preview item set from storage tryashtar:shulker_preview contents[{Slot:8b}]
execute if data storage tryashtar:shulker_preview contents[{Slot:8b}] positioned ~ 10 ~ run function tryashtar.shulker_preview:row_0/process_item
execute unless data storage tryashtar:shulker_preview contents[{Slot:8b}] run summon area_effect_cloud ~ 10 ~ {Tags:["tryashtar.shulker_preview"],CustomName:'{"translate":"tryashtar.shulker_preview.empty_slot"}'}

data modify storage tryashtar:shulker_preview item set from storage tryashtar:shulker_preview contents[{Slot:9b}]
execute if data storage tryashtar:shulker_preview contents[{Slot:9b}] positioned ~ 11 ~ run function tryashtar.shulker_preview:row_1/process_item
execute unless data storage tryashtar:shulker_preview contents[{Slot:9b}] run summon area_effect_cloud ~ 11 ~ {Tags:["tryashtar.shulker_preview"],CustomName:'{"translate":"tryashtar.shulker_preview.empty_slot"}'}

data modify storage tryashtar:shulker_preview item set from storage tryashtar:shulker_preview contents[{Slot:10b}]
execute if data storage tryashtar:shulker_preview contents[{Slot:10b}] positioned ~ 12 ~ run function tryashtar.shulker_preview:row_1/process_item
execute unless data storage tryashtar:shulker_preview contents[{Slot:10b}] run summon area_effect_cloud ~ 12 ~ {Tags:["tryashtar.shulker_preview"],CustomName:'{"translate":"tryashtar.shulker_preview.empty_slot"}'}

data modify storage tryashtar:shulker_preview item set from storage tryashtar:shulker_preview contents[{Slot:11b}]
execute if data storage tryashtar:shulker_preview contents[{Slot:11b}] positioned ~ 13 ~ run function tryashtar.shulker_preview:row_1/process_item
execute unless data storage tryashtar:shulker_preview contents[{Slot:11b}] run summon area_effect_cloud ~ 13 ~ {Tags:["tryashtar.shulker_preview"],CustomName:'{"translate":"tryashtar.shulker_preview.empty_slot"}'}

data modify storage tryashtar:shulker_preview item set from storage tryashtar:shulker_preview contents[{Slot:12b}]
execute if data storage tryashtar:shulker_preview contents[{Slot:12b}] positioned ~ 14 ~ run function tryashtar.shulker_preview:row_1/process_item
execute unless data storage tryashtar:shulker_preview contents[{Slot:12b}] run summon area_effect_cloud ~ 14 ~ {Tags:["tryashtar.shulker_preview"],CustomName:'{"translate":"tryashtar.shulker_preview.empty_slot"}'}

data modify storage tryashtar:shulker_preview item set from storage tryashtar:shulker_preview contents[{Slot:13b}]
execute if data storage tryashtar:shulker_preview contents[{Slot:13b}] positioned ~ 15 ~ run function tryashtar.shulker_preview:row_1/process_item
execute unless data storage tryashtar:shulker_preview contents[{Slot:13b}] run summon area_effect_cloud ~ 15 ~ {Tags:["tryashtar.shulker_preview"],CustomName:'{"translate":"tryashtar.shulker_preview.empty_slot"}'}

data modify storage tryashtar:shulker_preview item set from storage tryashtar:shulker_preview contents[{Slot:14b}]
execute if data storage tryashtar:shulker_preview contents[{Slot:14b}] positioned ~ 16 ~ run function tryashtar.shulker_preview:row_1/process_item
execute unless data storage tryashtar:shulker_preview contents[{Slot:14b}] run summon area_effect_cloud ~ 16 ~ {Tags:["tryashtar.shulker_preview"],CustomName:'{"translate":"tryashtar.shulker_preview.empty_slot"}'}

data modify storage tryashtar:shulker_preview item set from storage tryashtar:shulker_preview contents[{Slot:15b}]
execute if data storage tryashtar:shulker_preview contents[{Slot:15b}] positioned ~ 17 ~ run function tryashtar.shulker_preview:row_1/process_item
execute unless data storage tryashtar:shulker_preview contents[{Slot:15b}] run summon area_effect_cloud ~ 17 ~ {Tags:["tryashtar.shulker_preview"],CustomName:'{"translate":"tryashtar.shulker_preview.empty_slot"}'}

data modify storage tryashtar:shulker_preview item set from storage tryashtar:shulker_preview contents[{Slot:16b}]
execute if data storage tryashtar:shulker_preview contents[{Slot:16b}] positioned ~ 18 ~ run function tryashtar.shulker_preview:row_1/process_item
execute unless data storage tryashtar:shulker_preview contents[{Slot:16b}] run summon area_effect_cloud ~ 18 ~ {Tags:["tryashtar.shulker_preview"],CustomName:'{"translate":"tryashtar.shulker_preview.empty_slot"}'}

data modify storage tryashtar:shulker_preview item set from storage tryashtar:shulker_preview contents[{Slot:17b}]
execute if data storage tryashtar:shulker_preview contents[{Slot:17b}] positioned ~ 19 ~ run function tryashtar.shulker_preview:row_1/process_item
execute unless data storage tryashtar:shulker_preview contents[{Slot:17b}] run summon area_effect_cloud ~ 19 ~ {Tags:["tryashtar.shulker_preview"],CustomName:'{"translate":"tryashtar.shulker_preview.empty_slot"}'}

data modify storage tryashtar:shulker_preview item set from storage tryashtar:shulker_preview contents[{Slot:18b}]
execute if data storage tryashtar:shulker_preview contents[{Slot:18b}] positioned ~ 20 ~ run function tryashtar.shulker_preview:row_2/process_item
execute unless data storage tryashtar:shulker_preview contents[{Slot:18b}] run summon area_effect_cloud ~ 20 ~ {Tags:["tryashtar.shulker_preview"],CustomName:'{"translate":"tryashtar.shulker_preview.empty_slot"}'}

data modify storage tryashtar:shulker_preview item set from storage tryashtar:shulker_preview contents[{Slot:19b}]
execute if data storage tryashtar:shulker_preview contents[{Slot:19b}] positioned ~ 21 ~ run function tryashtar.shulker_preview:row_2/process_item
execute unless data storage tryashtar:shulker_preview contents[{Slot:19b}] run summon area_effect_cloud ~ 21 ~ {Tags:["tryashtar.shulker_preview"],CustomName:'{"translate":"tryashtar.shulker_preview.empty_slot"}'}

data modify storage tryashtar:shulker_preview item set from storage tryashtar:shulker_preview contents[{Slot:20b}]
execute if data storage tryashtar:shulker_preview contents[{Slot:20b}] positioned ~ 22 ~ run function tryashtar.shulker_preview:row_2/process_item
execute unless data storage tryashtar:shulker_preview contents[{Slot:20b}] run summon area_effect_cloud ~ 22 ~ {Tags:["tryashtar.shulker_preview"],CustomName:'{"translate":"tryashtar.shulker_preview.empty_slot"}'}

data modify storage tryashtar:shulker_preview item set from storage tryashtar:shulker_preview contents[{Slot:21b}]
execute if data storage tryashtar:shulker_preview contents[{Slot:21b}] positioned ~ 23 ~ run function tryashtar.shulker_preview:row_2/process_item
execute unless data storage tryashtar:shulker_preview contents[{Slot:21b}] run summon area_effect_cloud ~ 23 ~ {Tags:["tryashtar.shulker_preview"],CustomName:'{"translate":"tryashtar.shulker_preview.empty_slot"}'}

data modify storage tryashtar:shulker_preview item set from storage tryashtar:shulker_preview contents[{Slot:22b}]
execute if data storage tryashtar:shulker_preview contents[{Slot:22b}] positioned ~ 24 ~ run function tryashtar.shulker_preview:row_2/process_item
execute unless data storage tryashtar:shulker_preview contents[{Slot:22b}] run summon area_effect_cloud ~ 24 ~ {Tags:["tryashtar.shulker_preview"],CustomName:'{"translate":"tryashtar.shulker_preview.empty_slot"}'}

data modify storage tryashtar:shulker_preview item set from storage tryashtar:shulker_preview contents[{Slot:23b}]
execute if data storage tryashtar:shulker_preview contents[{Slot:23b}] positioned ~ 25 ~ run function tryashtar.shulker_preview:row_2/process_item
execute unless data storage tryashtar:shulker_preview contents[{Slot:23b}] run summon area_effect_cloud ~ 25 ~ {Tags:["tryashtar.shulker_preview"],CustomName:'{"translate":"tryashtar.shulker_preview.empty_slot"}'}

data modify storage tryashtar:shulker_preview item set from storage tryashtar:shulker_preview contents[{Slot:24b}]
execute if data storage tryashtar:shulker_preview contents[{Slot:24b}] positioned ~ 26 ~ run function tryashtar.shulker_preview:row_2/process_item
execute unless data storage tryashtar:shulker_preview contents[{Slot:24b}] run summon area_effect_cloud ~ 26 ~ {Tags:["tryashtar.shulker_preview"],CustomName:'{"translate":"tryashtar.shulker_preview.empty_slot"}'}

data modify storage tryashtar:shulker_preview item set from storage tryashtar:shulker_preview contents[{Slot:25b}]
execute if data storage tryashtar:shulker_preview contents[{Slot:25b}] positioned ~ 27 ~ run function tryashtar.shulker_preview:row_2/process_item
execute unless data storage tryashtar:shulker_preview contents[{Slot:25b}] run summon area_effect_cloud ~ 27 ~ {Tags:["tryashtar.shulker_preview"],CustomName:'{"translate":"tryashtar.shulker_preview.empty_slot"}'}

data modify storage tryashtar:shulker_preview item set from storage tryashtar:shulker_preview contents[{Slot:26b}]
execute if data storage tryashtar:shulker_preview contents[{Slot:26b}] positioned ~ 28 ~ run function tryashtar.shulker_preview:row_2/process_item
execute unless data storage tryashtar:shulker_preview contents[{Slot:26b}] run summon area_effect_cloud ~ 28 ~ {Tags:["tryashtar.shulker_preview"],CustomName:'{"translate":"tryashtar.shulker_preview.empty_slot"}'}

summon area_effect_cloud ~ 10.99 ~ {Tags:["tryashtar.shulker_preview"],CustomName:'{"translate":"tryashtar.shulker_preview.row_end"}'}
summon area_effect_cloud ~ 19.99 ~ {Tags:["tryashtar.shulker_preview"],CustomName:'{"translate":"tryashtar.shulker_preview.row_end"}'}
summon area_effect_cloud ~ 28.99 ~ {Tags:["tryashtar.shulker_preview"],CustomName:'{"translate":"tryashtar.shulker_preview.row_end"}'}

# evaluate entities on the sign
summon item ~ ~ ~ {UUID:[I;0,29999977,0,9832],Item:{id:tnt,Count:1b}}

data modify entity 0-1c9-c369-0-2668 Item set from storage tryashtar:shulker_preview contents[0]
execute store result score #amount shulker_preview run data get storage tryashtar:shulker_preview contents[0].Count
execute if score #amount shulker_preview matches 1.. if data entity 0-1c9-c369-0-2668 Item.tag.display.Name run data modify block ~2 1 ~ Text1 set value '{"translate":"%1$s%418634357$s","with":[[{"nbt":"Item.tag.display.Name","entity":"0-1c9-c369-0-2668","interpret":true,"color":"gray","italic":false}," x",{"score":{"name":"#amount","objective":"shulker_preview"}}],{"font":"tryashtar.shulker_preview:preview","selector":"@e[type=area_effect_cloud,tag=tryashtar.shulker_preview,x=0,y=0,z=0,sort=nearest]","color":"white","italic":false}]}'
execute if score #amount shulker_preview matches 1.. unless data entity 0-1c9-c369-0-2668 Item.tag.display.Name run data modify block ~2 1 ~ Text1 set value '{"translate":"%1$s%418634357$s","with":[[{"selector":"0-1c9-c369-0-2668","color":"gray","italic":false}," x",{"score":{"name":"#amount","objective":"shulker_preview"}}],{"font":"tryashtar.shulker_preview:preview","selector":"@e[type=area_effect_cloud,tag=tryashtar.shulker_preview,x=0,y=0,z=0,sort=nearest]","color":"white","italic":false}]}'
execute if score #amount shulker_preview matches ..0 run data modify block ~2 1 ~ Text1 set value '{"translate":"%1$s%418634357$s","with":["",{"font":"tryashtar.shulker_preview:preview","selector":"@e[type=area_effect_cloud,tag=tryashtar.shulker_preview,x=0,y=0,z=0,sort=nearest]","color":"white","italic":false}]}'

data modify entity 0-1c9-c369-0-2668 Item set from storage tryashtar:shulker_preview contents[1]
execute store result score #amount shulker_preview run data get storage tryashtar:shulker_preview contents[1].Count
execute if score #amount shulker_preview matches 1.. if data entity 0-1c9-c369-0-2668 Item.tag.display.Name run data modify block ~2 1 ~ Text2 set value '{"translate":"%1$s%418634357$s","with":[[{"nbt":"Item.tag.display.Name","entity":"0-1c9-c369-0-2668","interpret":true,"color":"gray","italic":false}," x",{"score":{"name":"#amount","objective":"shulker_preview"}}],{"font":"tryashtar.shulker_preview:preview","text":"\\uF82C\\uF82A\\uF827"}]}'
execute if score #amount shulker_preview matches 1.. unless data entity 0-1c9-c369-0-2668 Item.tag.display.Name run data modify block ~2 1 ~ Text2 set value '{"translate":"%1$s%418634357$s","with":[[{"selector":"0-1c9-c369-0-2668","color":"gray","italic":false}," x",{"score":{"name":"#amount","objective":"shulker_preview"}}],{"font":"tryashtar.shulker_preview:preview","text":"\\uF82C\\uF82A\\uF827"}]}'
execute if score #amount shulker_preview matches ..0 run data modify block ~2 1 ~ Text2 set value '{"translate":"%1$s%418634357$s","with":["",{"font":"tryashtar.shulker_preview:preview","text":"\\uF82C\\uF82A\\uF827"}]}'

data modify entity 0-1c9-c369-0-2668 Item set from storage tryashtar:shulker_preview contents[2]
execute store result score #amount shulker_preview run data get storage tryashtar:shulker_preview contents[2].Count
execute if score #amount shulker_preview matches 1.. if data entity 0-1c9-c369-0-2668 Item.tag.display.Name run data modify block ~2 1 ~ Text3 set value '{"translate":"%1$s%418634357$s","with":[[{"nbt":"Item.tag.display.Name","entity":"0-1c9-c369-0-2668","interpret":true,"color":"gray","italic":false}," x",{"score":{"name":"#amount","objective":"shulker_preview"}}],""]}'
execute if score #amount shulker_preview matches 1.. unless data entity 0-1c9-c369-0-2668 Item.tag.display.Name run data modify block ~2 1 ~ Text3 set value '{"translate":"%1$s%418634357$s","with":[[{"selector":"0-1c9-c369-0-2668","color":"gray","italic":false}," x",{"score":{"name":"#amount","objective":"shulker_preview"}}],""]}'
execute if score #amount shulker_preview matches ..0 run data modify block ~2 1 ~ Text3 set value '""'

data modify entity 0-1c9-c369-0-2668 Item set from storage tryashtar:shulker_preview contents[3]
execute store result score #amount shulker_preview run data get storage tryashtar:shulker_preview contents[3].Count
execute if score #amount shulker_preview matches 1.. if data entity 0-1c9-c369-0-2668 Item.tag.display.Name run data modify block ~2 1 ~ Text4 set value '{"translate":"%1$s%418634357$s","with":[[{"nbt":"Item.tag.display.Name","entity":"0-1c9-c369-0-2668","interpret":true,"color":"gray","italic":false}," x",{"score":{"name":"#amount","objective":"shulker_preview"}}],""]}'
execute if score #amount shulker_preview matches 1.. unless data entity 0-1c9-c369-0-2668 Item.tag.display.Name run data modify block ~2 1 ~ Text4 set value '{"translate":"%1$s%418634357$s","with":[[{"selector":"0-1c9-c369-0-2668","color":"gray","italic":false}," x",{"score":{"name":"#amount","objective":"shulker_preview"}}],""]}'
execute if score #amount shulker_preview matches ..0 run data modify block ~2 1 ~ Text4 set value '""'

data modify entity 0-1c9-c369-0-2668 Item set from storage tryashtar:shulker_preview contents[4]
execute store result score #amount shulker_preview run data get storage tryashtar:shulker_preview contents[4].Count
execute if score #amount shulker_preview matches 1.. if data entity 0-1c9-c369-0-2668 Item.tag.display.Name run data modify block ~3 1 ~ Text1 set value '{"translate":"%1$s%418634357$s","with":[[{"nbt":"Item.tag.display.Name","entity":"0-1c9-c369-0-2668","interpret":true,"color":"gray","italic":false}," x",{"score":{"name":"#amount","objective":"shulker_preview"}}],""]}'
execute if score #amount shulker_preview matches 1.. unless data entity 0-1c9-c369-0-2668 Item.tag.display.Name run data modify block ~3 1 ~ Text1 set value '{"translate":"%1$s%418634357$s","with":[[{"selector":"0-1c9-c369-0-2668","color":"gray","italic":false}," x",{"score":{"name":"#amount","objective":"shulker_preview"}}],""]}'
execute if score #amount shulker_preview matches ..0 run data modify block ~3 1 ~ Text1 set value '""'

execute store result score #total shulker_preview run data get storage tryashtar:shulker_preview contents
scoreboard players remove #total shulker_preview 5
execute if score #total shulker_preview matches 1.. run data modify block ~3 1 ~ Text2 set value '{"translate":"%1$s%418634357$s","with":[{"translate":"container.shulkerBox.more","color":"gray","italic":true,"with":[{"score":{"name":"#total","objective":"shulker_preview"}}]},""]}'

kill 0-1c9-c369-0-2668
execute if score #header_type shulker_preview matches 1 run data remove storage tryashtar:shulker_preview items[0].tag.BlockEntityTag
kill @e[type=area_effect_cloud,tag=tryashtar.shulker_preview]

# don't process any more items this tick
scoreboard players set #ready shulker_preview 0
