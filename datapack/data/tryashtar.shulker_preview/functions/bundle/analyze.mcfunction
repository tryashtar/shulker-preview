scoreboard players set #slots shulker_preview 0
scoreboard players set #row shulker_preview 0
execute store result score #row_size shulker_preview run data get storage tryashtar:shulker_preview contents
scoreboard players operation #row_count shulker_preview = #row_size shulker_preview
scoreboard players remove #row_size shulker_preview 17
scoreboard players operation #row_size shulker_preview /= #4 shulker_preview
execute if score #row_size shulker_preview matches ..-1 run scoreboard players set #row_size shulker_preview 0
scoreboard players add #row_size shulker_preview 5
scoreboard players operation #row_count shulker_preview /= #row_size shulker_preview

execute if score #row_count shulker_preview matches 0 run function tryashtar.shulker_preview:bundle/single_row

data modify storage tryashtar:shulker_preview running_contents set from storage tryashtar:shulker_preview contents
execute positioned ~ ~64 ~ run function tryashtar.shulker_preview:bundle/analyze_loop
