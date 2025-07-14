# main tick function
# look for any newly dropped items or players that are pending a scan
# only one box is processed per tick, so we keep the tag on players until they're processed
scoreboard players set #ready shulker_preview 1

# don't use "at", we need to run in the overworld where our special blocks are
execute if score #shulker_enabled shulker_preview matches 1 as @e[type=item,tag=!shulker_preview.checked] run function tryashtar.shulker_preview:shulker_box/check_dropped
execute if score #shulker_enabled shulker_preview matches 1 as @a[tag=shulker_preview.shulker_box] run function tryashtar.shulker_preview:shulker_box/check_player
execute if score #ender_enabled shulker_preview matches 1 as @a[tag=shulker_preview.ender_chest] positioned 29999977 1 9832 run function tryashtar.shulker_preview:ender_chest/check_player
