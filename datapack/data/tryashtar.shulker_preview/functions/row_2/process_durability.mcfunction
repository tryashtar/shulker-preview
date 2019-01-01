# create an entity that draws a durability bar
scoreboard players operation #durability shulker_preview *= #140 shulker_preview
scoreboard players operation #durability shulker_preview /= #max shulker_preview
execute if score #durability shulker_preview matches 5..15 run summon area_effect_cloud ~ ~ ~ {Tags:["tryashtar.shulker_preview"],CustomName:"{\"translate\":\"tryashtar.shulker_preview.durability.1.2\"}"}
execute if score #durability shulker_preview matches 15..25 run summon area_effect_cloud ~ ~ ~ {Tags:["tryashtar.shulker_preview"],CustomName:"{\"translate\":\"tryashtar.shulker_preview.durability.2.2\"}"}
execute if score #durability shulker_preview matches 25..35 run summon area_effect_cloud ~ ~ ~ {Tags:["tryashtar.shulker_preview"],CustomName:"{\"translate\":\"tryashtar.shulker_preview.durability.3.2\"}"}
execute if score #durability shulker_preview matches 35..45 run summon area_effect_cloud ~ ~ ~ {Tags:["tryashtar.shulker_preview"],CustomName:"{\"translate\":\"tryashtar.shulker_preview.durability.4.2\"}"}
execute if score #durability shulker_preview matches 45..55 run summon area_effect_cloud ~ ~ ~ {Tags:["tryashtar.shulker_preview"],CustomName:"{\"translate\":\"tryashtar.shulker_preview.durability.5.2\"}"}
execute if score #durability shulker_preview matches 55..65 run summon area_effect_cloud ~ ~ ~ {Tags:["tryashtar.shulker_preview"],CustomName:"{\"translate\":\"tryashtar.shulker_preview.durability.6.2\"}"}
execute if score #durability shulker_preview matches 65..75 run summon area_effect_cloud ~ ~ ~ {Tags:["tryashtar.shulker_preview"],CustomName:"{\"translate\":\"tryashtar.shulker_preview.durability.7.2\"}"}
execute if score #durability shulker_preview matches 75..85 run summon area_effect_cloud ~ ~ ~ {Tags:["tryashtar.shulker_preview"],CustomName:"{\"translate\":\"tryashtar.shulker_preview.durability.8.2\"}"}
execute if score #durability shulker_preview matches 85..95 run summon area_effect_cloud ~ ~ ~ {Tags:["tryashtar.shulker_preview"],CustomName:"{\"translate\":\"tryashtar.shulker_preview.durability.9.2\"}"}
execute if score #durability shulker_preview matches 95..105 run summon area_effect_cloud ~ ~ ~ {Tags:["tryashtar.shulker_preview"],CustomName:"{\"translate\":\"tryashtar.shulker_preview.durability.10.2\"}"}
execute if score #durability shulker_preview matches 105..115 run summon area_effect_cloud ~ ~ ~ {Tags:["tryashtar.shulker_preview"],CustomName:"{\"translate\":\"tryashtar.shulker_preview.durability.11.2\"}"}
execute if score #durability shulker_preview matches 115..125 run summon area_effect_cloud ~ ~ ~ {Tags:["tryashtar.shulker_preview"],CustomName:"{\"translate\":\"tryashtar.shulker_preview.durability.12.2\"}"}
execute if score #durability shulker_preview matches 125..135 run summon area_effect_cloud ~ ~ ~ {Tags:["tryashtar.shulker_preview"],CustomName:"{\"translate\":\"tryashtar.shulker_preview.durability.13.2\"}"}
execute if score #durability shulker_preview matches 135.. run summon area_effect_cloud ~ ~ ~ {Tags:["tryashtar.shulker_preview"],CustomName:"{\"translate\":\"tryashtar.shulker_preview.durability.14.2\"}"}
