# calculate the sizes list
data modify storage tryashtar:shulker_preview bundle_sizes set value []
data modify storage tryashtar:shulker_preview bundle_sizes append from storage tryashtar:shulker_preview items[0].tag.Items[].Count

# save it to the item
execute store success score #changed_size shulker_preview run data modify storage tryashtar:shulker_preview items[0].tag.bundle_sizes set from storage tryashtar:shulker_preview bundle_sizes

# if there was no change, remove this item
execute if score #changed_size shulker_preview matches 0 run data remove storage tryashtar:shulker_preview items[0]
execute if score #changed_size shulker_preview matches 0 if data storage tryashtar:shulker_preview items[0] run function tryashtar.shulker_preview:bundle/filter
