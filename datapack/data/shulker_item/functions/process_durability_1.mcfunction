# create an entity that draws a durability bar on the second row
scoreboard players operation #durability shulker_item *= #14 shulker_item
scoreboard players operation #durability shulker_item /= #max shulker_item
execute if score #durability shulker_item matches 0 run summon area_effect_cloud ~ ~ ~ {Tags:["shulker_item"],CustomName:"{\"translate\":\"shulker_item.durability.0.1\"}"}
execute if score #durability shulker_item matches 1 run summon area_effect_cloud ~ ~ ~ {Tags:["shulker_item"],CustomName:"{\"translate\":\"shulker_item.durability.1.1\"}"}
execute if score #durability shulker_item matches 2 run summon area_effect_cloud ~ ~ ~ {Tags:["shulker_item"],CustomName:"{\"translate\":\"shulker_item.durability.2.1\"}"}
execute if score #durability shulker_item matches 3 run summon area_effect_cloud ~ ~ ~ {Tags:["shulker_item"],CustomName:"{\"translate\":\"shulker_item.durability.3.1\"}"}
execute if score #durability shulker_item matches 4 run summon area_effect_cloud ~ ~ ~ {Tags:["shulker_item"],CustomName:"{\"translate\":\"shulker_item.durability.4.1\"}"}
execute if score #durability shulker_item matches 5 run summon area_effect_cloud ~ ~ ~ {Tags:["shulker_item"],CustomName:"{\"translate\":\"shulker_item.durability.5.1\"}"}
execute if score #durability shulker_item matches 6 run summon area_effect_cloud ~ ~ ~ {Tags:["shulker_item"],CustomName:"{\"translate\":\"shulker_item.durability.6.1\"}"}
execute if score #durability shulker_item matches 7 run summon area_effect_cloud ~ ~ ~ {Tags:["shulker_item"],CustomName:"{\"translate\":\"shulker_item.durability.7.1\"}"}
execute if score #durability shulker_item matches 8 run summon area_effect_cloud ~ ~ ~ {Tags:["shulker_item"],CustomName:"{\"translate\":\"shulker_item.durability.8.1\"}"}
execute if score #durability shulker_item matches 9 run summon area_effect_cloud ~ ~ ~ {Tags:["shulker_item"],CustomName:"{\"translate\":\"shulker_item.durability.9.1\"}"}
execute if score #durability shulker_item matches 10 run summon area_effect_cloud ~ ~ ~ {Tags:["shulker_item"],CustomName:"{\"translate\":\"shulker_item.durability.10.1\"}"}
execute if score #durability shulker_item matches 11 run summon area_effect_cloud ~ ~ ~ {Tags:["shulker_item"],CustomName:"{\"translate\":\"shulker_item.durability.11.1\"}"}
execute if score #durability shulker_item matches 12 run summon area_effect_cloud ~ ~ ~ {Tags:["shulker_item"],CustomName:"{\"translate\":\"shulker_item.durability.12.1\"}"}
execute if score #durability shulker_item matches 13.. run summon area_effect_cloud ~ ~ ~ {Tags:["shulker_item"],CustomName:"{\"translate\":\"shulker_item.durability.13.1\"}"}
