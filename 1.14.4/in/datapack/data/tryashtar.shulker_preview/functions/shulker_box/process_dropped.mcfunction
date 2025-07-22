# copy the shulker box items to the global shulker box for processing
data remove block ~ 1 ~ Items
data modify block ~ 1 ~ Items append from entity @s Item
scoreboard players set #ender_header shulker_preview 0
function tryashtar.shulker_preview:process

# copy it back out directly to the item entity
data modify entity @s Item set from block ~ 1 ~ Items[0]
