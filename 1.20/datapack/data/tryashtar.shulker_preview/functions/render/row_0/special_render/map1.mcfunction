data modify storage tryashtar.shulker_preview:data item merge value {red:"46",green:"40","blue":"2e"}
execute store success score #has_color shulker_preview store result score #color shulker_preview run data get storage tryashtar.shulker_preview:data item.components."minecraft:map_color"
execute if score #has_color shulker_preview matches 1 run function tryashtar.shulker_preview:render/convert_color
function tryashtar.shulker_preview:render/row_0/special_render/map2 with storage tryashtar.shulker_preview:data item
