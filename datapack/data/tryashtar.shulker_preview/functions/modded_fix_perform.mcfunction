execute store result score #slot shulker_preview run data get storage tryashtar:shulker_preview items[0].Slot
data remove storage tryashtar:shulker_preview items[0].Slot

data remove storage tryashtar:shulker_preview items[0].tag.HideFlags
data remove storage tryashtar:shulker_preview items[0].tag.display.Lore[-1]
data remove storage tryashtar:shulker_preview items[0].tag.display.Lore[-1]
data remove storage tryashtar:shulker_preview items[0].tag.display.Lore[-1]
data remove storage tryashtar:shulker_preview items[0].tag.display.Lore[-1]
data remove storage tryashtar:shulker_preview items[0].tag.display.Lore[-1]
data modify storage tryashtar:shulker_preview items[0].tag.shulker_broken set value 1b

data remove block ~ 1 ~ Items
data modify block ~ 1 ~ Items append from storage tryashtar:shulker_preview items[0]

data modify block ~2 1 ~ Text1 set value '{"translate":"%1$s%418634357$s","with":["",{"text":"Bukkit prevented this shulker tooltip","italic":false,"color":"red"}]}'
data modify block ~2 1 ~ Text2 set value '{"translate":"%1$s%418634357$s","with":["",{"text":"from displaying correctly. Sorry!","italic":false,"color":"red"}]}'
data modify block ~ 1 ~ Items[0].tag.display.Lore append from block ~2 1 ~ Text1
data modify block ~ 1 ~ Items[0].tag.display.Lore append from block ~2 1 ~ Text2

function tryashtar.shulker_preview:return_item
