# cheaply check if there are any unprocessed boxes
execute store result score #boxes shulker_preview run clear @s #tryashtar.shulker_preview:container{BlockEntityTag:{Items:[{}]}} 0
execute store result score #processed shulker_preview run clear @s #tryashtar.shulker_preview:container{shulker_processed:1b} 0

# if there are, expensively process them
execute if score #ready shulker_preview matches 1 if score #boxes shulker_preview > #processed shulker_preview if score #setup shulker_preview matches 1 at @s run function tryashtar.shulker_preview:process_player
