data modify block ~ ~1 ~ Items set from block ~ ~ ~ Items[{Slot:0b,id:"minecraft:shulker_box"}].tag.BlockEntityTag.Items
function shulker_item:process_box
data modify block ~ ~ ~ Items[{Slot:0b,id:"minecraft:shulker_box"}].tag.display.Lore[] set from block ~ ~2 ~ Text1
data modify block ~ ~ ~ Items[{Slot:0b,id:"minecraft:shulker_box"}].tag.HideFlags set value 63
