summon armor_stand ~ 999999 ~ {UUID:[I;0,29999977,0,9833],Marker:1b,Invisible:1b}
execute store result score #slot shulker_preview run data get storage tryashtar.shulker_preview:data items[0].Slot

data remove storage tryashtar.shulker_preview:data items[0].tag.HideFlags
data modify storage tryashtar.shulker_preview:data items[0].tag.shulker_broken set value 1b

data modify entity 0-1c9-c369-0-2669 HandItems[0] set from storage tryashtar.shulker_preview:data items[0]
item modify entity 0-1c9-c369-0-2669 weapon.mainhand tryashtar.shulker_preview:first_row_modded/broken

function tryashtar.shulker_preview:return_item
kill 0-1c9-c369-0-2668
