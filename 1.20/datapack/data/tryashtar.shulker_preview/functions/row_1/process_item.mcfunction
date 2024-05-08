data modify entity @s HandItems[0] set from storage tryashtar.shulker_preview:data item
execute if items entity @s weapon #tryashtar.shulker_preview:special_render run function tryashtar.shulker_preview:row_1/special_render with storage tryashtar.shulker_preview:data item
execute unless items entity @s weapon #tryashtar.shulker_preview:special_render run function tryashtar.shulker_preview:row_1/simple_render with storage tryashtar.shulker_preview:data item
execute if data storage tryashtar.shulker_preview:data item.components."minecraft:banner_patterns"[0] run function tryashtar.shulker_preview:row_1/overlay/banner_patterns
execute if data storage tryashtar.shulker_preview:data item.components."minecraft:pot_decorations" run function tryashtar.shulker_preview:row_1/overlay/pot_patterns1
execute if items entity @s weapon *[damage~{damage:{min:1}},max_damage] run function tryashtar.shulker_preview:row_1/overlay/durability
execute if items entity @s weapon *[count~{min:2}] run function tryashtar.shulker_preview:row_1/overlay/count with storage tryashtar.shulker_preview:data item
