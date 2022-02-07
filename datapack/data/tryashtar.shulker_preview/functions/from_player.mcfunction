scoreboard players set #done shulker_preview 2

# turn arbitrary NBT back into real item in global shulker box
data modify block ~ 1 ~ Items[0].tag.shulker_items[0].Slot set value 0b
data modify block ~ 1 ~ Items[0] set from block ~ 1 ~ Items[0].tag.shulker_items[0]

# read contents of item inside global shulker box to create entities, and copy the entity names to the lore
function tryashtar.shulker_preview:analyze

data modify block ~ 1 ~ Items[0].tag.display.Lore set value []
data modify block ~ 1 ~ Items[0].tag.display.Lore append from block ~2 1 ~ Text1
data modify block ~ 1 ~ Items[0].tag.display.Lore append from block ~2 1 ~ Text2
data modify block ~ 1 ~ Items[0].tag.display.Lore append from block ~2 1 ~ Text3
data modify block ~ 1 ~ Items[0].tag.display.Lore append from block ~2 1 ~ Text4
data modify block ~ 1 ~ Items[0].tag.display.Lore append from block ~3 1 ~ Text1
execute if score #total shulker_preview matches 1.. run data modify block ~ 1 ~ Items[0].tag.display.Lore append from block ~3 1 ~ Text2
execute unless score #total shulker_preview matches 1.. run data modify block ~ 1 ~ Items[0].tag.display.Lore append value '""'
execute if score #modded shulker_preview matches 2 store result block ~ 1 ~ Items[0].tag.shulker_length int 1 run data get block ~ 1 ~ Items[0].tag.display.Lore[1]

data modify block ~ 1 ~ Items[0].tag.HideFlags set value 32
data modify block ~ 1 ~ Items[0].tag.shulker_processed set value 1b

