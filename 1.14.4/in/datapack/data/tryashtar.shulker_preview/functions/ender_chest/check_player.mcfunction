# do nothing if a box was already processed this tick
# these checks need to go here because the functions get queued before executing

# we're always finished with ender chests in one go
execute if score #ready shulker_preview matches 1 run tag @s remove shulker_preview.ender_chest

# check for any ender chests
# there's no such thing as an "already processed" ender chest, both new and old need to have the exact same lore to stack
# so every time, all chests in the player's inventory get modified
execute if score #ready shulker_preview matches 1 store result score #ender_chests shulker_preview run clear @s ender_chest 0
execute if score #ready shulker_preview matches 1 if score #ender_chests shulker_preview matches 1.. run function tryashtar.shulker_preview:ender_chest/process_player

