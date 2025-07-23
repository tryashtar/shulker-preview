# summon tooltip background
summon area_effect_cloud ~ 1 ~ {Tags:["tryashtar.shulker_preview"],CustomName:'{"translate":"tryashtar.shulker_preview.start"}'}
execute if score #ender_header shulker_preview matches 1 run summon area_effect_cloud ~ 1.1 ~ {Tags:["tryashtar.shulker_preview"],CustomName:'{"translate":"tryashtar.shulker_preview.ender_tooltip"}'}
execute if score #ender_header shulker_preview matches 0 run summon area_effect_cloud ~ 1.1 ~ {Tags:["tryashtar.shulker_preview"],CustomName:'{"translate":"tryashtar.shulker_preview.shulker_tooltip"}'}

function tryashtar.shulker_preview:analyze

# construct the tooltip and fallback
# the first line of lore shows the custom tooltip if the pack is equipped
# if not, it displays the name and quantity of the first item, just like vanilla
summon item ~ ~ ~ {UUIDMost:8316025820458349088L,UUIDLeast:8102650238841747263L,Item:{id:"tnt",Count:1b}}
data modify block ~ 1 ~ Items[0].tag.display.Lore set value []

data modify entity 7368756c-6b65-7220-7072-65766965773f Item set from block ~ 1 ~ Items[0].tag.BlockEntityTag.Items[0]
execute store result score #amount shulker_preview run data get block ~ 1 ~ Items[0].tag.BlockEntityTag.Items[0].Count
execute if score #amount shulker_preview matches 1.. as 7368756c-6b65-7220-7072-65766965773f if data entity @s Item.tag.display.Name run loot replace block ~ 1 ~ container.1 loot tryashtar.shulker_preview:first_row/named
execute if score #amount shulker_preview matches 1.. as 7368756c-6b65-7220-7072-65766965773f unless data entity @s Item.tag.display.Name run loot replace block ~ 1 ~ container.1 loot tryashtar.shulker_preview:first_row/unnamed
execute if score #amount shulker_preview matches ..0 as 7368756c-6b65-7220-7072-65766965773f run loot replace block ~ 1 ~ container.1 loot tryashtar.shulker_preview:first_row/empty
data modify block ~ 1 ~ Items[0].tag.display.Lore append from block ~ 1 ~ Items[1].tag.display.Lore[]

# subsequent lines are blank when the pack is equipped
# if not, they show the name and quantity of subsequent items
data modify entity 7368756c-6b65-7220-7072-65766965773f Item set from block ~ 1 ~ Items[0].tag.BlockEntityTag.Items[1]
execute store result score #amount shulker_preview run data get block ~ 1 ~ Items[0].tag.BlockEntityTag.Items[1].Count
execute if score #amount shulker_preview matches 1.. as 7368756c-6b65-7220-7072-65766965773f if data entity @s Item.tag.display.Name run loot replace block ~ 1 ~ container.1 loot tryashtar.shulker_preview:other_rows/named
execute if score #amount shulker_preview matches 1.. as 7368756c-6b65-7220-7072-65766965773f unless data entity @s Item.tag.display.Name run loot replace block ~ 1 ~ container.1 loot tryashtar.shulker_preview:other_rows/unnamed
execute if score #amount shulker_preview matches ..0 as 7368756c-6b65-7220-7072-65766965773f run loot replace block ~ 1 ~ container.1 loot tryashtar.shulker_preview:other_rows/empty
data modify block ~ 1 ~ Items[0].tag.display.Lore append from block ~ 1 ~ Items[1].tag.display.Lore[]

data modify entity 7368756c-6b65-7220-7072-65766965773f Item set from block ~ 1 ~ Items[0].tag.BlockEntityTag.Items[2]
execute store result score #amount shulker_preview run data get block ~ 1 ~ Items[0].tag.BlockEntityTag.Items[2].Count
execute if score #amount shulker_preview matches 1.. as 7368756c-6b65-7220-7072-65766965773f if data entity @s Item.tag.display.Name run loot replace block ~ 1 ~ container.1 loot tryashtar.shulker_preview:other_rows/named
execute if score #amount shulker_preview matches 1.. as 7368756c-6b65-7220-7072-65766965773f unless data entity @s Item.tag.display.Name run loot replace block ~ 1 ~ container.1 loot tryashtar.shulker_preview:other_rows/unnamed
execute if score #amount shulker_preview matches ..0 as 7368756c-6b65-7220-7072-65766965773f run loot replace block ~ 1 ~ container.1 loot tryashtar.shulker_preview:other_rows/empty
data modify block ~ 1 ~ Items[0].tag.display.Lore append from block ~ 1 ~ Items[1].tag.display.Lore[]

