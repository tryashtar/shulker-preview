# read contents of item inside global shulker box to create entities, and copy the entity names to the lore
data remove block ~ 1 ~ Items
data modify block ~ 1 ~ Items append from entity @s Item
scoreboard players set #uuid shulker_preview -1
function tryashtar.shulker_preview:analyze

data modify block ~ 1 ~ Item.tag.display.Lore set value []
data modify block ~ 1 ~ Item.tag.display.Lore append from block ~2 1 ~ Text1
data modify block ~ 1 ~ Item.tag.display.Lore append from block ~2 1 ~ Text2
data modify block ~ 1 ~ Item.tag.display.Lore append from block ~2 1 ~ Text3
data modify block ~ 1 ~ Item.tag.display.Lore append from block ~2 1 ~ Text4
data modify block ~ 1 ~ Item.tag.display.Lore append from block ~3 1 ~ Text1
execute if score #total shulker_preview matches 1.. run data modify block ~ 1 ~ Item.tag.display.Lore append from block ~3 1 ~ Text2
execute unless score #total shulker_preview matches 1.. run data modify block ~ 1 ~ Item.tag.display.Lore append value '""'

data modify entity @s Item.tag.HideFlags set value 32
data modify entity @s Item.tag.shulker_processed set value 1b
