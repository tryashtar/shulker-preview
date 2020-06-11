# create an entity that draws the proper map overlay color
execute store result score #color shulker_preview run data get storage tryashtar:shulker_preview item.tag.display.MapColor
execute if score #color shulker_preview matches 3830373 run summon area_effect_cloud ~ ~0.1 ~ {Tags:["tryashtar.shulker_preview"],CustomName:'{"translate":"tryashtar.shulker_preview.overlay.filled_map_markings.1","color":"#3a7265"}'}
execute if score #color shulker_preview matches 5393476 run summon area_effect_cloud ~ ~0.1 ~ {Tags:["tryashtar.shulker_preview"],CustomName:'{"translate":"tryashtar.shulker_preview.overlay.filled_map_markings.1","color":"#524c44"}'}
execute unless score #color shulker_preview matches 3830373 unless score #color shulker_preview matches 5393476 run function tryashtar.shulker_preview:row_1/overlay/custom_map
