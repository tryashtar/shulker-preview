# potions can be any color, so a macro is needed
data modify storage tryashtar.shulker_preview:data item merge value {red:"38",green:"5d","blue":"c6"}
execute store success score #has_color shulker_preview store result score #color shulker_preview run data get storage tryashtar.shulker_preview:data item.components."minecraft:potion_contents".custom_color
execute if score #has_color shulker_preview matches 1 run function tryashtar.shulker_preview:render/convert_color
execute if score #has_color shulker_preview matches 0 run function tryashtar.shulker_preview:render/potion_color
function tryashtar.shulker_preview:render/row_2/special_render/potion2 with storage tryashtar.shulker_preview:data item
