data modify block ~ 1 ~ Items set value [{id:tnt,Count:1b,tag:{shulker_items:[]}}]
data modify storage tryashtar:shulker_preview ender_chests set value []
data modify storage tryashtar:shulker_preview ender_chests append from entity @s Inventory[{id:"minecraft:ender_chest"}] 
data modify block ~ 1 ~ Items[0].tag.shulker_items set from storage tryashtar:shulker_preview ender_chests

# copy player ender items to ender chest item so we can reuse shulker box technique
data modify block ~ 1 ~ Items[0].tag.shulker_items[0].tag.BlockEntityTag.Items set from entity @s EnderItems

# process the first one and return it normally
execute store result score #slot shulker_preview run data get block ~ 1 ~ Items[0].tag.shulker_items[0].Slot
function tryashtar.shulker_preview:from_player

# copy the identical lore to any remaining chests and return them quickly
data modify storage tryashtar:shulker_preview ender_chests[].tag.display.Lore set from block ~ 1 ~ Items[0].tag.display.Lore
data modify storage tryashtar:shulker_preview ender_chests[].tag.HideFlags set value 32
data modify storage tryashtar:shulker_preview ender_chests[].tag.shulker_processed set value 1b
execute if data storage tryashtar:shulker_preview ender_chests[1] run function tryashtar.shulker_preview:return_ender_chests

tag @s remove shulker_preview.ender_chest
