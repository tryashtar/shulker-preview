# setup
data modify storage tryashtar.shulker_preview:data items set value []
data modify storage tryashtar.shulker_preview:data items append from entity @s Item
data modify storage tryashtar.shulker_preview:data contents set from storage tryashtar.shulker_preview:data items[0].tag.BlockEntityTag.Items
scoreboard players set #header_type shulker_preview 0

# read contents of item to create entities
function tryashtar.shulker_preview:analyze

# copy lore to item
data modify storage tryashtar.shulker_preview:data items[0].tag.display.Lore set value []
function tryashtar.shulker_preview:shulker_box/append_lore

# return item to entity
data modify entity @s Item set from storage tryashtar.shulker_preview:data items[0]
