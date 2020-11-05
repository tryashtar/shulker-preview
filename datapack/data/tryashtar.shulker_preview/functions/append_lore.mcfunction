data modify block ~ 1 ~ Items[0].tag.display.Lore append from block ~2 1 ~ Text1
data modify block ~ 1 ~ Items[0].tag.display.Lore append from block ~2 1 ~ Text2
data modify block ~ 1 ~ Items[0].tag.display.Lore append from block ~2 1 ~ Text3
data modify block ~ 1 ~ Items[0].tag.display.Lore append from block ~2 1 ~ Text4
data modify block ~ 1 ~ Items[0].tag.display.Lore append from block ~3 1 ~ Text1
execute if score #total shulker_preview matches 1.. run data modify block ~ 1 ~ Items[0].tag.display.Lore append from block ~3 1 ~ Text2
execute unless score #total shulker_preview matches 1.. run data modify block ~ 1 ~ Items[0].tag.display.Lore append value '""'

data modify entity @s Item.tag.HideFlags set value 32
data modify entity @s Item.tag.shulker_processed set value 1b
