# loading a distant chunk is necessary for the global shulker box and sign
# nag the player until they do it, since functions can't run forceload
execute store success score #setup shulker_preview run forceload query 29999977 9832
execute if score #setup shulker_preview matches 1 run function tryashtar.shulker_preview:.meta/setup
execute unless score #setup shulker_preview matches 1 run schedule function tryashtar.shulker_preview:.meta/check_setup 5s
execute unless score #setup shulker_preview matches 1 run tellraw @a {"translate":"If you can see this, you still need to equip the resource pack!","with":[[{"text":"\uE336\n     ","color":"white"},{"text":"Welcome! Click this text to finalize installation\nof the Shulker Box tooltip preview pack.","color":"green","clickEvent":{"action":"run_command","value":"/execute in overworld run forceload add 29999977 9832"}}]],"color":"red"}
