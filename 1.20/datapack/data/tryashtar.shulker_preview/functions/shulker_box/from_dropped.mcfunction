data modify storage tryashtar.shulker_preview:data tooltip set value ['{"translate":"tryashtar.shulker_preview.shulker_tooltip"}']
data modify storage tryashtar.shulker_preview:data contents set from entity @s Item.components."minecraft:container"

# summon item holder to run predicates against
summon item ~ -10000 ~ {Invulnerable:1b,NoGravity:1b,Silent:1b,UUID:[I;1936225644,1801810464,1886545270,1768257313],Item:{id:"tnt",count:1}}
execute as 7368756c-6b65-7220-7072-657669657721 run function tryashtar.shulker_preview:analyze

# first item
data modify entity 7368756c-6b65-7220-7072-657669657721 Item set from storage tryashtar.shulker_preview:data contents[0]
execute store result score #amount shulker_preview run data get storage tryashtar.shulker_preview:data contents[0].count
execute if score #amount shulker_preview matches 1.. if items entity 7368756c-6b65-7220-7072-657669657721 weapon *[custom_name] run item modify entity @s contents tryashtar.shulker_preview:first_row/named
execute if score #amount shulker_preview matches 1.. unless items entity 7368756c-6b65-7220-7072-657669657721 weapon *[custom_name] run item modify entity @s contents tryashtar.shulker_preview:first_row/unnamed
execute if score #amount shulker_preview matches ..0 run item modify entity 7368756c-6b65-7220-7072-657669657721 contents tryashtar.shulker_preview:first_row/empty

# don't process any more items this tick
scoreboard players set #ready shulker_preview 0
kill 7368756c-6b65-7220-7072-657669657721
