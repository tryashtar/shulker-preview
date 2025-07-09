# calculate the weight of a bundle inside another bundle
# the ongoing context so far must be preserved in a simple stack
execute store result storage tryashtar.shulker_preview:data bundle_stack[-1].fullness int 1 run scoreboard players get #fullness shulker_preview
scoreboard players set #fullness shulker_preview 0
scoreboard players set #count shulker_preview 0
data modify storage tryashtar.shulker_preview:data bundle_stack append value {fullness:0}
data modify storage tryashtar.shulker_preview:data bundle_stack[-1].contents set from storage tryashtar.shulker_preview:data bundle_stack[-2].contents[-1].components."minecraft:bundle_contents"

# context is clear, calculate the weight of this bundle
# also add 4/64 extra weight
execute if data storage tryashtar.shulker_preview:data bundle_stack[-1].contents[0] run function tryashtar.shulker_preview:render/bundle_weight
scoreboard players operation #count shulker_preview = #fullness shulker_preview
scoreboard players add #count shulker_preview 4000

# pop the previous context from the stack when returning
execute store result score #fullness shulker_preview run data get storage tryashtar.shulker_preview:data bundle_stack[-2].fullness
data remove storage tryashtar.shulker_preview:data bundle_stack[-1]
