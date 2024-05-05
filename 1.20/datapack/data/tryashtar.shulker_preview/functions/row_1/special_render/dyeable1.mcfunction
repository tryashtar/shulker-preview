data modify storage tryashtar.shulker_preview:data item merge value {red:"A0",green:"65",blue:"40"}
execute store success score #has_color shulker_preview store result score #color shulker_preview run data get storage tryashtar.shulker_preview:data item.components."minecraft:dyed_color".rgb
execute if score #has_color shulker_preview matches 1 run function tryashtar.shulker_preview:convert_color
function tryashtar.shulker_preview:row_1/special_render/dyeable2 with storage tryashtar.shulker_preview:data item
