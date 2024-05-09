execute if score #shulker_enabled shulker_preview matches 1 run tellraw @a ["",{"translate":"tryashtar.shulker_preview.item.minecraft:shulker_box.0","font":"tryashtar.shulker_preview:preview"},"\n     ",{"text":"✔","color":"#56d656"}," ",{"text":"✘","color":"#8a8a8a","hoverEvent":{"action":"show_text","contents":{"text":"Click to disable them","color":"#f06e6e"}},"clickEvent":{"action":"run_command","value":"/function tryashtar.shulker_preview:config/shulker_box/disable"}},{"text":" Shulker box previews are","color":"#ffee7d"},{"text":" enabled.","color":"#56d656"}]
execute if score #shulker_enabled shulker_preview matches 0 run tellraw @a ["",{"translate":"tryashtar.shulker_preview.item.minecraft:shulker_box.0","font":"tryashtar.shulker_preview:preview"},"\n     ",{"text":"✔","color":"#8a8a8a","hoverEvent":{"action":"show_text","contents":{"text":"Click to enable them","color":"#56d656"}},"clickEvent":{"action":"run_command","value":"/function tryashtar.shulker_preview:config/shulker_box/enable"}}," ",{"text":"✘","color":"#f06e6e"},{"text":" Shulker box previews are","color":"#ffee7d"},{"text":" disabled.","color":"#f06e6e"}]

execute if score #ender_enabled shulker_preview matches 1 run tellraw @a ["",{"translate":"tryashtar.shulker_preview.item.minecraft:ender_chest.0","font":"tryashtar.shulker_preview:preview"},"\n     ",{"text":"✔","color":"#56d656"}," ",{"text":"✘","color":"#8a8a8a","hoverEvent":{"action":"show_text","contents":{"text":"Click to disable them","color":"#f06e6e"}},"clickEvent":{"action":"run_command","value":"/function tryashtar.shulker_preview:config/ender_chest/disable"}},{"text":" Ender chest previews are","color":"#ffee7d"},{"text":" enabled.","color":"#56d656"}]
execute if score #ender_enabled shulker_preview matches 0 run tellraw @a ["",{"translate":"tryashtar.shulker_preview.item.minecraft:ender_chest.0","font":"tryashtar.shulker_preview:preview"},"\n     ",{"text":"✔","color":"#8a8a8a","hoverEvent":{"action":"show_text","contents":{"text":"Click to enable them","color":"#56d656"}},"clickEvent":{"action":"run_command","value":"/function tryashtar.shulker_preview:config/ender_chest/enable"}}," ",{"text":"✘","color":"#f06e6e"},{"text":" Ender chest previews are","color":"#ffee7d"},{"text":" disabled.","color":"#f06e6e"}]
