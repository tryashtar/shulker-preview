# main load function
# set up scoreboard and data
scoreboard objectives add shulker_preview dummy "Shulker Box Preview"
scoreboard players set #256 shulker_preview 256
function tryashtar.shulker_preview:meta/initialize_data

# wait until a player is online to show status messages
function tryashtar.shulker_preview:meta/await_player

# start up schedule loop for ender chest checking function
execute if score #ender_enabled shulker_preview matches 1 run function tryashtar.shulker_preview:ender_chest/tick

# these are supposed to revoke themselves, but clear them here too in case any get stuck
advancement revoke @a only tryashtar.shulker_preview:detect_shulker_box
advancement revoke @a only tryashtar.shulker_preview:detect_ender_chest
