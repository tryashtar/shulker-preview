scoreboard players set #shulker_enabled shulker_preview 0
function tryashtar.shulker_preview:config/show_settings
tellraw @a [{"text":"⚠ ","color":"#ebdd23"},{"text":"Existing items will not be updated until they are placed and broken.","color":"#f06e6e"}]
