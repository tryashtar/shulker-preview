version = ctx.meta['shulker_preview']['target_version']

# check for integrity of loot table override
replaceitem block 29999977 1 9832 container.0 tnt{loot_integrity:1b}
loot replace block 29999977 1 9832 container.0 mine 29999977 1 9832 golden_pickaxe{drop_contents:1b}
execute store success score #loot_table shulker_preview if data block 29999977 1 9832 {Items:[{tag:{loot_integrity:1b}}]}
execute if score #loot_table shulker_preview matches 0 run tellraw @a [{"text":"\\n⚠ ","color":"yellow"},{"text":"Broken loot table!","color":"red"},{"text":" ⚠\\n","color":"yellow"},{"text":"The shulker box loot table appears to have been modified by another data pack. This prevents shulker previews from working.\\n","color":"red"}]
execute if score #loot_table shulker_preview matches 0 run scoreboard players set #install shulker_preview -2
execute if score #loot_table shulker_preview matches 1 if score #install shulker_preview matches -2 run scoreboard players set #install shulker_preview 0

# check for sufficient Minecraft version
execute store result score #version shulker_preview run data get entity @a[limit=1] DataVersion
execute if score #version shulker_preview matches (1,version.last.world-1) run tellraw @a [{"text":"\\n⚠ ","color":"yellow"},{"text":"Outdated Minecraft version!","color":"red"},{"text":" ⚠\\n","color":"yellow"},{"text":f"This shulker preview data pack is for version {version.first.name}.\\n","color":"red"},{"text":"Download for other versions here","color":"blue","underlined":true,"clickEvent":{"action":"open_url","value":"https://tryashtar.github.io/shulker-preview"}},"\\n"]
execute if score #version shulker_preview matches (1,version.first.world-1) run scoreboard players set #install shulker_preview -1
execute if score #version shulker_preview matches (version.last.world+1,None) run tellraw @a [{"text":"\\n⚠ ","color":"yellow"},{"text":"Outdated Shulker Preview version!","color":"red"},{"text":" ⚠\\n","color":"yellow"},{"text":f"This data pack is for version {version.first.name}.\\n","color":"red"},{"text":"Download for other versions here","color":"blue","underlined":true,"clickEvent":{"action":"open_url","value":"https://tryashtar.github.io/shulker-preview"}},"\\n"]
execute if score #version shulker_preview matches (version.last.world+1,None) run scoreboard players set #install shulker_preview -1
execute if score #version shulker_preview matches (version.first.world,version.last.world) if score #install shulker_preview matches -1 run scoreboard players set #install shulker_preview 0

# check for resource pack equipped/success message
scoreboard players add #install shulker_preview 0
execute if score #install shulker_preview matches 0 run function tryashtar.shulker_preview:meta/install

# check for modded server
scoreboard players add #modded shulker_preview 0
execute if score #modded shulker_preview matches 0 store success score #modded shulker_preview run data get entity @a[limit=1] "Spigot.ticksLived"
execute if score #modded shulker_preview matches 0 store success score #modded shulker_preview run data get entity @a[limit=1] "Bukkit.updateLevel"
execute if score #modded shulker_preview matches 0 store success score #modded shulker_preview run data get entity @a[limit=1] "Paper.SpawnReason"

execute if score #modded shulker_preview matches 1 run tellraw @a [{"text":"\\n⚠ ","color":"yellow"},{"text":"Modded server detected!","color":"red"},{"text":" ⚠\\n","color":"yellow"},{"text":"Bukkit and its derivatives can break vanilla behavior that shulker previews relies on.","color":"red"},{"text":"\\n⚠ ","color":"yellow"},{"text":"There is no guarantee it will work!","color":"red"},{"text":" ⚠\\n","color":"yellow"}]
execute if score #modded shulker_preview matches 1 run scoreboard players set #modded shulker_preview 2
