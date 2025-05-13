# generated from the crossbow model file
execute if data storage tryashtar.shulker_preview:data item.components."minecraft:charged_projectiles"[{id:"minecraft:firework_rocket"}] run return run data modify storage tryashtar.shulker_preview:data tooltip append value {translate:"tryashtar.shulker_preview.override.minecraft:crossbow.1.2"}
execute if data storage tryashtar.shulker_preview:data item.components."minecraft:charged_projectiles"[0] run return run data modify storage tryashtar.shulker_preview:data tooltip append value {translate:"tryashtar.shulker_preview.override.minecraft:crossbow.0.2"}
data modify storage tryashtar.shulker_preview:data tooltip append value {translate:"tryashtar.shulker_preview.item.minecraft:crossbow.2"}
