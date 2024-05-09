# first item
data modify entity 0-1c9-c369-0-2668 Item set from storage tryashtar.shulker_preview:data contents[0]
execute store result score #amount shulker_preview run data get storage tryashtar.shulker_preview:data contents[0].Count
execute if score #amount shulker_preview matches 1.. if data entity 0-1c9-c369-0-2668 Item.tag.display.Name run item modify entity 0-1c9-c369-0-2669 contents.mainhand tryashtar.shulker_preview:first_row_vanilla/named
execute if score #amount shulker_preview matches 1.. unless data entity 0-1c9-c369-0-2668 Item.tag.display.Name run item modify entity 0-1c9-c369-0-2669 contents.mainhand tryashtar.shulker_preview:first_row_vanilla/unnamed
execute if score #amount shulker_preview matches ..0 run item modify entity 0-1c9-c369-0-2669 contents.mainhand tryashtar.shulker_preview:first_row_vanilla/empty

function tryashtar.shulker_preview:modify_other_rows
