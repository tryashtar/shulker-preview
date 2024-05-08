data modify entity @s HandItems[0] set from storage tryashtar.shulker_preview:data item
execute if items entity @s weapon #tryashtar.shulker_preview:special_render run function tryashtar.shulker_preview:row_2/special_render with storage tryashtar.shulker_preview:data item
execute unless items entity @s weapon #tryashtar.shulker_preview:special_render run function tryashtar.shulker_preview:row_2/simple_render with storage tryashtar.shulker_preview:data item
execute if items entity @s weapon #banners[banner_patterns] run function tryashtar.shulker_preview:row_2/overlay/banner_patterns
execute if items entity @s weapon *[damage~{damage:{min:1}},max_damage] run function tryashtar.shulker_preview:row_2/overlay/durability
execute if items entity @s weapon *[count~{min:2}] run function tryashtar.shulker_preview:row_2/overlay/count with storage tryashtar.shulker_preview:data item
