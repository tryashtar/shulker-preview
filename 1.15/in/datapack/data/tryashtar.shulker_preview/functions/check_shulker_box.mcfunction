# copy all containers in inventory to arbitrary NBT area (item tag)
data modify block ~ 1 ~ Items set value [{id:tnt,Count:1b}]
data modify block ~ 1 ~ Items[0].tag.shulker_items append from entity @s Inventory[{tag:{BlockEntityTag:{Items:[{}]}}}]

# filter out containers that have already been processed
data remove block ~ 1 ~ Items[0].tag.shulker_items[{tag:{shulker_processed:1b}}]
scoreboard players set #uuid shulker_preview -1

# save which slot first remaining container came from
execute store result score #slot shulker_preview store success score #success shulker_preview run data get block ~ 1 ~ Items[0].tag.shulker_items[0].Slot

# workaround for the fact that /clear can find items in the cursor, but Inventory[] cannot
# without this sub-function, picking up a lone unprocessed shulker box puts the placeholder TNT in your inventory
execute if score #success shulker_preview matches 1 run function tryashtar.shulker_preview:from_player
