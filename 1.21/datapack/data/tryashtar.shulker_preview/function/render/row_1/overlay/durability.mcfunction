# render the durability bar
# first we get the current damage of the item, then see what the damage would be if set to a specific ratio
# if the current damage is less than these thresholds, use that corresponding bar width and color
execute store result score #damage shulker_preview run data get storage tryashtar.shulker_preview:data item.components."minecraft:damage"
item modify entity @s contents {function:"set_damage",damage:0.9615384615384616}
execute store result score #threshold shulker_preview run data get entity @s Item.components."minecraft:damage"
execute if score #damage shulker_preview <= #threshold shulker_preview run return run data modify storage tryashtar.shulker_preview:data tooltip append value '{"translate":"tryashtar.shulker_preview.durability.0.1","color":"#00ff00"}'
item modify entity @s contents {function:"set_damage",damage:0.8846153846153846}
execute store result score #threshold shulker_preview run data get entity @s Item.components."minecraft:damage"
execute if score #damage shulker_preview <= #threshold shulker_preview run return run data modify storage tryashtar.shulker_preview:data tooltip append value '{"translate":"tryashtar.shulker_preview.durability.1.1","color":"#27ff00"}'
item modify entity @s contents {function:"set_damage",damage:0.8076923076923077}
execute store result score #threshold shulker_preview run data get entity @s Item.components."minecraft:damage"
execute if score #damage shulker_preview <= #threshold shulker_preview run return run data modify storage tryashtar.shulker_preview:data tooltip append value '{"translate":"tryashtar.shulker_preview.durability.2.1","color":"#4eff00"}'
item modify entity @s contents {function:"set_damage",damage:0.7307692307692308}
execute store result score #threshold shulker_preview run data get entity @s Item.components."minecraft:damage"
execute if score #damage shulker_preview <= #threshold shulker_preview run return run data modify storage tryashtar.shulker_preview:data tooltip append value '{"translate":"tryashtar.shulker_preview.durability.3.1","color":"#75ff00"}'
item modify entity @s contents {function:"set_damage",damage:0.6538461538461539}
execute store result score #threshold shulker_preview run data get entity @s Item.components."minecraft:damage"
execute if score #damage shulker_preview <= #threshold shulker_preview run return run data modify storage tryashtar.shulker_preview:data tooltip append value '{"translate":"tryashtar.shulker_preview.durability.4.1","color":"#9cff00"}'
item modify entity @s contents {function:"set_damage",damage:0.5769230769230769}
execute store result score #threshold shulker_preview run data get entity @s Item.components."minecraft:damage"
execute if score #damage shulker_preview <= #threshold shulker_preview run return run data modify storage tryashtar.shulker_preview:data tooltip append value '{"translate":"tryashtar.shulker_preview.durability.5.1","color":"#c4ff00"}'
item modify entity @s contents {function:"set_damage",damage:0.5}
execute store result score #threshold shulker_preview run data get entity @s Item.components."minecraft:damage"
execute if score #damage shulker_preview <= #threshold shulker_preview run return run data modify storage tryashtar.shulker_preview:data tooltip append value '{"translate":"tryashtar.shulker_preview.durability.6.1","color":"#ebff00"}'
item modify entity @s contents {function:"set_damage",damage:0.42307692307692313}
execute store result score #threshold shulker_preview run data get entity @s Item.components."minecraft:damage"
execute if score #damage shulker_preview <= #threshold shulker_preview run return run data modify storage tryashtar.shulker_preview:data tooltip append value '{"translate":"tryashtar.shulker_preview.durability.7.1","color":"#ffeb00"}'
item modify entity @s contents {function:"set_damage",damage:0.34615384615384615}
execute store result score #threshold shulker_preview run data get entity @s Item.components."minecraft:damage"
execute if score #damage shulker_preview <= #threshold shulker_preview run return run data modify storage tryashtar.shulker_preview:data tooltip append value '{"translate":"tryashtar.shulker_preview.durability.8.1","color":"#ffc400"}'
item modify entity @s contents {function:"set_damage",damage:0.2692307692307693}
execute store result score #threshold shulker_preview run data get entity @s Item.components."minecraft:damage"
execute if score #damage shulker_preview <= #threshold shulker_preview run return run data modify storage tryashtar.shulker_preview:data tooltip append value '{"translate":"tryashtar.shulker_preview.durability.9.1","color":"#ff9c00"}'
item modify entity @s contents {function:"set_damage",damage:0.1923076923076923}
execute store result score #threshold shulker_preview run data get entity @s Item.components."minecraft:damage"
execute if score #damage shulker_preview <= #threshold shulker_preview run return run data modify storage tryashtar.shulker_preview:data tooltip append value '{"translate":"tryashtar.shulker_preview.durability.10.1","color":"#ff7500"}'
item modify entity @s contents {function:"set_damage",damage:0.11538461538461542}
execute store result score #threshold shulker_preview run data get entity @s Item.components."minecraft:damage"
execute if score #damage shulker_preview <= #threshold shulker_preview run return run data modify storage tryashtar.shulker_preview:data tooltip append value '{"translate":"tryashtar.shulker_preview.durability.11.1","color":"#ff4e00"}'
item modify entity @s contents {function:"set_damage",damage:0.038461538461538436}
execute store result score #threshold shulker_preview run data get entity @s Item.components."minecraft:damage"
execute if score #damage shulker_preview <= #threshold shulker_preview run return run data modify storage tryashtar.shulker_preview:data tooltip append value '{"translate":"tryashtar.shulker_preview.durability.12.1","color":"#ff2700"}'
data modify storage tryashtar.shulker_preview:data tooltip append value '{"translate":"tryashtar.shulker_preview.durability.13.1"}'