# return processed container to its original slot
execute if score #slot shulker_preview matches 0 run loot replace entity @s hotbar.0 1 mine ~ 1 ~ golden_pickaxe{drop_contents:true}
execute if score #slot shulker_preview matches 1 run loot replace entity @s hotbar.1 1 mine ~ 1 ~ golden_pickaxe{drop_contents:true}
execute if score #slot shulker_preview matches 2 run loot replace entity @s hotbar.2 1 mine ~ 1 ~ golden_pickaxe{drop_contents:true}
execute if score #slot shulker_preview matches 3 run loot replace entity @s hotbar.3 1 mine ~ 1 ~ golden_pickaxe{drop_contents:true}
execute if score #slot shulker_preview matches 4 run loot replace entity @s hotbar.4 1 mine ~ 1 ~ golden_pickaxe{drop_contents:true}
execute if score #slot shulker_preview matches 5 run loot replace entity @s hotbar.5 1 mine ~ 1 ~ golden_pickaxe{drop_contents:true}
execute if score #slot shulker_preview matches 6 run loot replace entity @s hotbar.6 1 mine ~ 1 ~ golden_pickaxe{drop_contents:true}
execute if score #slot shulker_preview matches 7 run loot replace entity @s hotbar.7 1 mine ~ 1 ~ golden_pickaxe{drop_contents:true}
execute if score #slot shulker_preview matches 8 run loot replace entity @s hotbar.8 1 mine ~ 1 ~ golden_pickaxe{drop_contents:true}
execute if score #slot shulker_preview matches 9 run loot replace entity @s inventory.0 1 mine ~ 1 ~ golden_pickaxe{drop_contents:true}
execute if score #slot shulker_preview matches 10 run loot replace entity @s inventory.1 1 mine ~ 1 ~ golden_pickaxe{drop_contents:true}
execute if score #slot shulker_preview matches 11 run loot replace entity @s inventory.2 1 mine ~ 1 ~ golden_pickaxe{drop_contents:true}
execute if score #slot shulker_preview matches 12 run loot replace entity @s inventory.3 1 mine ~ 1 ~ golden_pickaxe{drop_contents:true}
execute if score #slot shulker_preview matches 13 run loot replace entity @s inventory.4 1 mine ~ 1 ~ golden_pickaxe{drop_contents:true}
execute if score #slot shulker_preview matches 14 run loot replace entity @s inventory.5 1 mine ~ 1 ~ golden_pickaxe{drop_contents:true}
execute if score #slot shulker_preview matches 15 run loot replace entity @s inventory.6 1 mine ~ 1 ~ golden_pickaxe{drop_contents:true}
execute if score #slot shulker_preview matches 16 run loot replace entity @s inventory.7 1 mine ~ 1 ~ golden_pickaxe{drop_contents:true}
execute if score #slot shulker_preview matches 17 run loot replace entity @s inventory.8 1 mine ~ 1 ~ golden_pickaxe{drop_contents:true}
execute if score #slot shulker_preview matches 18 run loot replace entity @s inventory.9 1 mine ~ 1 ~ golden_pickaxe{drop_contents:true}
execute if score #slot shulker_preview matches 19 run loot replace entity @s inventory.10 1 mine ~ 1 ~ golden_pickaxe{drop_contents:true}
execute if score #slot shulker_preview matches 20 run loot replace entity @s inventory.11 1 mine ~ 1 ~ golden_pickaxe{drop_contents:true}
execute if score #slot shulker_preview matches 21 run loot replace entity @s inventory.12 1 mine ~ 1 ~ golden_pickaxe{drop_contents:true}
execute if score #slot shulker_preview matches 22 run loot replace entity @s inventory.13 1 mine ~ 1 ~ golden_pickaxe{drop_contents:true}
execute if score #slot shulker_preview matches 23 run loot replace entity @s inventory.14 1 mine ~ 1 ~ golden_pickaxe{drop_contents:true}
execute if score #slot shulker_preview matches 24 run loot replace entity @s inventory.15 1 mine ~ 1 ~ golden_pickaxe{drop_contents:true}
execute if score #slot shulker_preview matches 25 run loot replace entity @s inventory.16 1 mine ~ 1 ~ golden_pickaxe{drop_contents:true}
execute if score #slot shulker_preview matches 26 run loot replace entity @s inventory.17 1 mine ~ 1 ~ golden_pickaxe{drop_contents:true}
execute if score #slot shulker_preview matches 27 run loot replace entity @s inventory.18 1 mine ~ 1 ~ golden_pickaxe{drop_contents:true}
execute if score #slot shulker_preview matches 28 run loot replace entity @s inventory.19 1 mine ~ 1 ~ golden_pickaxe{drop_contents:true}
execute if score #slot shulker_preview matches 29 run loot replace entity @s inventory.20 1 mine ~ 1 ~ golden_pickaxe{drop_contents:true}
execute if score #slot shulker_preview matches 30 run loot replace entity @s inventory.21 1 mine ~ 1 ~ golden_pickaxe{drop_contents:true}
execute if score #slot shulker_preview matches 31 run loot replace entity @s inventory.22 1 mine ~ 1 ~ golden_pickaxe{drop_contents:true}
execute if score #slot shulker_preview matches 32 run loot replace entity @s inventory.23 1 mine ~ 1 ~ golden_pickaxe{drop_contents:true}
execute if score #slot shulker_preview matches 33 run loot replace entity @s inventory.24 1 mine ~ 1 ~ golden_pickaxe{drop_contents:true}
execute if score #slot shulker_preview matches 34 run loot replace entity @s inventory.25 1 mine ~ 1 ~ golden_pickaxe{drop_contents:true}
execute if score #slot shulker_preview matches 35 run loot replace entity @s inventory.26 1 mine ~ 1 ~ golden_pickaxe{drop_contents:true}
execute if score #slot shulker_preview matches -106 run loot replace entity @s weapon.offhand 1 mine ~ 1 ~ golden_pickaxe{drop_contents:true}
