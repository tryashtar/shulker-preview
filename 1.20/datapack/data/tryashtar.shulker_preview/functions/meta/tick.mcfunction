scoreboard players set #ready shulker_preview 1
execute if score #shulker_enabled shulker_preview matches 1 as @e[type=item,tag=!shulker_processed] at @s run function tryashtar.shulker_preview:check_dropped

execute if score #shulker_enabled shulker_preview matches 1 as @a[tag=shulker_preview.shulker_box] at @s run function tryashtar.shulker_preview:shulker_box/scan
execute if score #ender_enabled shulker_preview matches 1 as @a[tag=shulker_preview.ender_chest] at @s run function tryashtar.shulker_preview:ender_chest/scan
