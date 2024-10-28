# generated from the beehive model file
execute if data storage tryashtar.shulker_preview:data item.components."minecraft:block_state"{honey_level:"5"} run return run data modify storage tryashtar.shulker_preview:data tooltip append value '{"translate":"tryashtar.shulker_preview.override.minecraft:beehive.1.1"}'
execute unless data storage tryashtar.shulker_preview:data item.components."minecraft:block_state"{honey_level:"5"} run return run data modify storage tryashtar.shulker_preview:data tooltip append value '{"translate":"tryashtar.shulker_preview.override.minecraft:beehive.0.1"}'
data modify storage tryashtar.shulker_preview:data tooltip append value '{"translate":"tryashtar.shulker_preview.item.minecraft:beehive.1"}'
