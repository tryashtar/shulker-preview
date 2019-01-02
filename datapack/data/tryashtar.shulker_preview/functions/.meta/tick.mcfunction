scoreboard players set #ready shulker_preview 1
execute as @a run function tryashtar.shulker_preview:check_player
execute if score #ready shulker_preview matches 1 as @e[type=item,tag=!shulker_processed] run function tryashtar.shulker_preview:check_item
