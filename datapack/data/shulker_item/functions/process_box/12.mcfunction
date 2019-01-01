# there is a container in slot 12 of the global shulker box
# copy its contents to the sub-global shulker box, read them to create entities, and copy the entity names to the lore
data remove block ~1 ~ ~ Items
data modify block ~1 ~ ~ Items set from block ~ ~ ~ Items[{Slot:12b}].tag.BlockEntityTag.Items
function shulker_item:process_box
data remove block ~ ~ ~ Items[{Slot:12b}].tag.display.Lore
data modify block ~ ~ ~ Items[{Slot:12b}].tag.display.Lore append from block ~3 ~ ~ Text1
data modify block ~ ~ ~ Items[{Slot:12b}].tag.display.Lore append value "\"                                         \""
data modify block ~ ~ ~ Items[{Slot:12b}].tag.HideFlags set value 32
data modify block ~ ~ ~ Items[{Slot:12b}].tag.shulker_processed set value 1b
