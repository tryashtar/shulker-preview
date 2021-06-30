# check for integrity of loot table override
replaceitem block 29999977 1 9832 container.0 tnt
loot replace block 29999977 1 9832 container.0 mine 29999977 1 9832 golden_pickaxe{drop_contents:true}
execute store success score #loot_table shulker_preview if data block 29999977 1 9832 {Items:[{id:"minecraft:tnt"}]}
execute if score #loot_table shulker_preview matches 0 run tellraw @a [{"text":"\nWarning!\nThe shulker box loot table appears to have been modified by another data pack. This prevents shulker previews from working.\n","color":"#d11b1b"},{"text":"You can disable shulker previews then re-enable it to fix this, but that might break the other data pack. If you're still seeing this message, try ","color":"yellow"},{"text":"redownloading the data pack for your version\n","color":"#78b9ff","underlined":true,"clickEvent":{"action":"open_url","value":"https://tryashtar.github.io/shulker-preview"}}]

# check for sufficient Minecraft version
execute store result score #version shulker_preview run data get entity @a[limit=1] DataVersion
execute if score #version shulker_preview matches 1..2528 run tellraw @a [{"text":"\nOutdated Minecraft version!\nYou need to be on version ","color":"red"},{"text":"20w17a","color":"yellow"},{"text":" or later for shulker previews to work!\n"},{"text":"Download for older versions here\n","color":"blue","underlined":true,"clickEvent":{"action":"open_url","value":"https://tryashtar.github.io/shulker-preview"}}]
execute if score #version shulker_preview matches 1..2528 run scoreboard players set #setup shulker_preview -1
execute if score #version shulker_preview matches 2529.. if score #setup shulker_preview matches -1 run scoreboard players set #setup shulker_preview 0

# check for resource pack equipped/success message
scoreboard players add #setup shulker_preview 0
execute if score #setup shulker_preview matches 0 run tellraw @a {"translate":"%1$s%418634357$s","with":[{"text":"\nDon't forget to equip the shulker preview resource pack!\n","color":"#8fdff7"},""]}
execute if score #setup shulker_preview matches 0 run tellraw @a [{"text":"\nSuccessfully installed ","color":"#8fdff7"},{"text":"tryashtar's","color":"#3376d4","hoverEvent":{"action":"show_text","contents":{"text":"(click to see more of my stuff)","color":"gray"}},"clickEvent":{"action":"open_url","value":"https://youtube.com/c/tryashtar"}},{"text":" Shulker Preview Pack!\nThank you and enjoy.\n","color":"#8fdff7"},{"text":"You can also click this text to add previews to Ender Chests.\n","color":"#ac6bb5","hoverEvent":{"action":"show_text","contents":[{"text":"NOTE:\n","color":"red"},{"text":"This is experimental and may not work in all cases.","color":"gray"}]},"clickEvent":{"action":"run_command","value":"/function tryashtar.shulker_preview:.meta/enable_ender"}}]
execute if score #setup shulker_preview matches 0 run scoreboard players set #setup shulker_preview 1

# check for modded server
scoreboard players add #modded shulker_preview 0
execute if score #modded shulker_preview matches 0 store success score #modded shulker_preview run data get entity @a[limit=1] "Spigot.ticksLived"
execute if score #modded shulker_preview matches 0 store success score #modded shulker_preview run data get entity @a[limit=1] "Bukkit.updateLevel"
execute if score #modded shulker_preview matches 0 store success score #modded shulker_preview run data get entity @a[limit=1] "Paper.SpawnReason"

execute if score #modded shulker_preview matches 1 run tellraw @a [{"text":"\n⚠ ","color":"#ebdd23"},{"text":"Modded server detected!","color":"#d11b1b"},{"text":" ⚠\n","color":"#ebdd23"},{"text":"Bukkit and its derivatives break vanilla behavior that shulker previews relies on, specifically long lore on items.\nAs a workaround, the pack will attempt to switch to a slightly slower method that generates shorter lore.","color":"#f06e6e"},{"text":"\n⚠ ","color":"#ebdd23"},{"text":"There is no guarantee this will work!","color":"#d11b1b"},{"text":" ⚠\n","color":"#ebdd23"}]
execute if score #modded shulker_preview matches 1 run scoreboard players set #modded shulker_preview 2
