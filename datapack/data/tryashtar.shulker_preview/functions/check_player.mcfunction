# cheaply check if there are any unprocessed boxes
execute store result score #boxes shulker_preview if data entity @s Inventory[{tag:{BlockEntityTag:{Items:[{}]}}}]
execute store result score #processed shulker_preview if data entity @s Inventory[{tag:{shulker_processed:1b}}]

# if there are, expensively process them
execute if score #ready shulker_preview matches 1 if score #boxes shulker_preview > #processed shulker_preview if score #setup shulker_preview matches 1 positioned 29999976 1 9832 run function tryashtar.shulker_preview:process_player
