# items that require special rendering, like model overrides or colored layers
$data modify storage tryashtar.shulker_preview:data item merge from storage tryashtar.shulker_preview:data lookups.colors."$(id)"
execute if items entity @s contents #tryashtar.shulker_preview:special_render/overrides run return run function tryashtar.shulker_preview:render/row_1/special_render/overrides
execute if items entity @s contents #tryashtar.shulker_preview:special_render/grass_colored run return run function tryashtar.shulker_preview:render/row_1/special_render/grass_colored with storage tryashtar.shulker_preview:data item
execute if items entity @s contents #tryashtar.shulker_preview:special_render/spawn_eggs run return run function tryashtar.shulker_preview:render/row_1/special_render/spawn_eggs with storage tryashtar.shulker_preview:data item
execute if items entity @s contents #dyeable run return run function tryashtar.shulker_preview:render/row_1/special_render/dyeable1
execute if items entity @s contents #tryashtar.shulker_preview:special_render/potion run return run function tryashtar.shulker_preview:render/row_1/special_render/potion1
execute if items entity @s contents firework_star run return run function tryashtar.shulker_preview:render/row_1/special_render/star1
execute if items entity @s contents filled_map run return run function tryashtar.shulker_preview:render/row_1/special_render/map1
