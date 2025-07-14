# do nothing if a box was already processed this tick
# these checks need to go here because the functions get queued before executing

# if this is an unprocessed shulker box with items inside, process it
execute if score #ready shulker_preview matches 1 if entity @s[nbt={Item:{tag:{BlockEntityTag:{Items:[{}]}}}},nbt=!{Item:{tag:{"shulker_preview.processed":1b}}}] positioned 29999977 1 9832 run function tryashtar.shulker_preview:shulker_box/process_dropped

# don't check this item again, whether or not it was processed
execute if score #ready shulker_preview matches 1 run tag @s add shulker_preview.checked
