scoreboard players set #ender_enabled shulker_preview 1
function tryashtar.shulker_preview:ender_tick
tellraw @a [{"text":"\nEnder chest previews enabled successfully!\n","color":"green"},{"text":"You can run this command at any time to disable them:\n","color":"yellow"},{"text":"/function tryashtar.shulker_preview:.meta/disable_ender","color":"gray","hoverEvent":{"action":"show_text","value":{"text":"Click to disable","color":"yellow"}},"clickEvent":{"action":"run_command","value":"/function tryashtar.shulker_preview:.meta/disable_ender"}},"\n"]
