data modify storage tryashtar.shulker_preview:data items[0].tag.display.Lore append from block ~2 1 ~ Text1
data modify storage tryashtar.shulker_preview:data items[0].tag.display.Lore append from block ~2 1 ~ Text2
execute if score #row_count shulker_preview matches 2.. run data modify storage tryashtar.shulker_preview:data items[0].tag.display.Lore append from block ~2 1 ~ Text3
execute if score #row_count shulker_preview matches 3.. run data modify storage tryashtar.shulker_preview:data items[0].tag.display.Lore append from block ~2 1 ~ Text4
execute if score #row_count shulker_preview matches 3.. run data modify storage tryashtar.shulker_preview:data items[0].tag.display.Lore append from block ~3 1 ~ Text1
execute if score #row_count shulker_preview matches 4.. run data modify storage tryashtar.shulker_preview:data items[0].tag.display.Lore append from block ~3 1 ~ Text2
execute if score #row_count shulker_preview matches 4.. run data modify storage tryashtar.shulker_preview:data items[0].tag.display.Lore append value '""'

data modify storage tryashtar.shulker_preview:data items[0].tag.HideFlags set value 32
