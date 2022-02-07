# read contents of item inside global shulker box to create entities, and copy the entity names to the lore
data remove block ~ 1 ~ Items
data modify block ~ 1 ~ Items append from entity @s Item
scoreboard players set #uuid shulker_preview -1
function tryashtar.shulker_preview:analyze

data modify entity @s Item.tag.display.Lore set value []
data modify entity @s Item.tag.display.Lore append from storage tryashtar:shulker_preview line1
data modify entity @s Item.tag.display.Lore append from storage tryashtar:shulker_preview line2
data modify entity @s Item.tag.display.Lore append from storage tryashtar:shulker_preview line3
data modify entity @s Item.tag.display.Lore append from storage tryashtar:shulker_preview line4
data modify entity @s Item.tag.display.Lore append from storage tryashtar:shulker_preview line5
execute if score #total shulker_preview matches 1.. run data modify entity @s Item.tag.display.Lore append from block ~3 1 ~ Text2
execute unless score #total shulker_preview matches 1.. run data modify entity @s Item.tag.display.Lore append value '""'
execute if score #modded shulker_preview matches 2 store result block ~ 1 ~ Items[0].tag.shulker_length int 1 run data get storage tryashtar:shulker_preview line1

data modify entity @s Item.tag.HideFlags set value 32
data modify entity @s Item.tag.shulker_processed set value 1b
