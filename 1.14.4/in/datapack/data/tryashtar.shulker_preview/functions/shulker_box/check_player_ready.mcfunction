# if the player has any unprocessed boxes, we'll process one of them
execute store result score #boxes shulker_preview run clear @s #tryashtar.shulker_preview:shulker_boxes{BlockEntityTag:{Items:[{}]}} 0
execute store result score #processed shulker_preview run clear @s #tryashtar.shulker_preview:shulker_boxes{"shulker_preview.processed":1b} 0
execute if score #boxes shulker_preview > #processed shulker_preview run function tryashtar.shulker_preview:shulker_box/process_player

# keep the player flagged unless this was the last unprocessed box
# this has to run after processing, since modifying the player's inventory triggers the advancement
scoreboard players add #processed shulker_preview 1
execute if score #boxes shulker_preview <= #processed shulker_preview run tag @s remove shulker_preview.shulker_box
