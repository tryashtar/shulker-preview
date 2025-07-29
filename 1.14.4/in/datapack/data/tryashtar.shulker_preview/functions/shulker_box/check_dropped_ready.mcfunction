# don't check this item again, whether or not it gets processed
tag @s add shulker_preview.checked

# if this is an unprocessed container with items inside, process it
# checking for shulker box IDs would be too expensive here
execute if entity @s[nbt={Item:{tag:{BlockEntityTag:{Items:[{}]}}}},nbt=!{Item:{tag:{"shulker_preview.processed":1b}}}] run function tryashtar.shulker_preview:shulker_box/process_dropped
