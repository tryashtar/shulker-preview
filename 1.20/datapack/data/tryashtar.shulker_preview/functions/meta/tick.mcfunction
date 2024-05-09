# main tick function
# look for any newly dropped items or players that are pending a scan
# only one box is processed per tick, so we keep the tag on players until they're processed
scoreboard players set #ready shulker_preview 1

execute if score #shulker_enabled shulker_preview matches 1 as @e[type=item,tag=!shulker_preview.checked] at @s run function tryashtar.shulker_preview:shulker_box/check_dropped
execute if score #shulker_enabled shulker_preview matches 1 as @a[tag=shulker_preview.shulker_box] at @s run function tryashtar.shulker_preview:shulker_box/check_player
execute if score #ender_enabled shulker_preview matches 1 as @a[tag=shulker_preview.ender_chest] at @s run function tryashtar.shulker_preview:ender_chest/check_player
