# copy all ender chests in inventory to arbitrary NBT area (item tag)
data modify block ~ 1 ~ Items set value [{id:tnt,Count:1b}]
data modify storage tryashtar:shulker_preview ender_chests set value []
data modify storage tryashtar:shulker_preview ender_chests append from entity @s Inventory[{id:"minecraft:ender_chest"}] 
data modify block ~ 1 ~ Items[0].tag.shulker_items set from storage tryashtar:shulker_preview ender_chests

# copy player ender items to ender chest item so we can reuse shulker box technique
data modify block ~ 1 ~ Items[0].tag.shulker_items[0].tag.BlockEntityTag.Items set from entity @s EnderItems
scoreboard players set #ender_header shulker_preview 1

# proceed if there is at least one in the inventory (not just cursor)
execute store result score #slot shulker_preview store success score #success shulker_preview run data get storage tryashtar:shulker_preview ender_chests[0].Slot
execute if score #success shulker_preview matches 1 run function tryashtar.shulker_preview:process_ender_chests
