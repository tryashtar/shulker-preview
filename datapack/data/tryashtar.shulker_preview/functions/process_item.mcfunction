# copy item contents to sub-global shulker box inventory, read them to create entities, and copy the entity names to the lore
data modify block 29999977 1 9832 Items set from entity @s Item.tag.BlockEntityTag.Items
function tryashtar.shulker_preview:process_box
data modify entity @s Item.tag.display.Lore set value ['"\\uF82C\\uF82A\\uF827"','""','""','""','""']
data modify entity @s Item.tag.display.Lore prepend from block 29999979 1 9832 Text1
data modify entity @s Item.tag.HideFlags set value 32
data modify entity @s Item.tag.shulker_processed set value 1b
