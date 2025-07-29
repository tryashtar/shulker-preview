# the process function inspects items in the BlockEntityTag.Items container list
# we make a fake one by copying the player's EnderItems
data modify block ~ 1 ~ Items set value [{id:"tnt",Count:1b}]
data modify block ~ 1 ~ Items[0].tag.BlockEntityTag.Items set from entity @s EnderItems
scoreboard players set #ender_header shulker_preview 1
function tryashtar.shulker_preview:process

# use the jukebox as a temporary storage location for the lore, and ender chests in the player's inventory
# each one will be copied to the shulker box, assigned the lore, then returned to the player
data modify block ~1 1 ~ RecordItem set value {id:"tnt",Count:1b}
data modify block ~1 1 ~ RecordItem.tag.display.Lore set from block ~ 1 ~ Items[0].tag.display.Lore
data modify block ~1 1 ~ RecordItem.tag.ender_chests append from entity @s Inventory[{id:"minecraft:ender_chest"}]
execute store result score #slot shulker_preview store success score #has_slot shulker_preview run data get block ~1 1 ~ RecordItem.tag.ender_chests[0].Slot
execute if score #has_slot shulker_preview matches 1 run function tryashtar.shulker_preview:ender_chest/return_loop
