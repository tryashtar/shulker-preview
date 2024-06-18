# divide out the individual channels and add them to the running total
execute store result score #color shulker_preview run data get storage tryashtar.shulker_preview:data item.components."minecraft:firework_explosion".colors[-1]
scoreboard players operation #more_blue shulker_preview = #color shulker_preview
scoreboard players operation #more_blue shulker_preview %= #256 shulker_preview
scoreboard players operation #blue shulker_preview += #more_blue shulker_preview
scoreboard players operation #color shulker_preview /= #256 shulker_preview
scoreboard players operation #more_green shulker_preview = #color shulker_preview
scoreboard players operation #more_green shulker_preview %= #256 shulker_preview
scoreboard players operation #green shulker_preview += #more_green shulker_preview
scoreboard players operation #color shulker_preview /= #256 shulker_preview
scoreboard players operation #red shulker_preview += #color shulker_preview

# iterate to the next color
data remove storage tryashtar.shulker_preview:data item.components."minecraft:firework_explosion".colors[-1]
execute if data storage tryashtar.shulker_preview:data item.components."minecraft:firework_explosion".colors[0] run function tryashtar.shulker_preview:render/star_color_loop
