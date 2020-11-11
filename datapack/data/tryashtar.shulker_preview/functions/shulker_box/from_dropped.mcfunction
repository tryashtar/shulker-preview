# setup
data modify storage tryashtar.shulker_preview:data items set value []
data modify storage tryashtar.shulker_preview:data items append from entity @s Item
data modify storage tryashtar.shulker_preview:data contents set from storage tryashtar.shulker_preview:data items[0].tag.BlockEntityTag.Items
scoreboard players set #header_type shulker_preview 0

function tryashtar.shulker_preview:analyze
data modify entity @s Item set from storage tryashtar.shulker_preview:data items[0]
kill 0-1c9-c369-0-2669
