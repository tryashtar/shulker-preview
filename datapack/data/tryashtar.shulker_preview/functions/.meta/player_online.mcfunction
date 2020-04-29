execute store result score #version shulker_preview run data get entity @a[limit=1] DataVersion
execute if score #version shulker_preview matches 1..1967 run tellraw @a [{"text":"\nOutdated Minecraft version!\nYou need to be on version ","color":"red"},{"text":"1.14.3","color":"yellow"},{"text":" or later for shulker previews to work!"}]
execute if score #version shulker_preview matches 1..1967 run scoreboard players set #setup shulker_preview -1
execute if score #version shulker_preview matches 1968.. if score #setup shulker_preview matches -1 run scoreboard players set #setup shulker_preview 0

scoreboard players add #setup shulker_preview 0
execute if score #setup shulker_preview matches 0 run tellraw @a {"translate":"%1$s%418634357$s","with":[{"text":"\nDon't forget to equip the resource pack!\n\n","color":"#8fdff7"},""]}
execute if score #setup shulker_preview matches 0 run tellraw @a [{"text":"\n\nSuccessfully installed ","color":"#8fdff7"},{"text":"tryashtar's","color":"#3376d4","hoverEvent":{"action":"show_text","value":{"text":"(click to see more of my stuff)","color":"gray"}},"clickEvent":{"action":"open_url","value":"https://youtube.com/c/tryashtar"}},{"text":" Shulker Preview Pack!\nThank you and enjoy.\n\n","color":"#8fdff7"},{"text":"You can also click this text to add previews to Ender Chests.\n\n\n","color":"#ac6bb5","hoverEvent":{"action":"show_text","value":[{"text":"NOTE:\n","color":"red"},{"text":"This is experimental and will prevent ender chests from stacking.","color":"gray"}]},"clickEvent":{"action":"run_command","value":"/function tryashtar.shulker_preview:.meta/enable_ender"}}]
execute if score #setup shulker_preview matches 0 run scoreboard players set #setup shulker_preview 1

scoreboard players add #modded shulker_preview 0
execute if score #modded shulker_preview matches 0 store success score #modded shulker_preview run data get entity @a[limit=1] "Spigot.ticksLived"
execute if score #modded shulker_preview matches 0 store success score #modded shulker_preview run data get entity @a[limit=1] "Bukkit.updateLevel"
execute if score #modded shulker_preview matches 0 store success score #modded shulker_preview run data get entity @a[limit=1] "Paper.SpawnReason"

execute if score #modded shulker_preview matches 1 run tellraw @a {"text":"\nModded server detected! There is no guarantee shulker previews will be compatible!\n\n","color":"#d11b1b"}
execute if score #modded shulker_preview matches 1 run scoreboard players set #modded shulker_preview 2
