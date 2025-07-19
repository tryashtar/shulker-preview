# do nothing if a box was already processed this tick
# these checks need to go here because the functions get queued before executing

# if this is an unprocessed container with items inside, process it
# checking for shulker box IDs would be too expensive here
execute if score #ready shulker_preview matches 1 if entity @s[nbt={Item:{tag:{BlockEntityTag:{Items:[{}]}}}},nbt=!{Item:{tag:{"shulker_preview.processed":1b}}}] run function tryashtar.shulker_preview:shulker_box/process_dropped

# don't check this item again, whether or not it was processed
execute if score #ready shulker_preview matches 1 run tag @s add shulker_preview.checked
