# generated from the bee_nest model file
execute if data storage tryashtar.shulker_preview:data item.components."minecraft:block_state"{honey_level:"5"} run return run data modify storage tryashtar.shulker_preview:data tooltip append value '{"translate":"tryashtar.shulker_preview.override.minecraft:bee_nest.1.2"}'
execute unless data storage tryashtar.shulker_preview:data item.components."minecraft:block_state"{honey_level:"5"} run return run data modify storage tryashtar.shulker_preview:data tooltip append value '{"translate":"tryashtar.shulker_preview.override.minecraft:bee_nest.0.2"}'
data modify storage tryashtar.shulker_preview:data tooltip append value '{"translate":"tryashtar.shulker_preview.item.minecraft:bee_nest.2"}'
