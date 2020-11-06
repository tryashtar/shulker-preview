# check for any bundles
# can't say for sure whether any of them have been updated yet
execute store result score #bundles shulker_preview run clear @s bundle 0
execute if score #ready shulker_preview matches 1 if score #bundles shulker_preview matches 1.. positioned 29999977 1 9832 run function tryashtar.shulker_preview:bundle/prepare
