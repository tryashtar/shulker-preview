execute if score #ender_enabled shulker_preview matches 1 run return fail
scoreboard players set #ender_enabled shulker_preview 1
function tryashtar.shulker_preview:ender_chest/tick
tellraw @s [{text:"Ender chest tooltips have been ",color:"#8fdff7"},{text:"enabled.",color:"#56d656"}]
