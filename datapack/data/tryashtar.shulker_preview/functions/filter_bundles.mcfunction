execute store result score #old_size shulker_preview run data get block ~ 1 ~ Items[0].tag.shulker_items[0].tag.bundle_size
execute store result score #size shulker_preview store result block ~ 1 ~ Items[0].tag.shulker_items[0].tag.bundle_size byte 1 run data get block ~ 1 ~ Items[0].tag.shulker_items[0].tag.Items
execute if score #old_size shulker_preview = #size shulker_preview run data remove block ~ 1 ~ Items[0].tag.shulker_items[0]
execute if score #old_size shulker_preview = #size shulker_preview if data block ~ 1 ~ Items[0].tag.shulker_items[0] run function tryashtar.shulker_preview:filter_bundles
