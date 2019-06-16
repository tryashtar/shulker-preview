# skip this chest unless we end up actually scanning it
scoreboard players set #done shulker_preview 0

execute store result score #box_uuid shulker_preview run data get block ~ 1 ~ Items[0].tag.shulker_items[0].tag.uuid
execute store result score #box_contents shulker_preview run data get block ~ 1 ~ Items[0].tag.shulker_items[0].tag.contents

execute store result block ~ 1 ~ Items[0].tag.shulker_items[0].tag.uuid int 1 run scoreboard players get #uuid shulker_preview
execute store result block ~ 1 ~ Items[0].tag.shulker_items[0].tag.contents int 1 run scoreboard players get #contents shulker_preview

# copy player ender items to ender chest item so we can reuse shulker box technique
data modify block ~ 1 ~ Items[0].tag.shulker_items[0].tag.BlockEntityTag.Items set from entity @s EnderItems

# if "cached" UUID/contents in chest doesn't match updated values from player, update it
execute unless score #uuid shulker_preview = #box_uuid shulker_preview run function tryashtar.shulker_preview:from_player
execute if score #uuid shulker_preview = #box_uuid shulker_preview unless score #contents shulker_preview = #box_contents shulker_preview run function tryashtar.shulker_preview:from_player
