# render the fullness bar of a bundle
# set up a stack to be used in case of bundle nesting, get the weight, then check against some thresholds to get the bar width
scoreboard players set #fullness shulker_preview 0
data modify storage tryashtar.shulker_preview:data bundle_stack set value [{fullness:0}]
data modify storage tryashtar.shulker_preview:data bundle_stack[0].contents set from storage tryashtar.shulker_preview:data item.components."minecraft:bundle_contents"
function tryashtar.shulker_preview:render/bundle_weight
execute if score #fullness shulker_preview matches 64000.. run return run data modify storage tryashtar.shulker_preview:data tooltip append value '{"translate":"tryashtar.shulker_preview.durability.0.2","color":"#6666ff"}'
execute if score #fullness shulker_preview matches 59000.. run return run data modify storage tryashtar.shulker_preview:data tooltip append value '{"translate":"tryashtar.shulker_preview.durability.1.2","color":"#6666ff"}'
execute if score #fullness shulker_preview matches 54000.. run return run data modify storage tryashtar.shulker_preview:data tooltip append value '{"translate":"tryashtar.shulker_preview.durability.2.2","color":"#6666ff"}'
execute if score #fullness shulker_preview matches 48000.. run return run data modify storage tryashtar.shulker_preview:data tooltip append value '{"translate":"tryashtar.shulker_preview.durability.3.2","color":"#6666ff"}'
execute if score #fullness shulker_preview matches 43000.. run return run data modify storage tryashtar.shulker_preview:data tooltip append value '{"translate":"tryashtar.shulker_preview.durability.4.2","color":"#6666ff"}'
execute if score #fullness shulker_preview matches 38000.. run return run data modify storage tryashtar.shulker_preview:data tooltip append value '{"translate":"tryashtar.shulker_preview.durability.5.2","color":"#6666ff"}'
execute if score #fullness shulker_preview matches 32000.. run return run data modify storage tryashtar.shulker_preview:data tooltip append value '{"translate":"tryashtar.shulker_preview.durability.6.2","color":"#6666ff"}'
execute if score #fullness shulker_preview matches 27000.. run return run data modify storage tryashtar.shulker_preview:data tooltip append value '{"translate":"tryashtar.shulker_preview.durability.7.2","color":"#6666ff"}'
execute if score #fullness shulker_preview matches 22000.. run return run data modify storage tryashtar.shulker_preview:data tooltip append value '{"translate":"tryashtar.shulker_preview.durability.8.2","color":"#6666ff"}'
execute if score #fullness shulker_preview matches 16000.. run return run data modify storage tryashtar.shulker_preview:data tooltip append value '{"translate":"tryashtar.shulker_preview.durability.9.2","color":"#6666ff"}'
execute if score #fullness shulker_preview matches 11000.. run return run data modify storage tryashtar.shulker_preview:data tooltip append value '{"translate":"tryashtar.shulker_preview.durability.10.2","color":"#6666ff"}'
execute if score #fullness shulker_preview matches 6000.. run return run data modify storage tryashtar.shulker_preview:data tooltip append value '{"translate":"tryashtar.shulker_preview.durability.11.2","color":"#6666ff"}'
data modify storage tryashtar.shulker_preview:data tooltip append value '{"translate":"tryashtar.shulker_preview.durability.12.2","color":"#6666ff"}'
