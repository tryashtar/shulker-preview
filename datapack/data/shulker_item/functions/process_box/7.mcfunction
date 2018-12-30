data remove block ~ ~1 ~ Items
data modify block ~ ~1 ~ Items set from block ~ ~ ~ Items[{Slot:7b}].tag.BlockEntityTag.Items
function shulker_item:process_box
kill @e[type=area_effect_cloud,tag=shulker_item]
data modify block ~ ~ ~ Items[{Slot:7b}].tag.display.Lore[] set from block ~ ~2 ~ Text1
data modify block ~ ~ ~ Items[{Slot:7b}].tag.HideFlags set value 63
data modify block ~ ~ ~ Items[{Slot:7b}].tag.shulker_processed set value 1b
