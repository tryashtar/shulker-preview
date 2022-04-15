data modify storage tryashtar:shulker_preview items set value []
data modify storage tryashtar:shulker_preview items append from entity @s Inventory[{tag:{BlockEntityTag:{Items:[{}]}}}]
data remove storage tryashtar:shulker_preview items[{tag:{shulker_broken:1b}}]

function tryashtar.shulker_preview:modded_fix_check_loop
