scoreboard objectives add shulker_preview dummy "Shulker Box Preview"
scoreboard players set #13000 shulker_preview 13000

# place the global shulker box, jukebox, and sign
forceload remove 29999977 9832
forceload add 29999977 9832
fill 29999976 0 9831 29999980 2 9833 bedrock
setblock 29999977 1 9832 shulker_box{CustomName:'"tryashtar Global Shulker Box®"'}
setblock 29999978 1 9832 jukebox
setblock 29999979 1 9832 birch_sign{Text1:'""',Text2:'"tryashtar"',Text3:'"Evaluation Sign®"',Text4:'""'}

scoreboard players add #setup shulker_preview 0
execute if score #setup shulker_preview matches 0 run schedule function tryashtar.shulker_preview:.meta/welcome_message 20t
scoreboard players set #setup shulker_preview 1

execute if score #ender_enabled shulker_preview matches 1 run function tryashtar.shulker_preview:ender_tick
advancement revoke @a only tryashtar.shulker_preview:detect_shulker_box
advancement revoke @a only tryashtar.shulker_preview:detect_ender_chest
