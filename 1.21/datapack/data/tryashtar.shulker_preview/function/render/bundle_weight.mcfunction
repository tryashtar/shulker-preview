# recursively calculate the weight of a bundle, where 64000 is full
# first, get the count of an item in the bundle
# determine the max stack size with a set_count function, then divide
execute store result score #count shulker_preview run data get storage tryashtar.shulker_preview:data bundle_stack[-1].contents[-1].count 64000
data modify entity @s Item set from storage tryashtar.shulker_preview:data bundle_stack[-1].contents[-1]
item modify entity @s contents {function:"set_count",count:99999}
execute store result score #max shulker_preview run data get entity @s Item.count
scoreboard players operation #count shulker_preview /= #max shulker_preview

# bundles inside of bundles add their weight, plus 4/64
execute if items entity @s contents *[bundle_contents] run function tryashtar.shulker_preview:render/bundle_nested
scoreboard players operation #fullness shulker_preview += #count shulker_preview

# bees make a bundle instantly full
execute if data storage tryashtar.shulker_preview:data bundle_stack[-1].contents[-1].components."minecraft:bees"[0] run scoreboard players set #fullness shulker_preview 64000

# iterate to the next item in the bundle
data remove storage tryashtar.shulker_preview:data bundle_stack[-1].contents[-1]
execute if data storage tryashtar.shulker_preview:data bundle_stack[-1].contents[0] run function tryashtar.shulker_preview:render/bundle_weight
