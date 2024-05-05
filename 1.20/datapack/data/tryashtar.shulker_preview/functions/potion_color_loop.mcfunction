execute store result score #amplifier shulker_preview run data get storage tryashtar.shulker_preview:data item.components."minecraft:potion_contents".custom_effects[-1].amplifier
execute unless data storage tryashtar.shulker_preview:data item.components."minecraft:potion_contents".custom_effects[-1].amplifier run scoreboard players set #amplifier shulker_preview 0
scoreboard players add #amplifier shulker_preview 1
function tryashtar.shulker_preview:potion_color_get with storage tryashtar.shulker_preview:data item.components."minecraft:potion_contents".custom_effects[-1]

data remove storage tryashtar.shulker_preview:data item.components."minecraft:potion_contents".custom_effects[-1]
execute if data storage tryashtar.shulker_preview:data item.components."minecraft:potion_contents".custom_effects[0] run function tryashtar.shulker_preview:potion_color_loop
