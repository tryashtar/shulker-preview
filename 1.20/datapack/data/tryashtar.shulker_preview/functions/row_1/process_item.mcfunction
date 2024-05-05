data modify entity @s Item set from storage tryashtar.shulker_preview:data item
execute if items entity @s contents #tryashtar.shulker_preview:special_render run function tryashtar.shulker_preview:row_1/special_render with storage tryashtar.shulker_preview:data item
execute unless items entity @s contents #tryashtar.shulker_preview:special_render run function tryashtar.shulker_preview:row_1/simple_render with storage tryashtar.shulker_preview:data item
execute if items entity @s contents *[damage~{damage:{min:1}},max_damage] run function tryashtar.shulker_preview:row_1/overlay/durability
execute if items entity @s contents *[count~{min:2}] run function tryashtar.shulker_preview:row_1/overlay/count
