# check for any ender chests
# no optimization for "already scanned" chests, since any new lore must be copied to all of them in order for them to stack
execute store result score #ender_chests shulker_preview run clear @s ender_chest 0
execute if score #ready shulker_preview matches 1 if score #ender_chests shulker_preview matches 1.. positioned 29999977 1 9832 run function tryashtar.shulker_preview:ender_chest/prepare

# we're always finished with ender chests in one go
tag @s remove shulker_preview.ender_chest
