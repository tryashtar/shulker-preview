# look up a shield base hex color from its dye color
# insert it back into the item to use in another macro
$data modify storage tryashtar.shulker_preview:data item.base set from storage tryashtar.shulker_preview:data lookups.dyes.$(base)
