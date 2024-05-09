execute store result score #count shulker_preview run data get storage tryashtar.shulker_preview:data bundle_stack[-1].contents[-1].count 64000
data modify entity @s HandItems[1] set from storage tryashtar.shulker_preview:data bundle_stack[-1].contents[-1]
item modify entity @s weapon.offhand {function:"set_count",count:99999}
execute store result score #max shulker_preview run data get entity @s HandItems[1].count
scoreboard players operation #count shulker_preview /= #max shulker_preview
execute if items entity @s weapon.offhand *[bundle_contents] run function tryashtar.shulker_preview:bundle_nested
scoreboard players operation #fullness shulker_preview += #count shulker_preview
execute if data storage tryashtar.shulker_preview:data bundle_stack[-1].contents[-1].components."minecraft:bees"[0] run scoreboard players set #fullness shulker_preview 64000

data remove storage tryashtar.shulker_preview:data bundle_stack[-1].contents[-1]
execute if data storage tryashtar.shulker_preview:data bundle_stack[-1].contents[0] run function tryashtar.shulker_preview:bundle_weight
