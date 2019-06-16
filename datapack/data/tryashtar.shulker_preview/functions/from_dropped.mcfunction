# read contents of item inside global shulker box to create entities, and copy the entity names to the lore
data remove block ~ 1 ~ Items
data modify block ~ 1 ~ Items append from entity @s Item
scoreboard players set #uuid shulker_preview -1
function tryashtar.shulker_preview:analyze
data modify entity @s Item.tag.display.Lore set value ['"\\uF82C\\uF82A\\uF827"','""','""','""','""']
data modify entity @s Item.tag.display.Lore prepend from block ~2 1 ~ Text1
data modify entity @s Item.tag.HideFlags set value 32
data modify entity @s Item.tag.shulker_processed set value 1b
