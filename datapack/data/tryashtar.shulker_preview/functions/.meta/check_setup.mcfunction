# loading a distant chunk is necessary for the global shulker box and sign
# nag the player until they do it, since functions can't run forceload
scoreboard players enable @a shulker_trigger
execute if score #setup shulker_preview matches 0 store success score #setup shulker_preview run forceload query 29999977 9832
execute if score #setup shulker_preview matches 1 positioned 29999977 1 9832 run function tryashtar.shulker_preview:.meta/setup
execute if score #setup shulker_preview matches 0 if entity @a[scores={shulker_trigger=1..},limit=1] run scoreboard players set #setup shulker_preview 2
execute if score #setup shulker_preview matches 2 run schedule function tryashtar.shulker_preview:.meta/setup 1t
execute if score #setup shulker_preview matches 0 run schedule function tryashtar.shulker_preview:.meta/check_setup 5s
execute if score #setup shulker_preview matches 0 run tellraw @a {"translate":"If you can see this, you still need to equip the resource pack!","with":[[{"text":"\n\n\n\uE337\n     ","color":"white"},{"text":"Welcome! Real quick, we need to do some one-time setup.\n\n","color":"green"},{"text":"[Click here]","clickEvent":{"action":"run_command","value":"/execute if score #setup shulker_preview matches 0 in overworld run forceload add 29999977 9832"},"color":"blue","underlined":true},{"text":" if you have cheats enabled or operator access.\n\n","color":"yellow"},{"text":"[Click here]","clickEvent":{"action":"run_command","value":"/trigger shulker_trigger"},"color":"light_purple","underlined":true},{"text":" if you're on Realms or can't use cheats.","color":"yellow"}]],"color":"red"}
