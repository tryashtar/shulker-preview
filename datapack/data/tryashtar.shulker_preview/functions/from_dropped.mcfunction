# read contents of item inside global shulker box to create entities, and copy the entity names to the lore
data remove block ~ 1 ~ Items
data modify block ~ 1 ~ Items append from entity @s Item
scoreboard players set #header_type shulker_preview 0
function tryashtar.shulker_preview:analyze

data modify entity @s Item.tag.display.Lore set value []
function tryashtar.shulker_preview:append_lore
