# the player got a shulker box, flag them for a scan
# only one box is processed per tick, so we keep the tag on players until they're processed
advancement revoke @s only tryashtar.shulker_preview:detect_shulker_box
tag @s add shulker_preview.shulker_box
