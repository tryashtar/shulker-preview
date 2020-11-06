# determine row size
scoreboard players set #slots shulker_preview 0
scoreboard players set #row shulker_preview 0
execute store result score #row_size shulker_preview run data get storage tryashtar:shulker_preview contents
scoreboard players operation #row_count shulker_preview = #row_size shulker_preview
scoreboard players remove #row_count shulker_preview 1
scoreboard players remove #row_size shulker_preview 17
scoreboard players operation #row_size shulker_preview /= #4 shulker_preview
execute if score #row_size shulker_preview matches ..-1 run scoreboard players set #row_size shulker_preview 0
scoreboard players add #row_size shulker_preview 5
scoreboard players operation #row_count shulker_preview /= #5 shulker_preview

# draw background
summon area_effect_cloud ~ ~ ~ {Tags:["tryashtar.shulker_preview"],CustomName:'{"translate":"tryashtar.shulker_preview.adjust_bundle_tooltip"}'}
execute if score #row_count shulker_preview matches 0 positioned ~ ~1 ~ run function tryashtar.shulker_preview:bundle/rows/0_single
execute if score #row_count shulker_preview matches 1.. positioned ~ ~1 ~ run function tryashtar.shulker_preview:bundle/rows/0_top
execute positioned ~ ~2 ~ run function tryashtar.shulker_preview:bundle/rows/full_return
execute if score #row_count shulker_preview matches 1 positioned ~ ~3 ~ run function tryashtar.shulker_preview:bundle/rows/1_bottom
execute if score #row_count shulker_preview matches 2.. positioned ~ ~3 ~ run function tryashtar.shulker_preview:bundle/rows/1_center
execute if score #row_count shulker_preview matches 1.. positioned ~ ~4 ~ run function tryashtar.shulker_preview:bundle/rows/full_return
execute if score #row_count shulker_preview matches 2 positioned ~ ~5 ~ run function tryashtar.shulker_preview:bundle/rows/2_bottom
execute if score #row_count shulker_preview matches 3.. positioned ~ ~5 ~ run function tryashtar.shulker_preview:bundle/rows/2_center
execute if score #row_count shulker_preview matches 2.. positioned ~ ~6 ~ run function tryashtar.shulker_preview:bundle/rows/full_return
execute if score #row_count shulker_preview matches 3.. positioned ~ ~7 ~ run function tryashtar.shulker_preview:bundle/rows/3_bottom
execute if score #row_count shulker_preview matches 3.. positioned ~ ~8 ~ run function tryashtar.shulker_preview:bundle/rows/full_return

# draw items
summon area_effect_cloud ~ ~9 ~ {Tags:["tryashtar.shulker_preview"],CustomName:'{"translate":"tryashtar.shulker_preview.positive_pixel"}'}
data modify storage tryashtar:shulker_preview running_contents set from storage tryashtar:shulker_preview contents
execute positioned ~ ~10 ~ run function tryashtar.shulker_preview:bundle/analyze_loop
execute if score #slots shulker_preview matches 1.. positioned ~ ~1000 ~ run function tryashtar.shulker_preview:bundle/rows/return
execute if score #row_count shulker_preview matches 1.. run scoreboard players operation #slots shulker_preview = #row_size shulker_preview
execute positioned ~ ~1001 ~ run function tryashtar.shulker_preview:bundle/rows/forward
