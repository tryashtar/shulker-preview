execute store result score #slot shulker_preview run data get storage tryashtar:shulker_preview items[0].Slot
data remove storage tryashtar:shulker_preview items[0].Slot

data remove storage tryashtar:shulker_preview items[0].tag.HideFlags
data modify storage tryashtar:shulker_preview items[0].tag.shulker_broken set value 1b

data remove block ~ 1 ~ Items
data modify block ~ 1 ~ Items append from storage tryashtar:shulker_preview items[0]

loot spawn ~ ~ ~ loot tryashtar.shulker_preview:modded/broken
data modify block ~ 1 ~ Items[0].tag.display.Lore set from entity @e[type=item,distance=0,limit=1] Item.tag.display.Lore
kill @e[type=item,distance=0]

function tryashtar.shulker_preview:return_item
