data modify storage tryashtar.shulker_preview:data items[0].tag.display.Lore append from block ~2 1 ~ Text1
data modify storage tryashtar.shulker_preview:data items[0].tag.display.Lore append from block ~2 1 ~ Text2
data modify storage tryashtar.shulker_preview:data items[0].tag.display.Lore append from block ~2 1 ~ Text3
data modify storage tryashtar.shulker_preview:data items[0].tag.display.Lore append from block ~2 1 ~ Text4
data modify storage tryashtar.shulker_preview:data items[0].tag.display.Lore append from block ~3 1 ~ Text1
execute if score #total shulker_preview matches 1.. run data modify storage tryashtar.shulker_preview:data items[0].tag.display.Lore append from block ~3 1 ~ Text2
execute unless score #total shulker_preview matches 1.. run data modify storage tryashtar.shulker_preview:data items[0].tag.display.Lore append value '""'

data modify storage tryashtar.shulker_preview:data items[0].tag.HideFlags set value 32
data modify storage tryashtar.shulker_preview:data items[0].tag.shulker_processed set value 1b
