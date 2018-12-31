scoreboard objectives add shulker_item dummy "Shulker Box Preview"
scoreboard players set #14 shulker_item 14
execute unless score #setup shulker_item matches 1 run schedule function shulker_item:.meta/check_setup 1t
