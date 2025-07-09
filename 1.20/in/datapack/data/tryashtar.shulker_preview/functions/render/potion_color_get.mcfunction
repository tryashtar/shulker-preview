# look up the red, green, and blue components of this potion effect
# some potions like turtle master or water bottles add different amounts to the total, since they don't just have one effect
$data modify storage tryashtar.shulker_preview:data potion_color set from storage tryashtar.shulker_preview:data lookups.potions."$(id)"
execute store result score #add shulker_preview run data get storage tryashtar.shulker_preview:data potion_color[0]
scoreboard players operation #add shulker_preview *= #amplifier shulker_preview
scoreboard players operation #red shulker_preview += #add shulker_preview
execute store result score #add shulker_preview run data get storage tryashtar.shulker_preview:data potion_color[1]
scoreboard players operation #add shulker_preview *= #amplifier shulker_preview
scoreboard players operation #green shulker_preview += #add shulker_preview
execute store result score #add shulker_preview run data get storage tryashtar.shulker_preview:data potion_color[2]
scoreboard players operation #add shulker_preview *= #amplifier shulker_preview
scoreboard players operation #blue shulker_preview += #add shulker_preview
execute store result score #add shulker_preview run data get storage tryashtar.shulker_preview:data potion_color[3]
scoreboard players operation #add shulker_preview *= #amplifier shulker_preview
scoreboard players operation #total shulker_preview += #add shulker_preview
