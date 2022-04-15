scoreboard players set #done shulker_preview 2

# turn arbitrary NBT back into real item in global shulker box
data modify block ~ 1 ~ Items[0].tag.shulker_items[0].Slot set value 0b
data modify block ~ 1 ~ Items[0] set from block ~ 1 ~ Items[0].tag.shulker_items[0]

# read contents of item inside global shulker box to create entities, and copy the entity names to the lore
function tryashtar.shulker_preview:analyze

data modify block ~ 1 ~ Items[0].tag.display.Lore set value []
data modify block ~ 1 ~ Items[0].tag.display.Lore append from storage tryashtar:shulker_preview line1
data modify block ~ 1 ~ Items[0].tag.display.Lore append from storage tryashtar:shulker_preview line2
data modify block ~ 1 ~ Items[0].tag.display.Lore append from storage tryashtar:shulker_preview line3
data modify block ~ 1 ~ Items[0].tag.display.Lore append from storage tryashtar:shulker_preview line4
data modify block ~ 1 ~ Items[0].tag.display.Lore append from storage tryashtar:shulker_preview line5
execute if score #total shulker_preview matches 1.. run data modify block ~ 1 ~ Items[0].tag.display.Lore append from block ~3 1 ~ Text2
execute unless score #total shulker_preview matches 1.. run data modify block ~ 1 ~ Items[0].tag.display.Lore append value '""'
execute if score #modded shulker_preview matches 2 store result block ~ 1 ~ Items[0].tag.shulker_length int 1 run data get storage tryashtar:shulker_preview line1

data modify block ~ 1 ~ Items[0].tag.HideFlags set value 32
data modify block ~ 1 ~ Items[0].tag.shulker_processed set value 1b

function tryashtar.shulker_preview:return_item
