execute if score #shulker_enabled shulker_preview matches 0 run return fail
scoreboard players set #shulker_enabled shulker_preview 0
tellraw @s [{text:"Shulker box tooltips have been ",color:"#8fdff7"},{text:"disabled.",color:"#f06e6e"},{text:"\n⚠ ",color:"#ebdd23"},{text:"Existing items will not be updated until they are placed and broken.",color:"gray"}]
