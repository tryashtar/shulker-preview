# render the base item texture
data modify entity @s Item set from storage tryashtar.shulker_preview:data item
execute if items entity @s contents #tryashtar.shulker_preview:special_render run function tryashtar.shulker_preview:render/row_0/special with storage tryashtar.shulker_preview:data item
execute unless items entity @s contents #tryashtar.shulker_preview:special_render run function tryashtar.shulker_preview:render/row_0/simple with storage tryashtar.shulker_preview:data item

# render some item-specific overlays
execute if items entity @s contents #banners if data storage tryashtar.shulker_preview:data item.components."minecraft:banner_patterns"[0] run function tryashtar.shulker_preview:render/row_0/overlay/banner_patterns
execute if items entity @s contents shield if data storage tryashtar.shulker_preview:data item.components."minecraft:base_color" run function tryashtar.shulker_preview:render/row_0/overlay/shield_base
execute if items entity @s contents shield if data storage tryashtar.shulker_preview:data item.components."minecraft:banner_patterns"[0] run function tryashtar.shulker_preview:render/row_0/overlay/shield_patterns
execute if data storage tryashtar.shulker_preview:data item.components."minecraft:pot_decorations" run function tryashtar.shulker_preview:render/row_0/overlay/pot_patterns1
execute if data storage tryashtar.shulker_preview:data item.components."minecraft:trim" run function tryashtar.shulker_preview:render/row_0/overlay/armor_trim

# render some generic overlays
# banner bundle is last since checking the weight involves overwriting the weapon item
execute if items entity @s contents *[damage~{damage:{min:1}},max_damage] run function tryashtar.shulker_preview:render/row_0/overlay/durability
execute if items entity @s contents *[count~{min:2}] run function tryashtar.shulker_preview:render/row_0/overlay/count with storage tryashtar.shulker_preview:data item
execute if items entity @s contents *[bundle_contents~{items:{size:{min:1}}}] run function tryashtar.shulker_preview:render/row_0/overlay/bundle_bar
