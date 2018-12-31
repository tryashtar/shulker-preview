# there is a container in slot 13 of the global shulker box
# copy its contents to the sub-global shulker box, read them to create entities, and copy the entity names to the lore
data remove block ~1 ~ ~ Items
data modify block ~1 ~ ~ Items set from block ~ ~ ~ Items[{Slot:13b}].tag.BlockEntityTag.Items
function shulker_item:process_box
kill @e[type=area_effect_cloud,tag=shulker_item]
data modify block ~ ~ ~ Items[{Slot:13b}].tag.display.Lore[] set from block ~2 ~ ~ Text1
data modify block ~ ~ ~ Items[{Slot:13b}].tag.HideFlags set value 32
data modify block ~ ~ ~ Items[{Slot:13b}].tag.shulker_processed set value 1b
