# summon tooltip background
execute if score #header_type shulker_preview matches 0 if data storage tryashtar.shulker_preview:data items[0].tag.display.Name run summon marker ~ 1 ~ {Tags:["tryashtar.shulker_preview"],CustomName:'{"translate":"tryashtar.shulker_preview.shulker_tooltip"}'}
execute if score #header_type shulker_preview matches 0 unless data storage tryashtar.shulker_preview:data items[0].tag.display.Name run summon marker ~ 1 ~ {Tags:["tryashtar.shulker_preview"],CustomName:'{"translate":"tryashtar.shulker_preview.shulker_tooltip_header"}'}
execute if score #header_type shulker_preview matches 1 run summon marker ~ 1 ~ {Tags:["tryashtar.shulker_preview"],CustomName:'{"translate":"tryashtar.shulker_preview.ender_tooltip"}'}

# copy and analyze contents one by one
function tryashtar.shulker_preview:shulker_box/analyze

# convert back to real item for editing with /item
data modify storage tryashtar.shulker_preview:data items[0].tag.HideFlags set value 32
data modify storage tryashtar.shulker_preview:data items[0].tag.shulker_processed set value 1b
summon armor_stand ~ 999999 ~ {UUID:[I;0,29999977,0,9833],Marker:1b,Invisible:1b}
data modify storage tryashtar.shulker_preview:data items[0].Slot set value 0b
data modify entity 0-1c9-c369-0-2669 HandItems[0] set from storage tryashtar.shulker_preview:data items[0]

# get fallback data for tooltip
summon item ~ ~ ~ {UUID:[I;0,29999977,0,9832],Item:{id:tnt,Count:1b}}

# first item
data modify entity 0-1c9-c369-0-2668 Item set from storage tryashtar.shulker_preview:data contents[0]
execute store result score #amount shulker_preview run data get storage tryashtar.shulker_preview:data contents[0].Count
execute if score #amount shulker_preview matches 1.. if data entity 0-1c9-c369-0-2668 Item.tag.display.Name run item modify entity 0-1c9-c369-0-2669 weapon.mainhand tryashtar.shulker_preview:first_row/named
execute if score #amount shulker_preview matches 1.. unless data entity 0-1c9-c369-0-2668 Item.tag.display.Name run item modify entity 0-1c9-c369-0-2669 weapon.mainhand tryashtar.shulker_preview:first_row/unnamed
execute if score #amount shulker_preview matches ..0 run item modify entity 0-1c9-c369-0-2669 weapon.mainhand tryashtar.shulker_preview:first_row/empty

# second item
data modify entity 0-1c9-c369-0-2668 Item set from storage tryashtar.shulker_preview:data contents[1]
execute store result score #amount shulker_preview run data get storage tryashtar.shulker_preview:data contents[1].Count
execute if score #amount shulker_preview matches 1.. if data entity 0-1c9-c369-0-2668 Item.tag.display.Name run item modify entity 0-1c9-c369-0-2669 weapon.mainhand tryashtar.shulker_preview:other_rows/named
execute if score #amount shulker_preview matches 1.. unless data entity 0-1c9-c369-0-2668 Item.tag.display.Name run item modify entity 0-1c9-c369-0-2669 weapon.mainhand tryashtar.shulker_preview:other_rows/unnamed
execute if score #amount shulker_preview matches ..0 run item modify entity 0-1c9-c369-0-2669 weapon.mainhand tryashtar.shulker_preview:other_rows/empty

# third item
data modify entity 0-1c9-c369-0-2668 Item set from storage tryashtar.shulker_preview:data contents[2]
execute store result score #amount shulker_preview run data get storage tryashtar.shulker_preview:data contents[2].Count
execute if score #amount shulker_preview matches 1.. if data entity 0-1c9-c369-0-2668 Item.tag.display.Name run item modify entity 0-1c9-c369-0-2669 weapon.mainhand tryashtar.shulker_preview:other_rows/named
execute if score #amount shulker_preview matches 1.. unless data entity 0-1c9-c369-0-2668 Item.tag.display.Name run item modify entity 0-1c9-c369-0-2669 weapon.mainhand tryashtar.shulker_preview:other_rows/unnamed
execute if score #amount shulker_preview matches ..0 run item modify entity 0-1c9-c369-0-2669 weapon.mainhand tryashtar.shulker_preview:other_rows/empty

# fourth item
data modify entity 0-1c9-c369-0-2668 Item set from storage tryashtar.shulker_preview:data contents[3]
execute store result score #amount shulker_preview run data get storage tryashtar.shulker_preview:data contents[3].Count
execute if score #amount shulker_preview matches 1.. if data entity 0-1c9-c369-0-2668 Item.tag.display.Name run item modify entity 0-1c9-c369-0-2669 weapon.mainhand tryashtar.shulker_preview:other_rows/named
execute if score #amount shulker_preview matches 1.. unless data entity 0-1c9-c369-0-2668 Item.tag.display.Name run item modify entity 0-1c9-c369-0-2669 weapon.mainhand tryashtar.shulker_preview:other_rows/unnamed
execute if score #amount shulker_preview matches ..0 run item modify entity 0-1c9-c369-0-2669 weapon.mainhand tryashtar.shulker_preview:other_rows/empty

# fifth item
execute if score #amount shulker_preview matches 1.. if data entity 0-1c9-c369-0-2668 Item.tag.display.Name run item modify entity 0-1c9-c369-0-2669 weapon.mainhand tryashtar.shulker_preview:other_rows/named
execute if score #amount shulker_preview matches 1.. unless data entity 0-1c9-c369-0-2668 Item.tag.display.Name run item modify entity 0-1c9-c369-0-2669 weapon.mainhand tryashtar.shulker_preview:other_rows/unnamed
execute if score #amount shulker_preview matches ..0 run item modify entity 0-1c9-c369-0-2669 weapon.mainhand tryashtar.shulker_preview:other_rows/empty

# additional items
execute store result score #more shulker_preview run data get storage tryashtar.shulker_preview:data contents
scoreboard players remove #more shulker_preview 5
execute if score #more shulker_preview matches 1.. run item modify entity 0-1c9-c369-0-2669 weapon.mainhand tryashtar.shulker_preview:other_rows/more
execute unless score #more shulker_preview matches 1.. run item modify entity 0-1c9-c369-0-2669 weapon.mainhand tryashtar.shulker_preview:other_rows/empty

kill 0-1c9-c369-0-2668
kill @e[type=marker,tag=tryashtar.shulker_preview]

# don't process any more items this tick
scoreboard players set #ready shulker_preview 0
