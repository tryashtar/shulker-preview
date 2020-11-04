execute if entity @s[tag=shulker_preview.shulker_box] run function tryashtar.shulker_preview:has_shulker_box
execute if score #ender_enabled shulker_preview matches 1 if entity @s[tag=shulker_preview.ender_chest] positioned 29999977 1 9832 run function tryashtar.shulker_preview:has_ender_chest
execute if entity @s[tag=shulker_preview.bundle] run function tryashtar.shulker_preview:has_bundle
