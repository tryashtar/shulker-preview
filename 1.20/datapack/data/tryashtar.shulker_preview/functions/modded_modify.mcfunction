# first item
data modify entity 0-1c9-c369-0-2668 Item set from storage tryashtar.shulker_preview:data contents[0]
execute store result score #amount shulker_preview run data get storage tryashtar.shulker_preview:data contents[0].Count
execute if score #amount shulker_preview matches 1.. if data entity 0-1c9-c369-0-2668 Item.tag.display.Name run item modify entity 0-1c9-c369-0-2669 weapon.mainhand tryashtar.shulker_preview:first_row_modded/named
execute if score #amount shulker_preview matches 1.. unless data entity 0-1c9-c369-0-2668 Item.tag.display.Name run item modify entity 0-1c9-c369-0-2669 weapon.mainhand tryashtar.shulker_preview:first_row_modded/unnamed
execute if score #amount shulker_preview matches ..0 run item modify entity 0-1c9-c369-0-2669 weapon.mainhand tryashtar.shulker_preview:first_row_modded/empty

function tryashtar.shulker_preview:modify_other_rows

execute store result entity 0-1c9-c369-0-2669 HandItems[0].tag.shulker_length int 1 run data get entity 0-1c9-c369-0-2669 HandItems[0].tag.display.Lore[0]
