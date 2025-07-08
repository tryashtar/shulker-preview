execute if score #ready shulker_preview matches 1 run tag @s add shulker_processed
data modify storage tryashtar.shulker_preview:data items set value []
execute if score #ready shulker_preview matches 1 run data modify storage tryashtar.shulker_preview:data items append from entity @s Item
execute if score #ready shulker_preview matches 1 if data storage tryashtar.shulker_preview:data items[0].tag.BlockEntityTag.Items[0] unless data storage tryashtar.shulker_preview:data items[0].tag.shulker_processed run function tryashtar.shulker_preview:shulker_box/from_dropped
