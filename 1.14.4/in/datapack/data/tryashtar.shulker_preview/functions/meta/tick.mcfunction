# only one box is processed per tick
# this prevents freezing the server, or worse, blowing past maxCommandChainLength,
# if an unknowing or malicious player breaks tons of shulker boxes in the same tick
scoreboard players set #ready shulker_preview 1

# advancements add tags to players that are worth checking
# don't use "at", we need to run in the overworld where our special blocks are
execute if score #shulker_enabled shulker_preview matches 1 as @e[type=item,tag=!shulker_preview.checked] positioned 29999977 1 9832 run function tryashtar.shulker_preview:shulker_box/check_dropped
execute if score #shulker_enabled shulker_preview matches 1 as @a[tag=shulker_preview.shulker_box] positioned 29999977 1 9832 run function tryashtar.shulker_preview:shulker_box/check_player
execute if score #ender_enabled shulker_preview matches 1 as @a[tag=shulker_preview.ender_chest] positioned 29999977 1 9832 run function tryashtar.shulker_preview:ender_chest/check_player
