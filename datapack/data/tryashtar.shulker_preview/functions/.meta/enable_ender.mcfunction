scoreboard players set #ender_enabled shulker_preview 1
function tryashtar.shulker_preview:ender_tick
tellraw @a [{"text":"\n\nEnder chest previews enabled successfully!\n","color":"#ac6bb5"},{"text":"You can run this command at any time to disable them:\n","color":"yellow"},{"text":"/function tryashtar.shulker_preview:.meta/disable_ender\n\n","color":"gray","hoverEvent":{"action":"show_text","contents":{"text":"Click to disable ender chest previews","color":"yellow"}},"clickEvent":{"action":"run_command","value":"/function tryashtar.shulker_preview:.meta/disable_ender"}},"\n"]
