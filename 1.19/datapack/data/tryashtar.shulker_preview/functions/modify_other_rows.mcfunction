# second item (unnamed shulker box)
data modify entity 0-1c9-c369-0-2668 Item set from storage tryashtar.shulker_preview:data contents[1]
execute store result score #amount shulker_preview run data get storage tryashtar.shulker_preview:data contents[1].Count
execute unless data storage tryashtar.shulker_preview:data {id:"minecraft:ender_chest"} unless data storage tryashtar.shulker_preview:data items[0].tag.display.Name if score #amount shulker_preview matches 1.. if data entity 0-1c9-c369-0-2668 Item.tag.display.Name run item modify entity 0-1c9-c369-0-2669 weapon.mainhand tryashtar.shulker_preview:second_row/shulker_box/named
execute unless data storage tryashtar.shulker_preview:data {id:"minecraft:ender_chest"} unless data storage tryashtar.shulker_preview:data items[0].tag.display.Name if score #amount shulker_preview matches 1.. unless data entity 0-1c9-c369-0-2668 Item.tag.display.Name run item modify entity 0-1c9-c369-0-2669 weapon.mainhand tryashtar.shulker_preview:second_row/shulker_box/unnamed
execute unless data storage tryashtar.shulker_preview:data {id:"minecraft:ender_chest"} unless data storage tryashtar.shulker_preview:data items[0].tag.display.Name if score #amount shulker_preview matches ..0 run item modify entity 0-1c9-c369-0-2669 weapon.mainhand tryashtar.shulker_preview:second_row/shulker_box/empty

# second item (named shulker box)
execute unless data storage tryashtar.shulker_preview:data {id:"minecraft:ender_chest"} if data storage tryashtar.shulker_preview:data items[0].tag.display.Name if score #amount shulker_preview matches 1.. if data entity 0-1c9-c369-0-2668 Item.tag.display.Name run item modify entity 0-1c9-c369-0-2669 weapon.mainhand tryashtar.shulker_preview:second_row/named/named
execute unless data storage tryashtar.shulker_preview:data {id:"minecraft:ender_chest"} if data storage tryashtar.shulker_preview:data items[0].tag.display.Name if score #amount shulker_preview matches 1.. unless data entity 0-1c9-c369-0-2668 Item.tag.display.Name run item modify entity 0-1c9-c369-0-2669 weapon.mainhand tryashtar.shulker_preview:second_row/named/unnamed
execute unless data storage tryashtar.shulker_preview:data {id:"minecraft:ender_chest"} if data storage tryashtar.shulker_preview:data items[0].tag.display.Name if score #amount shulker_preview matches ..0 run item modify entity 0-1c9-c369-0-2669 weapon.mainhand tryashtar.shulker_preview:second_row/named/empty

# second item (ender chest)
execute if data storage tryashtar.shulker_preview:data {id:"minecraft:ender_chest"} if score #amount shulker_preview matches 1.. if data entity 0-1c9-c369-0-2668 Item.tag.display.Name run item modify entity 0-1c9-c369-0-2669 weapon.mainhand tryashtar.shulker_preview:second_row/ender_chest/named
execute if data storage tryashtar.shulker_preview:data {id:"minecraft:ender_chest"} if score #amount shulker_preview matches 1.. unless data entity 0-1c9-c369-0-2668 Item.tag.display.Name run item modify entity 0-1c9-c369-0-2669 weapon.mainhand tryashtar.shulker_preview:second_row/ender_chest/unnamed
execute if data storage tryashtar.shulker_preview:data {id:"minecraft:ender_chest"} if score #amount shulker_preview matches ..0 run item modify entity 0-1c9-c369-0-2669 weapon.mainhand tryashtar.shulker_preview:second_row/ender_chest/empty

# third item
data modify entity 0-1c9-c369-0-2668 Item set from storage tryashtar.shulker_preview:data contents[2]
execute store result score #amount shulker_preview run data get storage tryashtar.shulker_preview:data contents[2].Count
execute if score #amount shulker_preview matches 1.. if data entity 0-1c9-c369-0-2668 Item.tag.display.Name run item modify entity 0-1c9-c369-0-2669 weapon.mainhand tryashtar.shulker_preview:other_rows/named
execute if score #amount shulker_preview matches 1.. unless data entity 0-1c9-c369-0-2668 Item.tag.display.Name run item modify entity 0-1c9-c369-0-2669 weapon.mainhand tryashtar.shulker_preview:other_rows/unnamed
execute if score #amount shulker_preview matches ..0 run item modify entity 0-1c9-c369-0-2669 weapon.mainhand tryashtar.shulker_preview:other_rows/empty

# fourth item
data modify entity 0-1c9-c369-0-2668 Item set from storage tryashtar.shulker_preview:data contents[3]
execute store result score #amount shulker_preview run data get storage tryashtar.shulker_preview:data contents[3].Count
execute if score #amount shulker_preview matches 1.. if data entity 0-1c9-c369-0-2668 Item.tag.display.Name run item modify entity 0-1c9-c369-0-2669 weapon.mainhand tryashtar.shulker_preview:other_rows/named
execute if score #amount shulker_preview matches 1.. unless data entity 0-1c9-c369-0-2668 Item.tag.display.Name run item modify entity 0-1c9-c369-0-2669 weapon.mainhand tryashtar.shulker_preview:other_rows/unnamed
execute if score #amount shulker_preview matches ..0 run item modify entity 0-1c9-c369-0-2669 weapon.mainhand tryashtar.shulker_preview:other_rows/empty

# fifth item
execute if score #amount shulker_preview matches 1.. if data entity 0-1c9-c369-0-2668 Item.tag.display.Name run item modify entity 0-1c9-c369-0-2669 weapon.mainhand tryashtar.shulker_preview:other_rows/named
execute if score #amount shulker_preview matches 1.. unless data entity 0-1c9-c369-0-2668 Item.tag.display.Name run item modify entity 0-1c9-c369-0-2669 weapon.mainhand tryashtar.shulker_preview:other_rows/unnamed
execute if score #amount shulker_preview matches ..0 run item modify entity 0-1c9-c369-0-2669 weapon.mainhand tryashtar.shulker_preview:other_rows/empty

# additional items
execute store result score #more shulker_preview run data get storage tryashtar.shulker_preview:data contents
scoreboard players remove #more shulker_preview 5
execute if score #more shulker_preview matches 1.. run item modify entity 0-1c9-c369-0-2669 weapon.mainhand tryashtar.shulker_preview:other_rows/more
execute unless score #more shulker_preview matches 1.. run item modify entity 0-1c9-c369-0-2669 weapon.mainhand tryashtar.shulker_preview:other_rows/empty
