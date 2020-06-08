scoreboard objectives add shulker_preview dummy "Shulker Box Preview"
scoreboard players set #2 shulker_preview 2
scoreboard players set #4 shulker_preview 4
scoreboard players set #256 shulker_preview 256
scoreboard players set #65536 shulker_preview 65536
scoreboard players set #13000 shulker_preview 13000

# place the global shulker box and signs
forceload remove 29999977 9832
forceload add 29999977 9832
fill 29999976 0 9831 29999981 2 9833 bedrock
setblock 29999977 1 9832 shulker_box{CustomName:'"tryashtar Global Shulker Box®"'}
setblock 29999979 1 9832 birch_sign{Text1:'""',Text2:'"tryashtar"',Text3:'"Evaluation Sign®"',Text4:'""'}
setblock 29999980 1 9832 birch_sign{Text1:'""',Text2:'"tryashtar"',Text3:'"Evaluation Sign®"',Text4:'""'}

function tryashtar.shulker_preview:.meta/await_player

execute if score #ender_enabled shulker_preview matches 1 run function tryashtar.shulker_preview:ender_tick
advancement revoke @a only tryashtar.shulker_preview:detect_shulker_box
advancement revoke @a only tryashtar.shulker_preview:detect_ender_chest
