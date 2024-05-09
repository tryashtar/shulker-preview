# firework stars can be any color, so a macro is needed
data modify storage tryashtar.shulker_preview:data item merge value {red:"8a",green:"8a","blue":"8a"}
function tryashtar.shulker_preview:render/star_color
function tryashtar.shulker_preview:render/row_1/special_render/star2 with storage tryashtar.shulker_preview:data item
