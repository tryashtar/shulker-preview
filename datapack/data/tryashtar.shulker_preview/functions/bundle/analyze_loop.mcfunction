data modify storage tryashtar:shulker_preview item set from storage tryashtar:shulker_preview running_contents[0]
execute if score #row shulker_preview matches 0 run function tryashtar.shulker_preview:row_0/process_item
execute if score #row shulker_preview matches 1 run function tryashtar.shulker_preview:row_1/process_item
execute if score #row shulker_preview matches 2 run function tryashtar.shulker_preview:row_2/process_item
execute if score #row shulker_preview matches 3 run function tryashtar.shulker_preview:row_3/process_item
data remove storage tryashtar:shulker_preview running_contents[0]

scoreboard players add #slots shulker_preview 1
execute if score #slots shulker_preview >= #row_size shulker_preview positioned ~ ~1 ~ run function tryashtar.shulker_preview:bundle/rows/return

execute if data storage tryashtar:shulker_preview running_contents[0] positioned ~ ~2 ~ run function tryashtar.shulker_preview:bundle/analyze_loop
