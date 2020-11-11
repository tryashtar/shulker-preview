scoreboard players set #install shulker_preview 1
scoreboard players set #shulker_enabled shulker_preview 1
scoreboard players set #ender_enabled shulker_preview 0
tellraw @a {"translate":"%1$s%418634357$s","with":[{"text":"\nDon't forget to equip the shulker preview resource pack!\n","color":"#8fdff7"},""]}
tellraw @a [{"text":"\nSuccessfully installed ","color":"#8fdff7"},{"text":"tryashtar's","color":"#3376d4","hoverEvent":{"action":"show_text","contents":{"text":"(click to see more of my stuff)","color":"gray"}},"clickEvent":{"action":"open_url","value":"https://youtube.com/c/tryashtar"}},{"text":" Shulker Preview Pack!\nThank you and enjoy.","color":"#8fdff7"}]
function tryashtar.shulker_preview:.config/show_settings
