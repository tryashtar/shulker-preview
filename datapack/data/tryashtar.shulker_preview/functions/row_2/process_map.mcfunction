# create an entity that draws the proper map overlay color
execute if data storage tryashtar:shulker_preview item{tag:{display:{MapColor:3830373}}} run summon area_effect_cloud ~ ~0.1 ~ {Tags:["tryashtar.shulker_preview"],CustomName:'{"translate":"tryashtar.shulker_preview.overlay.filled_map_markings.2","color":"#3a7265"}'}
execute if data storage tryashtar:shulker_preview item{tag:{display:{MapColor:5393476}}} run summon area_effect_cloud ~ ~0.1 ~ {Tags:["tryashtar.shulker_preview"],CustomName:'{"translate":"tryashtar.shulker_preview.overlay.filled_map_markings.2","color":"#524c44"}'}
