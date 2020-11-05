scoreboard players operation #ready shulker_preview = #loot_table shulker_preview
execute if score #ready shulker_preview matches 1 as @e[type=item,tag=!shulker_processed] run function tryashtar.shulker_preview:check_dropped
execute if score #ready shulker_preview matches 1 run function tryashtar.shulker_preview:check_players
