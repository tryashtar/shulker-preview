# recursively draw all banner patterns
function tryashtar.shulker_preview:row_1/overlay/shield_pattern
data remove storage tryashtar.shulker_preview:data item.tag.BlockEntityTag.Patterns[0]
execute if data storage tryashtar.shulker_preview:data item.tag.BlockEntityTag.Patterns[0] positioned ~ ~0.01 ~ run function tryashtar.shulker_preview:row_1/overlay/shield
