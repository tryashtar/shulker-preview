scoreboard players set #red shulker_preview 0
scoreboard players set #green shulker_preview 0
scoreboard players set #blue shulker_preview 0
execute store result score #total shulker_preview run data get storage tryashtar.shulker_preview:data item.components."minecraft:firework_explosion".colors
execute if score #total shulker_preview matches 0 run return run return fail
function tryashtar.shulker_preview:star_color_loop

scoreboard players operation #red shulker_preview /= #total shulker_preview
scoreboard players operation #green shulker_preview /= #total shulker_preview
scoreboard players operation #blue shulker_preview /= #total shulker_preview
execute store result storage tryashtar.shulker_preview:data color.red int 1 run scoreboard players get #red shulker_preview
execute store result storage tryashtar.shulker_preview:data color.green int 1 run scoreboard players get #green shulker_preview
execute store result storage tryashtar.shulker_preview:data color.blue int 1 run scoreboard players get #blue shulker_preview
function tryashtar.shulker_preview:hex_color with storage tryashtar.shulker_preview:data color
