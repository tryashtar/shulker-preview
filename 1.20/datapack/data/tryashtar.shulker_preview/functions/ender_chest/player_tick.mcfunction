# if the player has a different number of items in their ender chest from last check, flag them for a scan
# only one box is processed per tick, so we keep the tag on players until they're processed
scoreboard players operation #ender shulker_preview = @s shulker_preview
execute store result score @s shulker_preview if items entity @s enderchest.* *
execute unless score #ender shulker_preview = @s shulker_preview run tag @s add shulker_preview.ender_chest
