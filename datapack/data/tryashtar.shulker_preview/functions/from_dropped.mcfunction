# read contents of item inside global shulker box to create entities, and copy the entity names to the lore
data remove block ~ 1 ~ Items
data modify block ~ 1 ~ Items append from entity @s Item
scoreboard players set #uuid shulker_preview -1
function tryashtar.shulker_preview:analyze

data modify entity @s Item.tag.display.Lore set value []
data modify entity @s Item.tag.display.Lore append from entity @e[type=item,tag=row1,distance=0,limit=1] Item.tag.display.Lore[]
data modify entity @s Item.tag.display.Lore append from entity @e[type=item,tag=row2,distance=0,limit=1] Item.tag.display.Lore[]
data modify entity @s Item.tag.display.Lore append from entity @e[type=item,tag=row3,distance=0,limit=1] Item.tag.display.Lore[]
data modify entity @s Item.tag.display.Lore append from entity @e[type=item,tag=row4,distance=0,limit=1] Item.tag.display.Lore[]
data modify entity @s Item.tag.display.Lore append from entity @e[type=item,tag=row5,distance=0,limit=1] Item.tag.display.Lore[]
data modify entity @s Item.tag.display.Lore append from entity @e[type=item,tag=row6,distance=0,limit=1] Item.tag.display.Lore[]
kill @e[type=item,distance=0]
execute if score #modded shulker_preview matches 2 store result entity @s Item.tag.shulker_length int 1 run data get entity @s Item.tag.display.Lore[0]

data modify entity @s Item.tag.HideFlags set value 32
data modify entity @s Item.tag.shulker_processed set value 1b
