execute store result score #expected_length shulker_preview run data get storage tryashtar:shulker_preview items[0].tag.shulker_length
execute store result score #actual_length shulker_preview run data get storage tryashtar:shulker_preview items[0].tag.display.Lore[0]

execute if score #actual_length shulker_preview < #expected_length shulker_preview run function tryashtar.shulker_preview:modded_fix_perform

data remove storage tryashtar:shulker_preview items[0]
execute if data storage tryashtar:shulker_preview items[0] run function tryashtar.shulker_preview:modded_fix_check_loop
