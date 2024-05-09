# render the armor trim overlay texture based on the material color
# it's not as accurate as the true items which use paletted permutations
# items of a matching material use a darker color as well
execute if data storage tryashtar.shulker_preview:data item.components{"minecraft:trim":{material:"minecraft:amethyst"}} run return run data modify storage tryashtar.shulker_preview:data tooltip append value '[{"translate":"tryashtar.shulker_preview.overlay"},{"translate":"tryashtar.shulker_preview.overlay.trim.boots.1","color":"#c98ff3"},{"translate":"tryashtar.shulker_preview.overlay_done"}]'
execute if data storage tryashtar.shulker_preview:data item.components{"minecraft:trim":{material:"minecraft:copper"}} run return run data modify storage tryashtar.shulker_preview:data tooltip append value '[{"translate":"tryashtar.shulker_preview.overlay"},{"translate":"tryashtar.shulker_preview.overlay.trim.boots.1","color":"#e3826c"},{"translate":"tryashtar.shulker_preview.overlay_done"}]'
execute if data storage tryashtar.shulker_preview:data item.components{"minecraft:trim":{material:"minecraft:diamond"}} if items entity @s contents #tryashtar.shulker_preview:armor_material/diamond run return run data modify storage tryashtar.shulker_preview:data tooltip append value '[{"translate":"tryashtar.shulker_preview.overlay"},{"translate":"tryashtar.shulker_preview.overlay.trim.boots.1","color":"#15b3a1"},{"translate":"tryashtar.shulker_preview.overlay_done"}]'
execute if data storage tryashtar.shulker_preview:data item.components{"minecraft:trim":{material:"minecraft:diamond"}} run return run data modify storage tryashtar.shulker_preview:data tooltip append value '[{"translate":"tryashtar.shulker_preview.overlay"},{"translate":"tryashtar.shulker_preview.overlay.trim.boots.1","color":"#cbfff5"},{"translate":"tryashtar.shulker_preview.overlay_done"}]'
execute if data storage tryashtar.shulker_preview:data item.components{"minecraft:trim":{material:"minecraft:emerald"}} run return run data modify storage tryashtar.shulker_preview:data tooltip append value '[{"translate":"tryashtar.shulker_preview.overlay"},{"translate":"tryashtar.shulker_preview.overlay.trim.boots.1","color":"#82f6ad"},{"translate":"tryashtar.shulker_preview.overlay_done"}]'
execute if data storage tryashtar.shulker_preview:data item.components{"minecraft:trim":{material:"minecraft:gold"}} if items entity @s contents #tryashtar.shulker_preview:armor_material/gold run return run data modify storage tryashtar.shulker_preview:data tooltip append value '[{"translate":"tryashtar.shulker_preview.overlay"},{"translate":"tryashtar.shulker_preview.overlay.trim.boots.1","color":"#c29c2a"},{"translate":"tryashtar.shulker_preview.overlay_done"}]'
execute if data storage tryashtar.shulker_preview:data item.components{"minecraft:trim":{material:"minecraft:gold"}} run return run data modify storage tryashtar.shulker_preview:data tooltip append value '[{"translate":"tryashtar.shulker_preview.overlay"},{"translate":"tryashtar.shulker_preview.overlay.trim.boots.1","color":"#fffd90"},{"translate":"tryashtar.shulker_preview.overlay_done"}]'
execute if data storage tryashtar.shulker_preview:data item.components{"minecraft:trim":{material:"minecraft:iron"}} if items entity @s contents #tryashtar.shulker_preview:armor_material/iron run return run data modify storage tryashtar.shulker_preview:data tooltip append value '[{"translate":"tryashtar.shulker_preview.overlay"},{"translate":"tryashtar.shulker_preview.overlay.trim.boots.1","color":"#a2b0b3"},{"translate":"tryashtar.shulker_preview.overlay_done"}]'
execute if data storage tryashtar.shulker_preview:data item.components{"minecraft:trim":{material:"minecraft:iron"}} run return run data modify storage tryashtar.shulker_preview:data tooltip append value '[{"translate":"tryashtar.shulker_preview.overlay"},{"translate":"tryashtar.shulker_preview.overlay.trim.boots.1","color":"#c5d2d4"},{"translate":"tryashtar.shulker_preview.overlay_done"}]'
execute if data storage tryashtar.shulker_preview:data item.components{"minecraft:trim":{material:"minecraft:lapis"}} run return run data modify storage tryashtar.shulker_preview:data tooltip append value '[{"translate":"tryashtar.shulker_preview.overlay"},{"translate":"tryashtar.shulker_preview.overlay.trim.boots.1","color":"#416e97"},{"translate":"tryashtar.shulker_preview.overlay_done"}]'
execute if data storage tryashtar.shulker_preview:data item.components{"minecraft:trim":{material:"minecraft:netherite"}} if items entity @s contents #tryashtar.shulker_preview:armor_material/netherite run return run data modify storage tryashtar.shulker_preview:data tooltip append value '[{"translate":"tryashtar.shulker_preview.overlay"},{"translate":"tryashtar.shulker_preview.overlay.trim.boots.1","color":"#2e2829"},{"translate":"tryashtar.shulker_preview.overlay_done"}]'
execute if data storage tryashtar.shulker_preview:data item.components{"minecraft:trim":{material:"minecraft:netherite"}} run return run data modify storage tryashtar.shulker_preview:data tooltip append value '[{"translate":"tryashtar.shulker_preview.overlay"},{"translate":"tryashtar.shulker_preview.overlay.trim.boots.1","color":"#5a575a"},{"translate":"tryashtar.shulker_preview.overlay_done"}]'
execute if data storage tryashtar.shulker_preview:data item.components{"minecraft:trim":{material:"minecraft:quartz"}} run return run data modify storage tryashtar.shulker_preview:data tooltip append value '[{"translate":"tryashtar.shulker_preview.overlay"},{"translate":"tryashtar.shulker_preview.overlay.trim.boots.1","color":"#f2efed"},{"translate":"tryashtar.shulker_preview.overlay_done"}]'
execute if data storage tryashtar.shulker_preview:data item.components{"minecraft:trim":{material:"minecraft:redstone"}} run return run data modify storage tryashtar.shulker_preview:data tooltip append value '[{"translate":"tryashtar.shulker_preview.overlay"},{"translate":"tryashtar.shulker_preview.overlay.trim.boots.1","color":"#e62008"},{"translate":"tryashtar.shulker_preview.overlay_done"}]'
