scoreboard objectives add shulker_preview dummy "Shulker Box Preview"
scoreboard players set #13000 shulker_preview 13000
execute store success score #setup shulker_preview run forceload query 29999977 9832
execute unless score #setup shulker_preview matches 1 run schedule function tryashtar.shulker_preview:.meta/check_setup 1s
execute if score #ender_enabled shulker_preview matches 1 run function tryashtar.shulker_preview:ender_tick

advancement revoke @a only tryashtar.shulker_preview:detect_shulker_box
advancement revoke @a only tryashtar.shulker_preview:detect_ender_chest
