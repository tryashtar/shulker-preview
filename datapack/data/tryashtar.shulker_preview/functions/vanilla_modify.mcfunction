# first item
data modify entity 0-1c9-c369-0-2668 Item set from block ~ 1 ~ Items[0].tag.BlockEntityTag.Items[0]
execute store result score #amount shulker_preview run data get block ~ 1 ~ Items[0].tag.BlockEntityTag.Items[0].Count
execute if score #amount shulker_preview matches 1.. if data entity 0-1c9-c369-0-2668 Item.tag.display.Name run loot spawn ~ ~ ~ loot tryashtar.shulker_preview:vanilla/first_row/named
execute if score #amount shulker_preview matches 1.. unless data entity 0-1c9-c369-0-2668 Item.tag.display.Name run loot spawn ~ ~ ~ loot tryashtar.shulker_preview:vanilla/first_row/unnamed
execute if score #amount shulker_preview matches ..0 run loot spawn ~ ~ ~ loot tryashtar.shulker_preview:vanilla/first_row/empty
tag @e[type=item,tag=,distance=0] add row1

# second item
data modify entity 0-1c9-c369-0-2668 Item set from block ~ 1 ~ Items[0].tag.BlockEntityTag.Items[1]
execute store result score #amount shulker_preview run data get block ~ 1 ~ Items[0].tag.BlockEntityTag.Items[1].Count
execute if score #amount shulker_preview matches 1.. if data entity 0-1c9-c369-0-2668 Item.tag.display.Name run loot spawn ~ ~ ~ loot tryashtar.shulker_preview:vanilla/other_rows/named
execute if score #amount shulker_preview matches 1.. unless data entity 0-1c9-c369-0-2668 Item.tag.display.Name run loot spawn ~ ~ ~ loot tryashtar.shulker_preview:vanilla/other_rows/unnamed
execute if score #amount shulker_preview matches ..0 run loot spawn ~ ~ ~ loot tryashtar.shulker_preview:vanilla/other_rows/empty
tag @e[type=item,tag=,distance=0] add row2

# third item
data modify entity 0-1c9-c369-0-2668 Item set from block ~ 1 ~ Items[0].tag.BlockEntityTag.Items[2]
execute store result score #amount shulker_preview run data get block ~ 1 ~ Items[0].tag.BlockEntityTag.Items[2].Count
execute if score #amount shulker_preview matches 1.. if data entity 0-1c9-c369-0-2668 Item.tag.display.Name run loot spawn ~ ~ ~ loot tryashtar.shulker_preview:vanilla/other_rows/named
execute if score #amount shulker_preview matches 1.. unless data entity 0-1c9-c369-0-2668 Item.tag.display.Name run loot spawn ~ ~ ~ loot tryashtar.shulker_preview:vanilla/other_rows/unnamed
execute if score #amount shulker_preview matches ..0 run loot spawn ~ ~ ~ loot tryashtar.shulker_preview:vanilla/other_rows/empty
tag @e[type=item,tag=,distance=0] add row3

# fourth item
data modify entity 0-1c9-c369-0-2668 Item set from block ~ 1 ~ Items[0].tag.BlockEntityTag.Items[3]
execute store result score #amount shulker_preview run data get block ~ 1 ~ Items[0].tag.BlockEntityTag.Items[3].Count
execute if score #amount shulker_preview matches 1.. if data entity 0-1c9-c369-0-2668 Item.tag.display.Name run loot spawn ~ ~ ~ loot tryashtar.shulker_preview:vanilla/other_rows/named
execute if score #amount shulker_preview matches 1.. unless data entity 0-1c9-c369-0-2668 Item.tag.display.Name run loot spawn ~ ~ ~ loot tryashtar.shulker_preview:vanilla/other_rows/unnamed
execute if score #amount shulker_preview matches ..0 run loot spawn ~ ~ ~ loot tryashtar.shulker_preview:vanilla/other_rows/empty
tag @e[type=item,tag=,distance=0] add row4

# fifth item
data modify entity 0-1c9-c369-0-2668 Item set from block ~ 1 ~ Items[0].tag.BlockEntityTag.Items[4]
execute store result score #amount shulker_preview run data get block ~ 1 ~ Items[0].tag.BlockEntityTag.Items[4].Count
execute if score #amount shulker_preview matches 1.. if data entity 0-1c9-c369-0-2668 Item.tag.display.Name run loot spawn ~ ~ ~ loot tryashtar.shulker_preview:vanilla/other_rows/named
execute if score #amount shulker_preview matches 1.. unless data entity 0-1c9-c369-0-2668 Item.tag.display.Name run loot spawn ~ ~ ~ loot tryashtar.shulker_preview:vanilla/other_rows/unnamed
execute if score #amount shulker_preview matches ..0 run loot spawn ~ ~ ~ loot tryashtar.shulker_preview:vanilla/other_rows/empty
tag @e[type=item,tag=,distance=0] add row5

# additional items
execute store result score #total shulker_preview run data get block ~ 1 ~ Items[0].tag.BlockEntityTag.Items
scoreboard players remove #total shulker_preview 5
execute if score #total shulker_preview matches 1.. run loot spawn ~ ~ ~ loot tryashtar.shulker_preview:vanilla/other_rows/more
execute unless score #total shulker_preview matches 1.. run loot spawn ~ ~ ~ loot tryashtar.shulker_preview:vanilla/other_rows/empty
tag @e[type=item,tag=,distance=0] add row6
