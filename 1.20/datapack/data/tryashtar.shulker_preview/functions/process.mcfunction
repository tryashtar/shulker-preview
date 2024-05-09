# box processing requires matching against real items in some cases, so we need an entity to hold those
# use an item entity specifically for the vanilla fallback tooltip, a selector text component will show the item's display name
function tryashtar.shulker_preview:start_render
summon item ~ -10000 ~ {Invulnerable:1b,NoGravity:1b,Silent:1b,UUID:[I;1936225644,1801810464,1886545270,1768257313],Item:{id:"tnt",count:1}}
execute as 7368756c-6b65-7220-7072-657669657721 run function tryashtar.shulker_preview:analyze

# construct the tooltip and fallback
# the first line of lore shows the custom tooltip if the pack is equipped
# if not, it displays the name and quantity of the first item, just like vanilla
data modify entity 7368756c-6b65-7220-7072-657669657721 Item set from storage tryashtar.shulker_preview:data contents[0].item
execute store result score #amount shulker_preview run data get storage tryashtar.shulker_preview:data contents[0].item.count
execute if score #amount shulker_preview matches 1.. if items entity 7368756c-6b65-7220-7072-657669657721 contents *[custom_name] run item modify entity @s contents tryashtar.shulker_preview:first_row/named
execute if score #amount shulker_preview matches 1.. unless items entity 7368756c-6b65-7220-7072-657669657721 contents *[custom_name] run item modify entity @s contents tryashtar.shulker_preview:first_row/unnamed
execute if score #amount shulker_preview matches ..0 run item modify entity @s contents tryashtar.shulker_preview:first_row/empty

# subsequent lines are blank when the pack is equipped
# if not, they show the name and quantity of subsequent items
data modify entity 7368756c-6b65-7220-7072-657669657721 Item set from storage tryashtar.shulker_preview:data contents[1].item
execute store result score #amount shulker_preview run data get storage tryashtar.shulker_preview:data contents[1].item.count
execute if score #amount shulker_preview matches 1.. if items entity 7368756c-6b65-7220-7072-657669657721 contents *[custom_name] run item modify entity @s contents tryashtar.shulker_preview:other_rows/named
execute if score #amount shulker_preview matches 1.. unless items entity 7368756c-6b65-7220-7072-657669657721 contents *[custom_name] run item modify entity @s contents tryashtar.shulker_preview:other_rows/unnamed
execute if score #amount shulker_preview matches ..0 run item modify entity @s contents tryashtar.shulker_preview:other_rows/empty

data modify entity 7368756c-6b65-7220-7072-657669657721 Item set from storage tryashtar.shulker_preview:data contents[2].item
execute store result score #amount shulker_preview run data get storage tryashtar.shulker_preview:data contents[2].item.count
execute if score #amount shulker_preview matches 1.. if items entity 7368756c-6b65-7220-7072-657669657721 contents *[custom_name] run item modify entity @s contents tryashtar.shulker_preview:other_rows/named
execute if score #amount shulker_preview matches 1.. unless items entity 7368756c-6b65-7220-7072-657669657721 contents *[custom_name] run item modify entity @s contents tryashtar.shulker_preview:other_rows/unnamed
execute if score #amount shulker_preview matches ..0 run item modify entity @s contents tryashtar.shulker_preview:other_rows/empty

data modify entity 7368756c-6b65-7220-7072-657669657721 Item set from storage tryashtar.shulker_preview:data contents[3].item
execute store result score #amount shulker_preview run data get storage tryashtar.shulker_preview:data contents[3].item.count
execute if score #amount shulker_preview matches 1.. if items entity 7368756c-6b65-7220-7072-657669657721 contents *[custom_name] run item modify entity @s contents tryashtar.shulker_preview:other_rows/named
execute if score #amount shulker_preview matches 1.. unless items entity 7368756c-6b65-7220-7072-657669657721 contents *[custom_name] run item modify entity @s contents tryashtar.shulker_preview:other_rows/unnamed
execute if score #amount shulker_preview matches ..0 run item modify entity @s contents tryashtar.shulker_preview:other_rows/empty

data modify entity 7368756c-6b65-7220-7072-657669657721 Item set from storage tryashtar.shulker_preview:data contents[4].item
execute store result score #amount shulker_preview run data get storage tryashtar.shulker_preview:data contents[4].item.count
execute if score #amount shulker_preview matches 1.. if items entity 7368756c-6b65-7220-7072-657669657721 contents *[custom_name] run item modify entity @s contents tryashtar.shulker_preview:other_rows/named
execute if score #amount shulker_preview matches 1.. unless items entity 7368756c-6b65-7220-7072-657669657721 contents *[custom_name] run item modify entity @s contents tryashtar.shulker_preview:other_rows/unnamed
execute if score #amount shulker_preview matches ..0 run item modify entity @s contents tryashtar.shulker_preview:other_rows/empty

# lastly, show the "X more..." line if the pack is not equipped
execute store result score #more shulker_preview run data get storage tryashtar.shulker_preview:data contents
scoreboard players remove #more shulker_preview 5
execute if score #more shulker_preview matches 1.. run item modify entity @s contents tryashtar.shulker_preview:other_rows/more
execute if score #more shulker_preview matches ..0 run item modify entity @s contents tryashtar.shulker_preview:other_rows/empty

# hide the original tooltip lines, and mark this box as processed
item modify entity @s contents tryashtar.shulker_preview:finish
execute if score #modded shulker_preview matches 2 store result entity @s Item.components."minecraft:custom_data"."shulker_preview.lore_length" int 1 run data get entity @s Item.components."minecraft:lore"[0]

# don't process any more items this tick
scoreboard players set #ready shulker_preview 0
kill 7368756c-6b65-7220-7072-657669657721
