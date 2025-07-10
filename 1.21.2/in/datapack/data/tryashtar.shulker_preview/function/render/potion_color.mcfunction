# a potion color is derived by averaging the colors of all of its effects, weighted by their amplifier
# copy the regular potion type to the custom_effects, if any, to iterate them altogether
execute if data storage tryashtar.shulker_preview:data item.components."minecraft:potion_contents".potion run data modify storage tryashtar.shulker_preview:data item.components."minecraft:potion_contents".custom_effects append value {}
execute if data storage tryashtar.shulker_preview:data item.components."minecraft:potion_contents".potion run data modify storage tryashtar.shulker_preview:data item.components."minecraft:potion_contents".custom_effects[-1].id set from storage tryashtar.shulker_preview:data item.components."minecraft:potion_contents".potion
scoreboard players set #red shulker_preview 0
scoreboard players set #green shulker_preview 0
scoreboard players set #blue shulker_preview 0
scoreboard players set #total shulker_preview 0
execute if data storage tryashtar.shulker_preview:data item.components."minecraft:potion_contents".custom_effects[0] run function tryashtar.shulker_preview:render/potion_color_loop

# average out the colors and get the result in hex form for the color macro
execute if score #total shulker_preview matches 0 run return run return fail
scoreboard players operation #red shulker_preview /= #total shulker_preview
scoreboard players operation #green shulker_preview /= #total shulker_preview
scoreboard players operation #blue shulker_preview /= #total shulker_preview
execute store result storage tryashtar.shulker_preview:data color.red int 1 run scoreboard players get #red shulker_preview
execute store result storage tryashtar.shulker_preview:data color.green int 1 run scoreboard players get #green shulker_preview
execute store result storage tryashtar.shulker_preview:data color.blue int 1 run scoreboard players get #blue shulker_preview
function tryashtar.shulker_preview:render/hex_color with storage tryashtar.shulker_preview:data color