data modify entity 7368756c-6b65-7220-7072-65766965773f Item set from block ~ 1 ~ Items[0].tag.BlockEntityTag.Items[3]
execute store result score #amount shulker_preview run data get block ~ 1 ~ Items[0].tag.BlockEntityTag.Items[3].Count
execute if score #amount shulker_preview matches 1.. as 7368756c-6b65-7220-7072-65766965773f if data entity @s Item.tag.display.Name run loot replace block ~ 1 ~ container.1 loot tryashtar.shulker_preview:other_rows/named
execute if score #amount shulker_preview matches 1.. as 7368756c-6b65-7220-7072-65766965773f unless data entity @s Item.tag.display.Name run loot replace block ~ 1 ~ container.1 loot tryashtar.shulker_preview:other_rows/unnamed
execute if score #amount shulker_preview matches ..0 as 7368756c-6b65-7220-7072-65766965773f run loot replace block ~ 1 ~ container.1 loot tryashtar.shulker_preview:other_rows/empty
data modify block ~ 1 ~ Items[0].tag.display.Lore append from block ~ 1 ~ Items[1].tag.display.Lore[]

data modify entity 7368756c-6b65-7220-7072-65766965773f Item set from block ~ 1 ~ Items[0].tag.BlockEntityTag.Items[4]
execute store result score #amount shulker_preview run data get block ~ 1 ~ Items[0].tag.BlockEntityTag.Items[4].Count
execute if score #amount shulker_preview matches 1.. as 7368756c-6b65-7220-7072-65766965773f if data entity @s Item.tag.display.Name run loot replace block ~ 1 ~ container.1 loot tryashtar.shulker_preview:other_rows/named
execute if score #amount shulker_preview matches 1.. as 7368756c-6b65-7220-7072-65766965773f unless data entity @s Item.tag.display.Name run loot replace block ~ 1 ~ container.1 loot tryashtar.shulker_preview:other_rows/unnamed
execute if score #amount shulker_preview matches ..0 as 7368756c-6b65-7220-7072-65766965773f run loot replace block ~ 1 ~ container.1 loot tryashtar.shulker_preview:other_rows/empty
data modify block ~ 1 ~ Items[0].tag.display.Lore append from block ~ 1 ~ Items[1].tag.display.Lore[]

# vanilla only shows 5, but we show 6 because it pushes the advanced tooltip below the container
data modify entity 7368756c-6b65-7220-7072-65766965773f Item set from block ~ 1 ~ Items[0].tag.BlockEntityTag.Items[5]
execute store result score #amount shulker_preview run data get block ~ 1 ~ Items[0].tag.BlockEntityTag.Items[5].Count
execute if score #amount shulker_preview matches 1.. as 7368756c-6b65-7220-7072-65766965773f if data entity @s Item.tag.display.Name run loot replace block ~ 1 ~ container.1 loot tryashtar.shulker_preview:other_rows/named
execute if score #amount shulker_preview matches 1.. as 7368756c-6b65-7220-7072-65766965773f unless data entity @s Item.tag.display.Name run loot replace block ~ 1 ~ container.1 loot tryashtar.shulker_preview:other_rows/unnamed
execute if score #amount shulker_preview matches ..0 as 7368756c-6b65-7220-7072-65766965773f run loot replace block ~ 1 ~ container.1 loot tryashtar.shulker_preview:other_rows/empty
data modify block ~ 1 ~ Items[0].tag.display.Lore append from block ~ 1 ~ Items[1].tag.display.Lore[]

# lastly, show the "X more..." line if the pack is not equipped
execute store result score #more shulker_preview run data get block ~ 1 ~ Items[0].tag.BlockEntityTag.Items
scoreboard players remove #more shulker_preview 6
execute if score #more shulker_preview matches 1.. as 7368756c-6b65-7220-7072-65766965773f run loot replace block ~ 1 ~ container.1 loot tryashtar.shulker_preview:other_rows/more
execute unless score #more shulker_preview matches 1.. as 7368756c-6b65-7220-7072-65766965773f run loot replace block ~ 1 ~ container.1 loot tryashtar.shulker_preview:other_rows/empty
data modify block ~ 1 ~ Items[0].tag.display.Lore append from block ~ 1 ~ Items[1].tag.display.Lore[]

# hide the original tooltip lines, and mark this box as processed
data modify block ~ ~1 ~ Items[0].tag.HideFlags set value 32
data modify block ~ ~1 ~ Items[0].tag."shulker_preview.processed" set value 1b

# don't process any more boxes this tick
scoreboard players set #ready shulker_preview 0
kill 7368756c-6b65-7220-7072-65766965773f
kill @e[type=area_effect_cloud,tag=tryashtar.shulker_preview]
