scoreboard objectives add shulker_item dummy
execute unless score #setup shulker_item matches 1 run schedule function shulker_item:.meta/check_setup 5s
