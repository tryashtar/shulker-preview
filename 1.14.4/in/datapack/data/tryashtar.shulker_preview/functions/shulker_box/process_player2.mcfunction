# turn arbitrary NBT back into real item in global shulker box
data modify block ~ 1 ~ Items[0].tag.shulker_items[0].Slot set value 0b
data modify block ~ 1 ~ Items[0] set from block ~ 1 ~ Items[0].tag.shulker_items[0]
scoreboard players set #ender_header shulker_preview 0
function tryashtar.shulker_preview:process

# return processed container to its original slot
function tryashtar.shulker_preview:copy_item
