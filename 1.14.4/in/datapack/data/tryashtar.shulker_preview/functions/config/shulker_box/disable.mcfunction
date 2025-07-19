scoreboard players set #shulker_enabled shulker_preview 0
function tryashtar.shulker_preview:config/show_settings
tellraw @a [{"text":"⚠ ","color":"yellow"},{"text":"Existing items will not be updated until they are placed and broken.","color":"red"}]
