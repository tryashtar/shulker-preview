# put the shulker box item in the global shulker box, process it, and return it to the player
data modify block ~1 1 ~ RecordItem.tag.shulker_boxes[0].Slot set value 0b
data modify block ~ 1 ~ Items[0] set from block ~1 1 ~ RecordItem.tag.shulker_boxes[0]
scoreboard players set #ender_header shulker_preview 0
function tryashtar.shulker_preview:process
function tryashtar.shulker_preview:copy_item
