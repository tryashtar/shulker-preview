execute store result score #bundles shulker_preview run clear @s bundle 0
execute if score #bundles shulker_preview matches 1.. positioned 29999977 1 9832 run function tryashtar.shulker_preview:check_bundles
tag @s remove shulker_preview.bundle
