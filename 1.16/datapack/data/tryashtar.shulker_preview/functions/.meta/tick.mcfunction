scoreboard players operation #ready shulker_preview = #loot_table shulker_preview
execute if score #ready shulker_preview matches 1 if score #shulker_enabled shulker_preview matches 1 as @e[type=item,tag=!shulker_processed] at @s run function tryashtar.shulker_preview:check_dropped
execute if score #loot_table shulker_preview matches 1 if score #shulker_enabled shulker_preview matches 1 as @a at @s run function tryashtar.shulker_preview:player_tick
