# create an entity that draws approximately colored armor
execute store result score #color shulker_preview run data get storage tryashtar.shulker_preview:data item.tag.display.color
function tryashtar.shulker_preview:row_2/analyze_color
execute if score #near_color shulker_preview matches 16383998 run summon marker ~ ~ ~ {Tags:["tryashtar.shulker_preview"],CustomName:'{"translate":"tryashtar.shulker_preview.item.leather_helmet.2","color":"#f9fffe"}'}
execute if score #near_color shulker_preview matches 16351261 run summon marker ~ ~ ~ {Tags:["tryashtar.shulker_preview"],CustomName:'{"translate":"tryashtar.shulker_preview.item.leather_helmet.2","color":"#f9801d"}'}
execute if score #near_color shulker_preview matches 13061821 run summon marker ~ ~ ~ {Tags:["tryashtar.shulker_preview"],CustomName:'{"translate":"tryashtar.shulker_preview.item.leather_helmet.2","color":"#c74ebd"}'}
execute if score #near_color shulker_preview matches 3847130 run summon marker ~ ~ ~ {Tags:["tryashtar.shulker_preview"],CustomName:'{"translate":"tryashtar.shulker_preview.item.leather_helmet.2","color":"#3ab3da"}'}
execute if score #near_color shulker_preview matches 16701501 run summon marker ~ ~ ~ {Tags:["tryashtar.shulker_preview"],CustomName:'{"translate":"tryashtar.shulker_preview.item.leather_helmet.2","color":"#fed83d"}'}
execute if score #near_color shulker_preview matches 8439583 run summon marker ~ ~ ~ {Tags:["tryashtar.shulker_preview"],CustomName:'{"translate":"tryashtar.shulker_preview.item.leather_helmet.2","color":"#80c71f"}'}
execute if score #near_color shulker_preview matches 15961002 run summon marker ~ ~ ~ {Tags:["tryashtar.shulker_preview"],CustomName:'{"translate":"tryashtar.shulker_preview.item.leather_helmet.2","color":"#f38baa"}'}
execute if score #near_color shulker_preview matches 4673362 run summon marker ~ ~ ~ {Tags:["tryashtar.shulker_preview"],CustomName:'{"translate":"tryashtar.shulker_preview.item.leather_helmet.2","color":"#474f52"}'}
execute if score #near_color shulker_preview matches 10329495 run summon marker ~ ~ ~ {Tags:["tryashtar.shulker_preview"],CustomName:'{"translate":"tryashtar.shulker_preview.item.leather_helmet.2","color":"#9d9d97"}'}
execute if score #near_color shulker_preview matches 1481884 run summon marker ~ ~ ~ {Tags:["tryashtar.shulker_preview"],CustomName:'{"translate":"tryashtar.shulker_preview.item.leather_helmet.2","color":"#169c9c"}'}
execute if score #near_color shulker_preview matches 8991416 run summon marker ~ ~ ~ {Tags:["tryashtar.shulker_preview"],CustomName:'{"translate":"tryashtar.shulker_preview.item.leather_helmet.2","color":"#8932b8"}'}
execute if score #near_color shulker_preview matches 3949738 run summon marker ~ ~ ~ {Tags:["tryashtar.shulker_preview"],CustomName:'{"translate":"tryashtar.shulker_preview.item.leather_helmet.2","color":"#3c44aa"}'}
execute if score #near_color shulker_preview matches 8606770 run summon marker ~ ~ ~ {Tags:["tryashtar.shulker_preview"],CustomName:'{"translate":"tryashtar.shulker_preview.item.leather_helmet.2","color":"#835432"}'}
execute if score #near_color shulker_preview matches 6192150 run summon marker ~ ~ ~ {Tags:["tryashtar.shulker_preview"],CustomName:'{"translate":"tryashtar.shulker_preview.item.leather_helmet.2","color":"#5e7c16"}'}
execute if score #near_color shulker_preview matches 11546150 run summon marker ~ ~ ~ {Tags:["tryashtar.shulker_preview"],CustomName:'{"translate":"tryashtar.shulker_preview.item.leather_helmet.2","color":"#b02e26"}'}
execute if score #near_color shulker_preview matches 1908001 run summon marker ~ ~ ~ {Tags:["tryashtar.shulker_preview"],CustomName:'{"translate":"tryashtar.shulker_preview.item.leather_helmet.2","color":"#1d1d21"}'}
