scoreboard players set #done shulker_preview 2

# turn arbitrary NBT back into real item in global shulker box
data modify block ~ 1 ~ Items[0].tag.shulker_items[0].Slot set value 0b
data modify block ~ 1 ~ Items[0] set from block ~ 1 ~ Items[0].tag.shulker_items[0]

# read contents of item inside global shulker box to create entities, and copy the entity names to the lore
function tryashtar.shulker_preview:analyze

data modify block ~ 1 ~ Items[0].tag.display.Lore set value []
data modify block ~ 1 ~ Items[0].tag.display.Lore append from entity @e[type=item,tag=row1,distance=0,limit=1] Item.tag.display.Lore[]
data modify block ~ 1 ~ Items[0].tag.display.Lore append from entity @e[type=item,tag=row2,distance=0,limit=1] Item.tag.display.Lore[]
data modify block ~ 1 ~ Items[0].tag.display.Lore append from entity @e[type=item,tag=row3,distance=0,limit=1] Item.tag.display.Lore[]
data modify block ~ 1 ~ Items[0].tag.display.Lore append from entity @e[type=item,tag=row4,distance=0,limit=1] Item.tag.display.Lore[]
data modify block ~ 1 ~ Items[0].tag.display.Lore append from entity @e[type=item,tag=row5,distance=0,limit=1] Item.tag.display.Lore[]
data modify block ~ 1 ~ Items[0].tag.display.Lore append from entity @e[type=item,tag=row6,distance=0,limit=1] Item.tag.display.Lore[]
kill @e[type=item,distance=0]

data modify block ~ 1 ~ Items[0].tag.HideFlags set value 32
data modify block ~ 1 ~ Items[0].tag.shulker_processed set value 1b

function tryashtar.shulker_preview:return_item
