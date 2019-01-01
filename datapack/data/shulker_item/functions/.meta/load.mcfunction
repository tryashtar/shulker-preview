scoreboard objectives add shulker_item dummy "Shulker Box Preview"
scoreboard players set #140 shulker_item 140
execute unless score #setup shulker_item matches 1 run schedule function shulker_item:.meta/check_setup 1t
