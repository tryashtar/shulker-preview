data modify storage tryashtar:shulker_preview old_sizes set from block ~ 1 ~ Items[0].tag.shulker_items[0].tag.bundle_sizes
data modify block ~ 1 ~ Items[0].tag.shulker_items[0].tag.bundle_sizes set value []
data modify block ~ 1 ~ Items[0].tag.shulker_items[0].tag.bundle_sizes append from block ~ 1 ~ Items[0].tag.shulker_items[0].tag.Items[].Count
execute store success score #changed_size shulker_preview run data modify storage tryashtar:shulker_preview old_sizes set from block ~ 1 ~ Items[0].tag.shulker_items[0].tag.bundle_sizes

execute if score #changed_size shulker_preview matches 0 run data remove block ~ 1 ~ Items[0].tag.shulker_items[0]
execute if score #changed_size shulker_preview matches 0 if data block ~ 1 ~ Items[0].tag.shulker_items[0] run function tryashtar.shulker_preview:filter_bundles
