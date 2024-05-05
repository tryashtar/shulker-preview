scoreboard objectives add shulker_preview dummy "Shulker Box Preview"
scoreboard players set #256 shulker_preview 256
function tryashtar.shulker_preview:meta/initialize_data

function tryashtar.shulker_preview:meta/await_player

execute if score #ender_enabled shulker_preview matches 1 run function tryashtar.shulker_preview:ender_chest/tick
advancement revoke @a only tryashtar.shulker_preview:detect_shulker_box
advancement revoke @a only tryashtar.shulker_preview:detect_ender_chest
