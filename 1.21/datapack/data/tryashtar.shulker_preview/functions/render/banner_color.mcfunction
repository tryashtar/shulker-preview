# look up a banner pattern's hex color from its dye color
# insert it back into the same spot to use in another macro
$data modify storage tryashtar.shulker_preview:data item.components."minecraft:banner_patterns"[0].color set from storage tryashtar.shulker_preview:data lookups.dyes.$(color)
