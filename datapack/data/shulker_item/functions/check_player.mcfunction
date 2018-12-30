# cheaply check if there are any unprocessed boxes
execute store result score #boxes shulker_item run clear @s #shulker_item:container{BlockEntityTag:{Items:[{}]}} 0
execute store result score #processed shulker_item run clear @s #shulker_item:container{shulker_processed:1b} 0

# if there are, expensively process them
execute if score #boxes shulker_item > #processed shulker_item run function shulker_item:process_player
