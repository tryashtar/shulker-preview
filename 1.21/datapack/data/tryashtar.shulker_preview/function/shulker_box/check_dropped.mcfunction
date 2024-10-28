# exit immediately if a box was already processed this tick
# this check needs to go here because the functions get queued before executing
execute unless score #ready shulker_preview matches 1 run return fail

# if this is an unprocessed shulker box with items inside, process it
execute if items entity @s contents #tryashtar.shulker_preview:shulker_boxes[!custom_data~{"shulker_preview.processed":1b},container~{}] run function tryashtar.shulker_preview:shulker_box/process_dropped

# don't check this item again, whether or not it was processed
tag @s add shulker_preview.checked
