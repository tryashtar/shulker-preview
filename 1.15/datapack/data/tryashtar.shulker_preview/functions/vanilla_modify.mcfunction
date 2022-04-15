data modify entity 0-1c9-c369-0-2668 Item set from block ~ 1 ~ Items[0].tag.BlockEntityTag.Items[0]
execute store result score #amount shulker_preview run data get block ~ 1 ~ Items[0].tag.BlockEntityTag.Items[0].Count
execute if score #amount shulker_preview matches 1.. if data entity 0-1c9-c369-0-2668 Item.tag.display.Name run data modify block ~2 1 ~ Text1 set value '{"translate":"%1$s%418634357$s","with":[[{"nbt":"Item.tag.display.Name","entity":"0-1c9-c369-0-2668","interpret":true,"color":"gray","italic":false}," x",{"score":{"name":"#amount","objective":"shulker_preview"}}],["\\uF800",{"selector":"@e[type=area_effect_cloud,tag=tryashtar.shulker_preview,x=0,y=0,z=0,sort=nearest]","color":"white","italic":false}]]}'
execute if score #amount shulker_preview matches 1.. unless data entity 0-1c9-c369-0-2668 Item.tag.display.Name run data modify block ~2 1 ~ Text1 set value '{"translate":"%1$s%418634357$s","with":[[{"selector":"0-1c9-c369-0-2668","color":"gray","italic":false}," x",{"score":{"name":"#amount","objective":"shulker_preview"}}],["\\uF800",{"selector":"@e[type=area_effect_cloud,tag=tryashtar.shulker_preview,x=0,y=0,z=0,sort=nearest]","color":"white","italic":false}]]}'
execute if score #amount shulker_preview matches ..0 run data modify block ~2 1 ~ Text1 set value '{"translate":"%1$s%418634357$s","with":["",["\\uF800",{"selector":"@e[type=area_effect_cloud,tag=tryashtar.shulker_preview,x=0,y=0,z=0,sort=nearest]","color":"white","italic":false}]]}'
data modify storage tryashtar:shulker_preview line1 set from block ~2 1 ~ Text1

data modify entity 0-1c9-c369-0-2668 Item set from block ~ 1 ~ Items[0].tag.BlockEntityTag.Items[1]
execute store result score #amount shulker_preview run data get block ~ 1 ~ Items[0].tag.BlockEntityTag.Items[1].Count
execute if score #amount shulker_preview matches 1.. if data entity 0-1c9-c369-0-2668 Item.tag.display.Name run data modify block ~2 1 ~ Text2 set value '{"translate":"%1$s%418634357$s","with":[[{"nbt":"Item.tag.display.Name","entity":"0-1c9-c369-0-2668","interpret":true,"color":"gray","italic":false}," x",{"score":{"name":"#amount","objective":"shulker_preview"}}],"\\uF82C\\uF82A\\uF827"]}'
execute if score #amount shulker_preview matches 1.. unless data entity 0-1c9-c369-0-2668 Item.tag.display.Name run data modify block ~2 1 ~ Text2 set value '{"translate":"%1$s%418634357$s","with":[[{"selector":"0-1c9-c369-0-2668","color":"gray","italic":false}," x",{"score":{"name":"#amount","objective":"shulker_preview"}}],"\\uF82C\\uF82A\\uF827"]}'
execute if score #amount shulker_preview matches ..0 run data modify block ~2 1 ~ Text2 set value '{"translate":"%1$s%418634357$s","with":["","\\uF82C\\uF82A\\uF827"]}'
data modify storage tryashtar:shulker_preview line2 set from block ~2 1 ~ Text2

