function tryashtar.shulker_preview:banner_color with storage tryashtar.shulker_preview:data item.components."minecraft:banner_patterns"[0]
function tryashtar.shulker_preview:render/row_2/overlay/shield_patterns_one with storage tryashtar.shulker_preview:data item.components."minecraft:banner_patterns"[0]
data remove storage tryashtar.shulker_preview:data item.components."minecraft:banner_patterns"[0]
execute if data storage tryashtar.shulker_preview:data item.components."minecraft:banner_patterns"[0] run function tryashtar.shulker_preview:render/row_2/overlay/shield_patterns_loop
