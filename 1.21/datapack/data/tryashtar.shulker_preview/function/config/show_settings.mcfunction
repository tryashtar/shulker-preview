# display enabled status of shulker boxes and ender chests
# operators can click the icons to toggle each
execute store result storage tryashtar.shulker_preview:data settings.shulker_box byte 1 run scoreboard players get #shulker_enabled shulker_preview
execute store result storage tryashtar.shulker_preview:data settings.ender_chest byte 1 run scoreboard players get #ender_enabled shulker_preview
execute store result storage tryashtar.shulker_preview:data settings.colors byte 1 run scoreboard players get #colors_enabled shulker_preview
function tryashtar.shulker_preview:config/show_settings.macro with storage tryashtar.shulker_preview:data settings