data modify entity 0-1c9-c369-0-2668 Item set from block ~ 1 ~ Items[0].tag.BlockEntityTag.Items[2]
execute store result score #amount shulker_preview run data get block ~ 1 ~ Items[0].tag.BlockEntityTag.Items[2].Count
execute if score #amount shulker_preview matches 1.. if data entity 0-1c9-c369-0-2668 Item.tag.display.Name run data modify block ~2 1 ~ Text3 set value '{"translate":"%1$s%418634357$s","with":[[{"nbt":"Item.tag.display.Name","entity":"0-1c9-c369-0-2668","interpret":true,"color":"gray","italic":false}," x",{"score":{"name":"#amount","objective":"shulker_preview"}}],""]}'
execute if score #amount shulker_preview matches 1.. unless data entity 0-1c9-c369-0-2668 Item.tag.display.Name run data modify block ~2 1 ~ Text3 set value '{"translate":"%1$s%418634357$s","with":[[{"selector":"0-1c9-c369-0-2668","color":"gray","italic":false}," x",{"score":{"name":"#amount","objective":"shulker_preview"}}],""]}'
execute if score #amount shulker_preview matches ..0 run data modify block ~2 1 ~ Text3 set value '""'
data modify storage tryashtar:shulker_preview line3 set from block ~2 1 ~ Text3

data modify entity 0-1c9-c369-0-2668 Item set from block ~ 1 ~ Items[0].tag.BlockEntityTag.Items[3]
execute store result score #amount shulker_preview run data get block ~ 1 ~ Items[0].tag.BlockEntityTag.Items[3].Count
execute if score #amount shulker_preview matches 1.. if data entity 0-1c9-c369-0-2668 Item.tag.display.Name run data modify block ~2 1 ~ Text4 set value '{"translate":"%1$s%418634357$s","with":[[{"nbt":"Item.tag.display.Name","entity":"0-1c9-c369-0-2668","interpret":true,"color":"gray","italic":false}," x",{"score":{"name":"#amount","objective":"shulker_preview"}}],""]}'
execute if score #amount shulker_preview matches 1.. unless data entity 0-1c9-c369-0-2668 Item.tag.display.Name run data modify block ~2 1 ~ Text4 set value '{"translate":"%1$s%418634357$s","with":[[{"selector":"0-1c9-c369-0-2668","color":"gray","italic":false}," x",{"score":{"name":"#amount","objective":"shulker_preview"}}],""]}'
execute if score #amount shulker_preview matches ..0 run data modify block ~2 1 ~ Text4 set value '""'
data modify storage tryashtar:shulker_preview line4 set from block ~2 1 ~ Text4

data modify entity 0-1c9-c369-0-2668 Item set from block ~ 1 ~ Items[0].tag.BlockEntityTag.Items[4]
execute store result score #amount shulker_preview run data get block ~ 1 ~ Items[0].tag.BlockEntityTag.Items[4].Count
execute if score #amount shulker_preview matches 1.. if data entity 0-1c9-c369-0-2668 Item.tag.display.Name run data modify block ~3 1 ~ Text1 set value '{"translate":"%1$s%418634357$s","with":[[{"nbt":"Item.tag.display.Name","entity":"0-1c9-c369-0-2668","interpret":true,"color":"gray","italic":false}," x",{"score":{"name":"#amount","objective":"shulker_preview"}}],""]}'
execute if score #amount shulker_preview matches 1.. unless data entity 0-1c9-c369-0-2668 Item.tag.display.Name run data modify block ~3 1 ~ Text1 set value '{"translate":"%1$s%418634357$s","with":[[{"selector":"0-1c9-c369-0-2668","color":"gray","italic":false}," x",{"score":{"name":"#amount","objective":"shulker_preview"}}],""]}'
execute if score #amount shulker_preview matches ..0 run data modify block ~3 1 ~ Text1 set value '""'
data modify storage tryashtar:shulker_preview line5 set from block ~3 1 ~ Text1

execute store result score #total shulker_preview run data get block ~ 1 ~ Items[0].tag.BlockEntityTag.Items
scoreboard players remove #total shulker_preview 5
execute if score #total shulker_preview matches 1.. run data modify block ~3 1 ~ Text2 set value '{"translate":"%1$s%418634357$s","with":[{"translate":"container.shulkerBox.more","color":"gray","italic":true,"with":[{"score":{"name":"#total","objective":"shulker_preview"}}]},""]}'
data modify storage tryashtar:shulker_preview line6 set from block ~3 1 ~ Text2
