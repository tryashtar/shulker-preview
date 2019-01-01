# create an entity that draws a durability bar
scoreboard players operation #durability shulker_item *= #140 shulker_item
scoreboard players operation #durability shulker_item /= #max shulker_item
execute if score #durability shulker_item matches 5..15 run summon area_effect_cloud ~ ~ ~ {Tags:["shulker_item"],CustomName:"{\"translate\":\"shulker_item.durability.1.2\"}"}
execute if score #durability shulker_item matches 15..25 run summon area_effect_cloud ~ ~ ~ {Tags:["shulker_item"],CustomName:"{\"translate\":\"shulker_item.durability.2.2\"}"}
execute if score #durability shulker_item matches 25..35 run summon area_effect_cloud ~ ~ ~ {Tags:["shulker_item"],CustomName:"{\"translate\":\"shulker_item.durability.3.2\"}"}
execute if score #durability shulker_item matches 35..45 run summon area_effect_cloud ~ ~ ~ {Tags:["shulker_item"],CustomName:"{\"translate\":\"shulker_item.durability.4.2\"}"}
execute if score #durability shulker_item matches 45..55 run summon area_effect_cloud ~ ~ ~ {Tags:["shulker_item"],CustomName:"{\"translate\":\"shulker_item.durability.5.2\"}"}
execute if score #durability shulker_item matches 55..65 run summon area_effect_cloud ~ ~ ~ {Tags:["shulker_item"],CustomName:"{\"translate\":\"shulker_item.durability.6.2\"}"}
execute if score #durability shulker_item matches 65..75 run summon area_effect_cloud ~ ~ ~ {Tags:["shulker_item"],CustomName:"{\"translate\":\"shulker_item.durability.7.2\"}"}
execute if score #durability shulker_item matches 75..85 run summon area_effect_cloud ~ ~ ~ {Tags:["shulker_item"],CustomName:"{\"translate\":\"shulker_item.durability.8.2\"}"}
execute if score #durability shulker_item matches 85..95 run summon area_effect_cloud ~ ~ ~ {Tags:["shulker_item"],CustomName:"{\"translate\":\"shulker_item.durability.9.2\"}"}
execute if score #durability shulker_item matches 95..105 run summon area_effect_cloud ~ ~ ~ {Tags:["shulker_item"],CustomName:"{\"translate\":\"shulker_item.durability.10.2\"}"}
execute if score #durability shulker_item matches 105..115 run summon area_effect_cloud ~ ~ ~ {Tags:["shulker_item"],CustomName:"{\"translate\":\"shulker_item.durability.11.2\"}"}
execute if score #durability shulker_item matches 115..125 run summon area_effect_cloud ~ ~ ~ {Tags:["shulker_item"],CustomName:"{\"translate\":\"shulker_item.durability.12.2\"}"}
execute if score #durability shulker_item matches 125..135 run summon area_effect_cloud ~ ~ ~ {Tags:["shulker_item"],CustomName:"{\"translate\":\"shulker_item.durability.13.2\"}"}
execute if score #durability shulker_item matches 135.. run summon area_effect_cloud ~ ~ ~ {Tags:["shulker_item"],CustomName:"{\"translate\":\"shulker_item.durability.14.2\"}"}
