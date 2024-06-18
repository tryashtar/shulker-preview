# the player got an ender chest, flag them for a scan
# only one box is processed per tick, so we keep the tag on players until they're processed
advancement revoke @s only tryashtar.shulker_preview:detect_ender_chest
tag @s add shulker_preview.ender_chest
