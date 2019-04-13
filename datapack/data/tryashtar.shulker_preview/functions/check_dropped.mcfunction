execute if score #ready shulker_preview matches 1 run tag @s add shulker_processed
execute if score #ready shulker_preview matches 1 at @s[nbt={Item:{tag:{BlockEntityTag:{Items:[{}]}}}},nbt=!{Item:{tag:{shulker_processed:1b}}}] run function tryashtar.shulker_preview:from_dropped
