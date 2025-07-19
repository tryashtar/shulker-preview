# do nothing if a box was already processed this tick
# these checks need to go here because the functions get queued before executing

# check for any unprocessed boxes
execute if score #ready shulker_preview matches 1 store result score #boxes shulker_preview run clear @s #tryashtar.shulker_preview:shulker_boxes{BlockEntityTag:{Items:[{}]}} 0
execute if score #ready shulker_preview matches 1 store result score #processed shulker_preview run clear @s #tryashtar.shulker_preview:shulker_boxes{"shulker_preview.processed":1b} 0
execute if score #ready shulker_preview matches 1 if score #boxes shulker_preview > #processed shulker_preview run function tryashtar.shulker_preview:shulker_box/process_player

# if there are more boxes to process next tick, keep the player flagged
scoreboard players add #processed shulker_preview 1
execute if score #ready shulker_preview matches 1 if score #boxes shulker_preview <= #processed shulker_preview run tag @s remove shulker_preview.shulker_box
