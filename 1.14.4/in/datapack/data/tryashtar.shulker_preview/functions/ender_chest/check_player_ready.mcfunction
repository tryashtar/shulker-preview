# if the player has any ender chests, we need to update them all
execute store result score #ender_chests shulker_preview run clear @s ender_chest 0
execute if score #ender_chests shulker_preview matches 1.. run function tryashtar.shulker_preview:ender_chest/process_player

# since we updated every ender chest, we're done with this player
# this has to run after processing, since modifying the player's inventory triggers the advancement
tag @s remove shulker_preview.ender_chest
