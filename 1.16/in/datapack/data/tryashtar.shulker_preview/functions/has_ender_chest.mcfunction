execute store result score #ender_chests shulker_preview run clear @s ender_chest 0
execute if score #ender_chests shulker_preview matches 1.. positioned 29999977 1 9832 run function tryashtar.shulker_preview:check_ender_chests
tag @s remove shulker_preview.ender_chest
