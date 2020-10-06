# create an entity that draws a banner pattern overlay
data modify storage tryashtar:shulker_preview pattern set from storage tryashtar:shulker_preview item.tag.BlockEntityTag.Patterns[0]
execute if data storage tryashtar:shulker_preview pattern{Color:0} run function tryashtar.shulker_preview:row_2/overlay/shield/white
execute if data storage tryashtar:shulker_preview pattern{Color:1} run function tryashtar.shulker_preview:row_2/overlay/shield/orange
execute if data storage tryashtar:shulker_preview pattern{Color:2} run function tryashtar.shulker_preview:row_2/overlay/shield/magenta
execute if data storage tryashtar:shulker_preview pattern{Color:3} run function tryashtar.shulker_preview:row_2/overlay/shield/light_blue
execute if data storage tryashtar:shulker_preview pattern{Color:4} run function tryashtar.shulker_preview:row_2/overlay/shield/yellow
execute if data storage tryashtar:shulker_preview pattern{Color:5} run function tryashtar.shulker_preview:row_2/overlay/shield/lime
execute if data storage tryashtar:shulker_preview pattern{Color:6} run function tryashtar.shulker_preview:row_2/overlay/shield/pink
execute if data storage tryashtar:shulker_preview pattern{Color:7} run function tryashtar.shulker_preview:row_2/overlay/shield/gray
execute if data storage tryashtar:shulker_preview pattern{Color:8} run function tryashtar.shulker_preview:row_2/overlay/shield/light_gray
execute if data storage tryashtar:shulker_preview pattern{Color:9} run function tryashtar.shulker_preview:row_2/overlay/shield/cyan
execute if data storage tryashtar:shulker_preview pattern{Color:10} run function tryashtar.shulker_preview:row_2/overlay/shield/purple
execute if data storage tryashtar:shulker_preview pattern{Color:11} run function tryashtar.shulker_preview:row_2/overlay/shield/blue
execute if data storage tryashtar:shulker_preview pattern{Color:12} run function tryashtar.shulker_preview:row_2/overlay/shield/brown
execute if data storage tryashtar:shulker_preview pattern{Color:13} run function tryashtar.shulker_preview:row_2/overlay/shield/green
execute if data storage tryashtar:shulker_preview pattern{Color:14} run function tryashtar.shulker_preview:row_2/overlay/shield/red
execute if data storage tryashtar:shulker_preview pattern{Color:15} run function tryashtar.shulker_preview:row_2/overlay/shield/black
