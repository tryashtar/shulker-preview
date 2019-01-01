scoreboard objectives add shulker_preview dummy "Shulker Box Preview"
scoreboard players set #140 shulker_preview 140
execute unless score #setup shulker_preview matches 1 run schedule function tryashtar.shulker_preview:.meta/check_setup 1t
