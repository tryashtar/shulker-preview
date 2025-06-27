execute if score #shulker_enabled shulker_preview matches 1 run return fail
scoreboard players set #shulker_enabled shulker_preview 1
tellraw @s [{text:"Shulker box tooltips have been ",color:"#8fdff7"},{text:"enabled.",color:"#56d656"}]
