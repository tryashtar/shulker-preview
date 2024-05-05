execute if items entity @s contents *[custom_name] run data modify storage tryashtar.shulker_preview:data tooltip set value ['{"translate":"tryashtar.shulker_preview.shulker_tooltip"}']
execute unless items entity @s contents *[custom_name] run data modify storage tryashtar.shulker_preview:data tooltip set value ['{"translate":"tryashtar.shulker_preview.shulker_tooltip_header"}']
data modify storage tryashtar.shulker_preview:data contents set from entity @s Item.components."minecraft:container"

function tryashtar.shulker_preview:analyze
