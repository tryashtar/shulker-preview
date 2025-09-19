# set up scoreboard
# it's mostly #-prefixed fake players, but is also used to cache players' ender chest contents size
scoreboard objectives add shulker_preview dummy "Shulker Box Preview"
scoreboard players set #13000 shulker_preview 13000

# place the global shulker box and jukebox
forceload remove 29999977 9832
forceload add 29999977 9832
fill 29999976 0 9831 29999979 2 9833 bedrock
setblock 29999977 1 9832 shulker_box
setblock 29999978 1 9832 jukebox

# wait until a player is online to show status messages
function tryashtar.shulker_preview:meta/await_player

# start up schedule loop for ender chest checking function
execute if score #ender_enabled shulker_preview matches 1 run function tryashtar.shulker_preview:ender_chest/tick

# these are supposed to revoke themselves, but clear them here too in case any get stuck
advancement revoke @a only tryashtar.shulker_preview:detect_shulker_box
advancement revoke @a only tryashtar.shulker_preview:detect_ender_chest
