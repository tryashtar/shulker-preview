# render the armor trim overlay texture based on the type of armor this is
execute if items entity @s contents #head_armor run return run function tryashtar.shulker_preview:render/row_0/overlay/armor_trim/helmet
execute if items entity @s contents #chest_armor run return run function tryashtar.shulker_preview:render/row_0/overlay/armor_trim/chestplate
execute if items entity @s contents #leg_armor run return run function tryashtar.shulker_preview:render/row_0/overlay/armor_trim/leggings
execute if items entity @s contents #foot_armor run return run function tryashtar.shulker_preview:render/row_0/overlay/armor_trim/boots
