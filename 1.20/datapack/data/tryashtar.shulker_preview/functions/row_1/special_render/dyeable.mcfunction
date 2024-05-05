execute store success score #has_color shulker_preview store result score #color shulker_preview run data get storage tryashtar.shulker_preview:data item.components."minecraft:dyed_color".rgb
scoreboard players operation #blue shulker_preview = #color shulker_preview
scoreboard players operation #blue shulker_preview %= #256 shulker_preview
scoreboard players operation #color shulker_preview /= #256 shulker_preview
scoreboard players operation #green shulker_preview = #color shulker_preview
scoreboard players operation #green shulker_preview %= #256 shulker_preview
scoreboard players operation #color shulker_preview /= #256 shulker_preview
scoreboard players operation #red shulker_preview = #color shulker_preview
$execute if items entity 7368756c-6b65-7220-7072-657669657721 contents wolf_armor run data modify storage tryashtar.shulker_preview:data tooltip append value '[{"translate":"tryashtar.shulker_preview.layer.$(id).0.1"},{"translate":"tryashtar.shulker_preview.layer.$(id).1.1","color":"#00aced"}]'
$execute unless items entity 7368756c-6b65-7220-7072-657669657721 contents wolf_armor run data modify storage tryashtar.shulker_preview:data tooltip append value '[{"translate":"tryashtar.shulker_preview.layer.$(id).0.1","color":"#00aced"},{"translate":"tryashtar.shulker_preview.layer.$(id).1.1","color":"white"}]'
