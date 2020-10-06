# recursively draw all banner patterns
function tryashtar.shulker_preview:row_2/overlay/banner_pattern
data remove storage tryashtar:shulker_preview item.tag.BlockEntityTag.Patterns[0]
execute if data storage tryashtar:shulker_preview item.tag.BlockEntityTag.Patterns[0] positioned ~ ~0.01 ~ run function tryashtar.shulker_preview:row_2/overlay/banner
