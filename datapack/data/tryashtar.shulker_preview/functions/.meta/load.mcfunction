scoreboard objectives add shulker_preview dummy "Shulker Box Preview"
scoreboard objectives add shulker_trigger trigger "Shulker Box Trigger"
scoreboard players set #13000 shulker_preview 13000
scoreboard players add #setup shulker_preview 0
execute if score #setup shulker_preview matches 1 store success score #setup shulker_preview run forceload query 29999977 9832
execute if score #setup shulker_preview matches 0 run schedule function tryashtar.shulker_preview:.meta/check_setup 1s
execute if score #setup shulker_preview matches 1 unless entity 0-1c9-c369-0-2668 run summon area_effect_cloud 29999977 1 9832 {UUIDMost:29999977L,UUIDLeast:9832L,CustomName:'"Shulker Marker"',Age:-2147483648,Duration:-1,WaitTime:-2147483648}
execute if score #setup shulker_preview matches 2 unless entity 0-1c9-c369-0-2668 run summon area_effect_cloud ~ 1 ~ {UUIDMost:29999977L,UUIDLeast:9832L,CustomName:'"Shulker Marker"',Age:-2147483648,Duration:-1,WaitTime:-2147483648}
execute if score #ender_enabled shulker_preview matches 1 run function tryashtar.shulker_preview:ender_tick

advancement revoke @a only tryashtar.shulker_preview:detect_shulker_box
advancement revoke @a only tryashtar.shulker_preview:detect_ender_chest
