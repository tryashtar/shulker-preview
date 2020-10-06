# create an entity that draws a banner pattern overlay
data modify storage tryashtar:shulker_preview pattern set from storage tryashtar:shulker_preview item.tag.BlockEntityTag.Patterns[0]
execute if data storage tryashtar:shulker_preview pattern{Color:0} run function tryashtar.shulker_preview:row_1/overlay/banner/white
execute if data storage tryashtar:shulker_preview pattern{Color:1} run function tryashtar.shulker_preview:row_1/overlay/banner/orange
execute if data storage tryashtar:shulker_preview pattern{Color:2} run function tryashtar.shulker_preview:row_1/overlay/banner/magenta
execute if data storage tryashtar:shulker_preview pattern{Color:3} run function tryashtar.shulker_preview:row_1/overlay/banner/light_blue
execute if data storage tryashtar:shulker_preview pattern{Color:4} run function tryashtar.shulker_preview:row_1/overlay/banner/yellow
execute if data storage tryashtar:shulker_preview pattern{Color:5} run function tryashtar.shulker_preview:row_1/overlay/banner/lime
execute if data storage tryashtar:shulker_preview pattern{Color:6} run function tryashtar.shulker_preview:row_1/overlay/banner/pink
execute if data storage tryashtar:shulker_preview pattern{Color:7} run function tryashtar.shulker_preview:row_1/overlay/banner/gray
execute if data storage tryashtar:shulker_preview pattern{Color:8} run function tryashtar.shulker_preview:row_1/overlay/banner/light_gray
execute if data storage tryashtar:shulker_preview pattern{Color:9} run function tryashtar.shulker_preview:row_1/overlay/banner/cyan
execute if data storage tryashtar:shulker_preview pattern{Color:10} run function tryashtar.shulker_preview:row_1/overlay/banner/purple
execute if data storage tryashtar:shulker_preview pattern{Color:11} run function tryashtar.shulker_preview:row_1/overlay/banner/blue
execute if data storage tryashtar:shulker_preview pattern{Color:12} run function tryashtar.shulker_preview:row_1/overlay/banner/brown
execute if data storage tryashtar:shulker_preview pattern{Color:13} run function tryashtar.shulker_preview:row_1/overlay/banner/green
execute if data storage tryashtar:shulker_preview pattern{Color:14} run function tryashtar.shulker_preview:row_1/overlay/banner/red
execute if data storage tryashtar:shulker_preview pattern{Color:15} run function tryashtar.shulker_preview:row_1/overlay/banner/black
