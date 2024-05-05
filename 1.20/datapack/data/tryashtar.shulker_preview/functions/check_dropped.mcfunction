execute unless score #ready shulker_preview matches 1 run return fail
tag @s add shulker_preview.checked
execute if items entity @s contents #tryashtar.shulker_preview:shulker_boxes[!custom_data~{"shulker_preview.processed":1b},container~{items:{size:{min:1}}}] run function tryashtar.shulker_preview:shulker_box/from_dropped
