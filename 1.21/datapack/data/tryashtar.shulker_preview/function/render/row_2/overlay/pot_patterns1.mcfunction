# render decorated pot patterns as overlays
# only the second and fourth are visible on the left and right, respectively
# each ID is an item name of either a sherd or brick
data modify storage tryashtar.shulker_preview:data tooltip append value {translate:"tryashtar.shulker_preview.overlay"}
data modify storage tryashtar.shulker_preview:data item.left set from storage tryashtar.shulker_preview:data item.components."minecraft:pot_decorations"[1]
data modify storage tryashtar.shulker_preview:data item.right set from storage tryashtar.shulker_preview:data item.components."minecraft:pot_decorations"[3]
function tryashtar.shulker_preview:render/row_2/overlay/pot_patterns2 with storage tryashtar.shulker_preview:data item
data modify storage tryashtar.shulker_preview:data tooltip append value {translate:"tryashtar.shulker_preview.overlay_done"}
