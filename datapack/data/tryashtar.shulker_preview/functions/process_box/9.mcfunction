# there is a container in slot 9 of the global shulker box
# copy its contents to the sub-global shulker box, read them to create entities, and copy the entity names to the lore
data remove block ~1 ~ ~ Items
data modify block ~1 ~ ~ Items set from block ~ ~ ~ Items[{Slot:9b}].tag.BlockEntityTag.Items
function tryashtar.shulker_preview:process_box
data modify block ~ ~ ~ Items[{Slot:9b}].tag.display.Lore set value ["\"\\uF82C\\uF82A\\uF827\"","\"\"","\"\"","\"\"","\"\""]
data modify block ~ ~ ~ Items[{Slot:9b}].tag.display.Lore prepend from block ~3 ~ ~ Text1
data modify block ~ ~ ~ Items[{Slot:9b}].tag.HideFlags set value 32
data modify block ~ ~ ~ Items[{Slot:9b}].tag.shulker_processed set value 1b
