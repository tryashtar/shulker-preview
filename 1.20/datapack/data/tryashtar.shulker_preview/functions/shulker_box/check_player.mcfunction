# exit immediately if a box was already processed this tick
# this check needs to go here because the functions get queued before executing
execute unless score #ready shulker_preview matches 1 run return fail

# check for any unprocessed boxes
execute store result score #boxes shulker_preview run clear @s #tryashtar.shulker_preview:shulker_boxes[!custom_data~{"shulker_preview.processed":1b},container~{items:{size:{min:1}}}] 0
execute if score #boxes shulker_preview matches 1.. run function tryashtar.shulker_preview:shulker_box/process

# if there are more boxes to process next tick, keep the player flagged
execute if score #boxes shulker_preview matches ..1 run tag @s remove shulker_preview.shulker_box
