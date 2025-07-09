# if your ender chest contents changes, rescan inventory
scoreboard players operation #ender shulker_preview = @s shulker_preview
execute store result score @s shulker_preview if data entity @s EnderItems[]
execute unless score #ender shulker_preview = @s shulker_preview run tag @s add shulker_preview.ender_chest
