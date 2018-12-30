execute store result score #slot shulker_item run data get block ~ ~ ~ Items[0].tag.shulker_item.Slot
scoreboard players remove #slot shulker_item 9
execute store result block ~ ~ ~ Items[0].tag.shulker_item.Slot byte 1 run scoreboard players get #slot shulker_item
data modify block ~ ~ ~ Items append from block ~ ~ ~ Items[0].tag.shulker_item
data remove block ~ ~ ~ Items[0].tag.shulker_item
