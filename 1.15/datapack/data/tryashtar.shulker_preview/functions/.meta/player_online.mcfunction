execute store result score #version shulker_preview run data get entity @a[limit=1] DataVersion
execute if score #version shulker_preview matches 1..2224 run tellraw @a [{"text":"\nOutdated Minecraft version!\nYou need to be on version ","color":"red"},{"text":"1.15","color":"yellow"},{"text":" or later for shulker previews to work!"}]
execute if score #version shulker_preview matches 1..2224 run scoreboard players set #setup shulker_preview -1
execute if score #version shulker_preview matches 2225.. if score #setup shulker_preview matches -1 run scoreboard players set #setup shulker_preview 0

scoreboard players add #setup shulker_preview 0
execute if score #setup shulker_preview matches 0 run tellraw @a {"translate":"%1$s","with":[{"text":"\nDon't forget to equip the resource pack!\n","color":"red"},""]}
execute if score #setup shulker_preview matches 0 run tellraw @a [{"text":"Successfully installed ","color":"green"},{"text":"tryashtar's","color":"blue","hoverEvent":{"action":"show_text","value":{"text":"(click to see more of my stuff)","color":"gray"}},"clickEvent":{"action":"open_url","value":"https://youtube.com/c/tryashtar"}},{"text":" Shulker Preview Pack!\nThank you and enjoy.\n\n","color":"green"},{"text":"You can also click this text to add previews to Ender Chests.","color":"yellow","hoverEvent":{"action":"show_text","value":[{"text":"NOTE:\n","color":"red"},{"text":"This is experimental and will prevent ender chests from stacking.","color":"gray"}]},"clickEvent":{"action":"run_command","value":"/function tryashtar.shulker_preview:.meta/enable_ender"}}]
execute if score #setup shulker_preview matches 0 run scoreboard players set #setup shulker_preview 1

scoreboard players add #modded shulker_preview 0
execute if score #modded shulker_preview matches 0 store success score #modded shulker_preview run data get entity @a[limit=1] "Spigot.ticksLived"
execute if score #modded shulker_preview matches 0 store success score #modded shulker_preview run data get entity @a[limit=1] "Bukkit.updateLevel"
execute if score #modded shulker_preview matches 0 store success score #modded shulker_preview run data get entity @a[limit=1] "Paper.SpawnReason"

execute if score #modded shulker_preview matches 1 run tellraw @a [{"text":"\n⚠ ","color":"dark_red"},{"text":"Modded server detected!","color":"red"},{"text":" ⚠\n","color":"dark_red"},{"text":"Bukkit and its derivatives break vanilla behavior that shulker previews relies on, specifically long lore on items.\nAs a workaround, the pack will attempt to switch to a slightly slower method that generates shorter lore.","color":"yellow"},{"text":"\n⚠ ","color":"dark_red"},{"text":"There is no guarantee this will work!","color":"red"},{"text":" ⚠\n","color":"dark_red"}]
execute if score #modded shulker_preview matches 1 run scoreboard players set #modded shulker_preview 2
