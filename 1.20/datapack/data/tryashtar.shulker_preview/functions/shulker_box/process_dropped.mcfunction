# initialize the tooltip text component array that all rendering appends to
data modify storage tryashtar.shulker_preview:data tooltip set value ['{"translate":"tryashtar.shulker_preview.shulker_tooltip"}']

# when necessary, NBT lookups are faster in storage, and permit destructive iteration
# so pre-emptively copy the shulker box items to storage
data modify storage tryashtar.shulker_preview:data contents set from entity @s Item.components."minecraft:container"

# we can directly modify this item, it doesn't need to be copied anywhere
function tryashtar.shulker_preview:process
