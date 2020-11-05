execute as @a[tag=shulker_preview.shulker_box] run function tryashtar.shulker_preview:shulker_box/scan
execute if score #ender_enabled shulker_preview matches 1 as @a[tag=shulker_preview.ender_chest] positioned 29999977 1 9832 run function tryashtar.shulker_preview:ender_chest/scan
execute as @a[tag=shulker_preview.bundle] run function tryashtar.shulker_preview:bundle/scan
