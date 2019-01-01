# these slots are 9-35 on the player, but we need them to be 0-27 in the global shulker box
# so we copy the item data to a temporary location, subtract 9, then copy it to where it belongs
execute store result score #slot shulker_preview run data get block ~ ~ ~ Items[0].tag.shulker_item.Slot
scoreboard players remove #slot shulker_preview 9
execute store result block ~ ~ ~ Items[0].tag.shulker_item.Slot byte 1 run scoreboard players get #slot shulker_preview
data modify block ~ ~ ~ Items append from block ~ ~ ~ Items[0].tag.shulker_item
data remove block ~ ~ ~ Items[0].tag.shulker_item
