# cheaply check if there are any unprocessed boxes
execute store result score #boxes shulker_preview run clear @s #tryashtar.shulker_preview:shulker_boxes{BlockEntityTag:{Items:[{}]}} 0
execute store result score #processed shulker_preview run clear @s #tryashtar.shulker_preview:shulker_boxes{shulker_processed:1b} 0

# if there are, expensively process them
execute if score #ready shulker_preview matches 1 if score #boxes shulker_preview > #processed shulker_preview if score #setup shulker_preview matches 1 at @s run function tryashtar.shulker_preview:check_shulker_box

execute if score #boxes shulker_preview <= #processed shulker_preview run tag @s remove shulker_preview.shulker_box
