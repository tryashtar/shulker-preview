scoreboard players operation #ready shulker_preview = #loot_table shulker_preview
execute as @e[type=item,tag=!shulker_processed] run function tryashtar.shulker_preview:check_dropped

execute if score #shulker_enabled shulker_preview matches 1 as @a[tag=shulker_preview.shulker_box] run function tryashtar.shulker_preview:shulker_box/scan
execute if score #ender_enabled shulker_preview matches 1 as @a[tag=shulker_preview.ender_chest] positioned 29999977 1 9832 run function tryashtar.shulker_preview:ender_chest/scan

# the advancement optimization doesn't work well with bundles because of MC-117653 
execute if score #bundle_enabled shulker_preview matches 1 as @a run function tryashtar.shulker_preview:bundle/scan
