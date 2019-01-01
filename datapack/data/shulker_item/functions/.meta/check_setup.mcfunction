# loading a distant chunk is necessary for the global shulker box and sign
# nag the player until they do it, since functions can't run forceload
execute unless score #setup shulker_item matches 1 if blocks 29999976 0 9832 29999976 0 9832 29999976 0 9832 all run function shulker_item:.meta/setup
execute if score #setup shulker_item matches 1 run tellraw @a {"text":"Success! Thank you and enjoy.","color":"yellow"}
execute unless score #setup shulker_item matches 1 run schedule function shulker_item:.meta/check_setup 5s
execute unless score #setup shulker_item matches 1 run tellraw @a {"translate":"If you can see this, you still need to equip the resource pack!","with":[[{"text":"\uE370\n     ","color":"white"},{"text":"Welcome! Click this text to finalize installation of the Shulker Box tooltip preview pack.","color":"green","clickEvent":{"action":"run_command","value":"/forceload add 29999976 9832"}}]],"color":"red"}
