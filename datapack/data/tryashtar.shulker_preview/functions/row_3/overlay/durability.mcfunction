# create an entity that draws a durability bar
scoreboard players operation #durability shulker_preview *= #13000 shulker_preview
scoreboard players operation #durability shulker_preview /= #max shulker_preview
execute if score #durability shulker_preview matches 1..499 run summon area_effect_cloud ~ ~0.8 ~ {Tags:["tryashtar.shulker_preview"],CustomName:'{"translate":"tryashtar.shulker_preview.durability.1.3"}'}
execute if score #durability shulker_preview matches 500..1499 run summon area_effect_cloud ~ ~0.8 ~ {Tags:["tryashtar.shulker_preview"],CustomName:'{"translate":"tryashtar.shulker_preview.durability.2.3"}'}
execute if score #durability shulker_preview matches 1500..2499 run summon area_effect_cloud ~ ~0.8 ~ {Tags:["tryashtar.shulker_preview"],CustomName:'{"translate":"tryashtar.shulker_preview.durability.3.3"}'}
execute if score #durability shulker_preview matches 2500..3499 run summon area_effect_cloud ~ ~0.8 ~ {Tags:["tryashtar.shulker_preview"],CustomName:'{"translate":"tryashtar.shulker_preview.durability.4.3"}'}
execute if score #durability shulker_preview matches 3500..4499 run summon area_effect_cloud ~ ~0.8 ~ {Tags:["tryashtar.shulker_preview"],CustomName:'{"translate":"tryashtar.shulker_preview.durability.5.3"}'}
execute if score #durability shulker_preview matches 4500..5499 run summon area_effect_cloud ~ ~0.8 ~ {Tags:["tryashtar.shulker_preview"],CustomName:'{"translate":"tryashtar.shulker_preview.durability.6.3"}'}
execute if score #durability shulker_preview matches 5500..6499 run summon area_effect_cloud ~ ~0.8 ~ {Tags:["tryashtar.shulker_preview"],CustomName:'{"translate":"tryashtar.shulker_preview.durability.7.3"}'}
execute if score #durability shulker_preview matches 6500..7499 run summon area_effect_cloud ~ ~0.8 ~ {Tags:["tryashtar.shulker_preview"],CustomName:'{"translate":"tryashtar.shulker_preview.durability.8.3"}'}
execute if score #durability shulker_preview matches 7500..8499 run summon area_effect_cloud ~ ~0.8 ~ {Tags:["tryashtar.shulker_preview"],CustomName:'{"translate":"tryashtar.shulker_preview.durability.9.3"}'}
execute if score #durability shulker_preview matches 8500..9499 run summon area_effect_cloud ~ ~0.8 ~ {Tags:["tryashtar.shulker_preview"],CustomName:'{"translate":"tryashtar.shulker_preview.durability.10.3"}'}
execute if score #durability shulker_preview matches 9500..10499 run summon area_effect_cloud ~ ~0.8 ~ {Tags:["tryashtar.shulker_preview"],CustomName:'{"translate":"tryashtar.shulker_preview.durability.11.3"}'}
execute if score #durability shulker_preview matches 10500..11499 run summon area_effect_cloud ~ ~0.8 ~ {Tags:["tryashtar.shulker_preview"],CustomName:'{"translate":"tryashtar.shulker_preview.durability.12.3"}'}
execute if score #durability shulker_preview matches 11500..12499 run summon area_effect_cloud ~ ~0.8 ~ {Tags:["tryashtar.shulker_preview"],CustomName:'{"translate":"tryashtar.shulker_preview.durability.13.3"}'}
execute if score #durability shulker_preview matches 12500.. run summon area_effect_cloud ~ ~0.8 ~ {Tags:["tryashtar.shulker_preview"],CustomName:'{"translate":"tryashtar.shulker_preview.durability.14.3"}'}
