# we need a nested function here because this function gets queued before executing
execute if score #ready shulker_preview matches 1 run function tryashtar.shulker_preview:shulker_box/check_dropped_ready
