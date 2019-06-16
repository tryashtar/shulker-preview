execute if score #ready shulker_preview matches 1 run tag @s add shulker_processed
execute if score #ready shulker_preview matches 1 if entity @s[nbt={Item:{tag:{BlockEntityTag:{Items:[{}]}}}},nbt=!{Item:{tag:{shulker_processed:1b}}}] at 0-1c9-c369-0-2668 run function tryashtar.shulker_preview:from_dropped
