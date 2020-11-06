# check for integrity of loot table override
replaceitem block 29999977 1 9832 container.0 tnt
loot replace block 29999977 1 9832 container.0 mine 29999977 1 9832 golden_pickaxe{drop_contents:true}
execute store success score #loot_table shulker_preview if data block 29999977 1 9832 {Items:[{id:"minecraft:tnt"}]}
execute if score #loot_table shulker_preview matches 0 run tellraw @a [{"text":"\nWarning!\nThe shulker box loot table appears to have been modified by another data pack. This prevents shulker previews from working.\n","color":"#d11b1b"},{"text":"You can disable shulker previews then re-enable it to fix this, but that might break the other data pack. If you're still seeing this message, try ","color":"yellow"},{"text":"redownloading the data pack for your version\n","color":"#78b9ff","underlined":true,"clickEvent":{"action":"open_url","value":"https://tryashtar.github.io/shulker-preview"}}]
execute if score #loot_table shulker_preview matches 0 run scoreboard players set #install shulker_preview -2
execute if score #loot_table shulker_preview matches 1 if score #install shulker_preview matches -2 run scoreboard players set #install shulker_preview 0

# check for sufficient Minecraft version
execute store result score #version shulker_preview run data get entity @a[limit=1] DataVersion
execute if score #version shulker_preview matches 1..2528 run tellraw @a [{"text":"\nOutdated Minecraft version!\nYou need to be on version ","color":"red"},{"text":"20w17a","color":"yellow"},{"text":" or later for shulker previews to work!\n"},{"text":"Download for older versions here\n","color":"blue","underlined":true,"clickEvent":{"action":"open_url","value":"https://tryashtar.github.io/shulker-preview"}}]
execute if score #version shulker_preview matches 1..2528 run scoreboard players set #install shulker_preview -1
execute if score #version shulker_preview matches 2529.. if score #install shulker_preview matches -1 run scoreboard players set #install shulker_preview 0

# check for resource pack equipped/success message
scoreboard players add #install shulker_preview 0
execute if score #install shulker_preview matches 0 run function tryashtar.shulker_preview:.meta/install

# check for modded server
scoreboard players add #modded shulker_preview 0
execute if score #modded shulker_preview matches 0 store success score #modded shulker_preview run data get entity @a[limit=1] "Spigot.ticksLived"
execute if score #modded shulker_preview matches 0 store success score #modded shulker_preview run data get entity @a[limit=1] "Bukkit.updateLevel"
execute if score #modded shulker_preview matches 0 store success score #modded shulker_preview run data get entity @a[limit=1] "Paper.SpawnReason"

execute if score #modded shulker_preview matches 1 run tellraw @a {"text":"\nModded server detected! There is no guarantee shulker previews will be compatible!\n","color":"#d11b1b"}
execute if score #modded shulker_preview matches 1 run scoreboard players set #modded shulker_preview 2
