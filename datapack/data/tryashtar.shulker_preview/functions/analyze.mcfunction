# summon tooltip background
execute unless score #header_type shulker_preview matches 2 if data storage tryashtar:shulker_preview items[0].tag.display.Name run summon area_effect_cloud ~ 1 ~ {Tags:["tryashtar.shulker_preview"],CustomName:'{"translate":"tryashtar.shulker_preview.shulker_tooltip"}'}
execute if score #header_type shulker_preview matches 0 unless data storage tryashtar:shulker_preview items[0].tag.display.Name run summon area_effect_cloud ~ 1 ~ {Tags:["tryashtar.shulker_preview"],CustomName:'{"translate":"tryashtar.shulker_preview.shulker_tooltip_header"}'}
execute if score #header_type shulker_preview matches 1 unless data storage tryashtar:shulker_preview items[0].tag.display.Name run summon area_effect_cloud ~ 1 ~ {Tags:["tryashtar.shulker_preview"],CustomName:'{"translate":"tryashtar.shulker_preview.ender_tooltip"}'}

# copy and analyze contents one by one
execute if score #header_type shulker_preview matches 0..1 run function tryashtar.shulker_preview:analyze_slots
execute if score #header_type shulker_preview matches 2 positioned ~ 2 ~ run function tryashtar.shulker_preview:bundle/analyze

# evaluate entities on the sign
summon item ~ ~ ~ {UUID:[I;0,29999977,0,9832],Item:{id:tnt,Count:1b}}

data modify entity 0-1c9-c369-0-2668 Item set from storage tryashtar:shulker_preview contents[0]
execute store result score #amount shulker_preview run data get storage tryashtar:shulker_preview contents[0].Count
execute if score #amount shulker_preview matches 1.. if data entity 0-1c9-c369-0-2668 Item.tag.display.Name run data modify block ~2 1 ~ Text1 set value '{"translate":"%1$s%418634357$s","with":[[{"nbt":"Item.tag.display.Name","entity":"0-1c9-c369-0-2668","interpret":true,"color":"gray","italic":false}," x",{"score":{"name":"#amount","objective":"shulker_preview"}}],{"font":"tryashtar.shulker_preview:preview","selector":"@e[type=area_effect_cloud,tag=tryashtar.shulker_preview,x=0,y=0,z=0,sort=nearest]","color":"white","italic":false}]}'
execute if score #amount shulker_preview matches 1.. unless data entity 0-1c9-c369-0-2668 Item.tag.display.Name run data modify block ~2 1 ~ Text1 set value '{"translate":"%1$s%418634357$s","with":[[{"selector":"0-1c9-c369-0-2668","color":"gray","italic":false}," x",{"score":{"name":"#amount","objective":"shulker_preview"}}],{"font":"tryashtar.shulker_preview:preview","selector":"@e[type=area_effect_cloud,tag=tryashtar.shulker_preview,x=0,y=0,z=0,sort=nearest]","color":"white","italic":false}]}'
execute if score #amount shulker_preview matches ..0 run data modify block ~2 1 ~ Text1 set value '{"translate":"%1$s%418634357$s","with":["",{"font":"tryashtar.shulker_preview:preview","selector":"@e[type=area_effect_cloud,tag=tryashtar.shulker_preview,x=0,y=0,z=0,sort=nearest]","color":"white","italic":false}]}'

data modify entity 0-1c9-c369-0-2668 Item set from storage tryashtar:shulker_preview contents[1]
execute store result score #amount shulker_preview run data get storage tryashtar:shulker_preview contents[1].Count
execute if score #amount shulker_preview matches 1.. if data entity 0-1c9-c369-0-2668 Item.tag.display.Name run data modify block ~2 1 ~ Text2 set value '{"translate":"%1$s%418634357$s","with":[[{"nbt":"Item.tag.display.Name","entity":"0-1c9-c369-0-2668","interpret":true,"color":"gray","italic":false}," x",{"score":{"name":"#amount","objective":"shulker_preview"}}],""]}'
execute if score #amount shulker_preview matches 1.. unless data entity 0-1c9-c369-0-2668 Item.tag.display.Name run data modify block ~2 1 ~ Text2 set value '{"translate":"%1$s%418634357$s","with":[[{"selector":"0-1c9-c369-0-2668","color":"gray","italic":false}," x",{"score":{"name":"#amount","objective":"shulker_preview"}}],""]}'
execute if score #amount shulker_preview matches ..0 run data modify block ~2 1 ~ Text2 set value '""'

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
