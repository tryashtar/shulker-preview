# render banner patterns as overlays
# first move the cursor back on top of the item, then draw the overlays, then put the cursor after the item again
data modify storage tryashtar.shulker_preview:data tooltip append value '{"translate":"tryashtar.shulker_preview.overlay"}'
function tryashtar.shulker_preview:render/row_2/overlay/banner_patterns_loop
data modify storage tryashtar.shulker_preview:data tooltip append value '{"translate":"tryashtar.shulker_preview.overlay_done"}'
