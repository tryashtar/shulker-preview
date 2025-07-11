data modify storage tryashtar.shulker_preview:data items set value []
data modify storage tryashtar.shulker_preview:data items append from entity @s Inventory[{tag:{BlockEntityTag:{Items:[{}]}}}]
data remove storage tryashtar.shulker_preview:data items[{tag:{shulker_broken:1b}}]

function tryashtar.shulker_preview:modded_fix_check_loop
