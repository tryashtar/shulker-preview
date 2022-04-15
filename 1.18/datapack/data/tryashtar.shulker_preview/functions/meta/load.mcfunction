scoreboard objectives add shulker_preview dummy "Shulker Box Preview"
scoreboard players set #2 shulker_preview 2
scoreboard players set #4 shulker_preview 4
scoreboard players set #5 shulker_preview 5
scoreboard players set #256 shulker_preview 256
scoreboard players set #65536 shulker_preview 65536
scoreboard players set #13000 shulker_preview 13000

function tryashtar.shulker_preview:meta/await_player

execute if score #ender_enabled shulker_preview matches 1 run function tryashtar.shulker_preview:ender_chest/tick
advancement revoke @a only tryashtar.shulker_preview:detect_shulker_box
advancement revoke @a only tryashtar.shulker_preview:detect_ender_chest
