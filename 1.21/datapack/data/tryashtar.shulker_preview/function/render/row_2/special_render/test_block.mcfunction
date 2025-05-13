# generated from the test_block model file
execute if data storage tryashtar.shulker_preview:data item.components."minecraft:block_state"{mode:"accept"} run return run data modify storage tryashtar.shulker_preview:data tooltip append value {translate:"tryashtar.shulker_preview.override.minecraft:test_block.2.2"}
execute if data storage tryashtar.shulker_preview:data item.components."minecraft:block_state"{mode:"fail"} run return run data modify storage tryashtar.shulker_preview:data tooltip append value {translate:"tryashtar.shulker_preview.override.minecraft:test_block.1.2"}
execute if data storage tryashtar.shulker_preview:data item.components."minecraft:block_state"{mode:"log"} run return run data modify storage tryashtar.shulker_preview:data tooltip append value {translate:"tryashtar.shulker_preview.override.minecraft:test_block.0.2"}
data modify storage tryashtar.shulker_preview:data tooltip append value {translate:"tryashtar.shulker_preview.item.minecraft:test_block.2"}
