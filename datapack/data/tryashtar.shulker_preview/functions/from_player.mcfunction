# read contents of item to create entities
function tryashtar.shulker_preview:analyze

# copy lore to item
data modify storage tryashtar:shulker_preview items[0].tag.display.Lore set value []
execute if score #header_type shulker_preview matches 0..1 if data storage tryashtar:shulker_preview contents[0] run function tryashtar.shulker_preview:shulker_box/append_lore
execute if score #header_type shulker_preview matches 2 if data storage tryashtar:shulker_preview contents[0] run function tryashtar.shulker_preview:bundle/append_lore

# put the item in the global shulker box and return it to the player
data modify storage tryashtar:shulker_preview items[0].Slot set value 0b
data modify block ~ 1 ~ Items[0] set from storage tryashtar:shulker_preview items[0]
function tryashtar.shulker_preview:return_item
