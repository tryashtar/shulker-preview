# summon item holder to run predicates against
summon item_frame ~ -10000 ~ {Invulnerable:1b,NoGravity:1b,Silent:1b,Fixed:1b,Invisible:1b,UUID:[I;1936225644,1801810464,1886545270,1768257313]}

# copy and analyze contents one by one
data modify storage tryashtar.shulker_preview:data item set from storage tryashtar.shulker_preview:data contents[{slot:0}].item
execute if data storage tryashtar.shulker_preview:data contents[{slot:0}] as 7368756c-6b65-7220-7072-657669657721 run function tryashtar.shulker_preview:row_0/process_item
execute unless data storage tryashtar.shulker_preview:data contents[{slot:0}] run data modify storage tryashtar.shulker_preview:data tooltip append value '{"translate":"tryashtar.shulker_preview.empty_slot"}'

data modify storage tryashtar.shulker_preview:data item set from storage tryashtar.shulker_preview:data contents[{slot:1}].item
execute if data storage tryashtar.shulker_preview:data contents[{slot:1}] as 7368756c-6b65-7220-7072-657669657721 run function tryashtar.shulker_preview:row_0/process_item
execute unless data storage tryashtar.shulker_preview:data contents[{slot:1}] run data modify storage tryashtar.shulker_preview:data tooltip append value '{"translate":"tryashtar.shulker_preview.empty_slot"}'

data modify storage tryashtar.shulker_preview:data item set from storage tryashtar.shulker_preview:data contents[{slot:2}].item
execute if data storage tryashtar.shulker_preview:data contents[{slot:2}] as 7368756c-6b65-7220-7072-657669657721 run function tryashtar.shulker_preview:row_0/process_item
execute unless data storage tryashtar.shulker_preview:data contents[{slot:2}] run data modify storage tryashtar.shulker_preview:data tooltip append value '{"translate":"tryashtar.shulker_preview.empty_slot"}'

data modify storage tryashtar.shulker_preview:data item set from storage tryashtar.shulker_preview:data contents[{slot:3}].item
execute if data storage tryashtar.shulker_preview:data contents[{slot:3}] as 7368756c-6b65-7220-7072-657669657721 run function tryashtar.shulker_preview:row_0/process_item
execute unless data storage tryashtar.shulker_preview:data contents[{slot:3}] run data modify storage tryashtar.shulker_preview:data tooltip append value '{"translate":"tryashtar.shulker_preview.empty_slot"}'

data modify storage tryashtar.shulker_preview:data item set from storage tryashtar.shulker_preview:data contents[{slot:4}].item
execute if data storage tryashtar.shulker_preview:data contents[{slot:4}] as 7368756c-6b65-7220-7072-657669657721 run function tryashtar.shulker_preview:row_0/process_item
execute unless data storage tryashtar.shulker_preview:data contents[{slot:4}] run data modify storage tryashtar.shulker_preview:data tooltip append value '{"translate":"tryashtar.shulker_preview.empty_slot"}'

data modify storage tryashtar.shulker_preview:data item set from storage tryashtar.shulker_preview:data contents[{slot:5}].item
execute if data storage tryashtar.shulker_preview:data contents[{slot:5}] as 7368756c-6b65-7220-7072-657669657721 run function tryashtar.shulker_preview:row_0/process_item
execute unless data storage tryashtar.shulker_preview:data contents[{slot:5}] run data modify storage tryashtar.shulker_preview:data tooltip append value '{"translate":"tryashtar.shulker_preview.empty_slot"}'

data modify storage tryashtar.shulker_preview:data item set from storage tryashtar.shulker_preview:data contents[{slot:6}].item
execute if data storage tryashtar.shulker_preview:data contents[{slot:6}] as 7368756c-6b65-7220-7072-657669657721 run function tryashtar.shulker_preview:row_0/process_item
execute unless data storage tryashtar.shulker_preview:data contents[{slot:6}] run data modify storage tryashtar.shulker_preview:data tooltip append value '{"translate":"tryashtar.shulker_preview.empty_slot"}'

data modify storage tryashtar.shulker_preview:data item set from storage tryashtar.shulker_preview:data contents[{slot:7}].item
execute if data storage tryashtar.shulker_preview:data contents[{slot:7}] as 7368756c-6b65-7220-7072-657669657721 run function tryashtar.shulker_preview:row_0/process_item
execute unless data storage tryashtar.shulker_preview:data contents[{slot:7}] run data modify storage tryashtar.shulker_preview:data tooltip append value '{"translate":"tryashtar.shulker_preview.empty_slot"}'

data modify storage tryashtar.shulker_preview:data item set from storage tryashtar.shulker_preview:data contents[{slot:8}].item
execute if data storage tryashtar.shulker_preview:data contents[{slot:8}] as 7368756c-6b65-7220-7072-657669657721 run function tryashtar.shulker_preview:row_0/process_item
execute unless data storage tryashtar.shulker_preview:data contents[{slot:8}] run data modify storage tryashtar.shulker_preview:data tooltip append value '{"translate":"tryashtar.shulker_preview.empty_slot"}'

data modify storage tryashtar.shulker_preview:data tooltip append value '{"translate":"tryashtar.shulker_preview.row_end"}'

data modify storage tryashtar.shulker_preview:data item set from storage tryashtar.shulker_preview:data contents[{slot:9}].item
execute if data storage tryashtar.shulker_preview:data contents[{slot:9}] as 7368756c-6b65-7220-7072-657669657721 run function tryashtar.shulker_preview:row_1/process_item
execute unless data storage tryashtar.shulker_preview:data contents[{slot:9}] run data modify storage tryashtar.shulker_preview:data tooltip append value '{"translate":"tryashtar.shulker_preview.empty_slot"}'

data modify storage tryashtar.shulker_preview:data item set from storage tryashtar.shulker_preview:data contents[{slot:10}].item
execute if data storage tryashtar.shulker_preview:data contents[{slot:10}] as 7368756c-6b65-7220-7072-657669657721 run function tryashtar.shulker_preview:row_1/process_item
execute unless data storage tryashtar.shulker_preview:data contents[{slot:10}] run data modify storage tryashtar.shulker_preview:data tooltip append value '{"translate":"tryashtar.shulker_preview.empty_slot"}'

data modify storage tryashtar.shulker_preview:data item set from storage tryashtar.shulker_preview:data contents[{slot:11}].item
execute if data storage tryashtar.shulker_preview:data contents[{slot:11}] as 7368756c-6b65-7220-7072-657669657721 run function tryashtar.shulker_preview:row_1/process_item
execute unless data storage tryashtar.shulker_preview:data contents[{slot:11}] run data modify storage tryashtar.shulker_preview:data tooltip append value '{"translate":"tryashtar.shulker_preview.empty_slot"}'

data modify storage tryashtar.shulker_preview:data item set from storage tryashtar.shulker_preview:data contents[{slot:12}].item
execute if data storage tryashtar.shulker_preview:data contents[{slot:12}] as 7368756c-6b65-7220-7072-657669657721 run function tryashtar.shulker_preview:row_1/process_item
execute unless data storage tryashtar.shulker_preview:data contents[{slot:12}] run data modify storage tryashtar.shulker_preview:data tooltip append value '{"translate":"tryashtar.shulker_preview.empty_slot"}'

data modify storage tryashtar.shulker_preview:data item set from storage tryashtar.shulker_preview:data contents[{slot:13}].item
execute if data storage tryashtar.shulker_preview:data contents[{slot:13}] as 7368756c-6b65-7220-7072-657669657721 run function tryashtar.shulker_preview:row_1/process_item
execute unless data storage tryashtar.shulker_preview:data contents[{slot:13}] run data modify storage tryashtar.shulker_preview:data tooltip append value '{"translate":"tryashtar.shulker_preview.empty_slot"}'

data modify storage tryashtar.shulker_preview:data item set from storage tryashtar.shulker_preview:data contents[{slot:14}].item
execute if data storage tryashtar.shulker_preview:data contents[{slot:14}] as 7368756c-6b65-7220-7072-657669657721 run function tryashtar.shulker_preview:row_1/process_item
execute unless data storage tryashtar.shulker_preview:data contents[{slot:14}] run data modify storage tryashtar.shulker_preview:data tooltip append value '{"translate":"tryashtar.shulker_preview.empty_slot"}'

data modify storage tryashtar.shulker_preview:data item set from storage tryashtar.shulker_preview:data contents[{slot:15}].item
execute if data storage tryashtar.shulker_preview:data contents[{slot:15}] as 7368756c-6b65-7220-7072-657669657721 run function tryashtar.shulker_preview:row_1/process_item
execute unless data storage tryashtar.shulker_preview:data contents[{slot:15}] run data modify storage tryashtar.shulker_preview:data tooltip append value '{"translate":"tryashtar.shulker_preview.empty_slot"}'

data modify storage tryashtar.shulker_preview:data item set from storage tryashtar.shulker_preview:data contents[{slot:16}].item
execute if data storage tryashtar.shulker_preview:data contents[{slot:16}] as 7368756c-6b65-7220-7072-657669657721 run function tryashtar.shulker_preview:row_1/process_item
execute unless data storage tryashtar.shulker_preview:data contents[{slot:16}] run data modify storage tryashtar.shulker_preview:data tooltip append value '{"translate":"tryashtar.shulker_preview.empty_slot"}'

data modify storage tryashtar.shulker_preview:data item set from storage tryashtar.shulker_preview:data contents[{slot:17}].item
execute if data storage tryashtar.shulker_preview:data contents[{slot:17}] as 7368756c-6b65-7220-7072-657669657721 run function tryashtar.shulker_preview:row_1/process_item
execute unless data storage tryashtar.shulker_preview:data contents[{slot:17}] run data modify storage tryashtar.shulker_preview:data tooltip append value '{"translate":"tryashtar.shulker_preview.empty_slot"}'

data modify storage tryashtar.shulker_preview:data tooltip append value '{"translate":"tryashtar.shulker_preview.row_end"}'

data modify storage tryashtar.shulker_preview:data item set from storage tryashtar.shulker_preview:data contents[{slot:18}].item
execute if data storage tryashtar.shulker_preview:data contents[{slot:18}] as 7368756c-6b65-7220-7072-657669657721 run function tryashtar.shulker_preview:row_2/process_item
execute unless data storage tryashtar.shulker_preview:data contents[{slot:18}] run data modify storage tryashtar.shulker_preview:data tooltip append value '{"translate":"tryashtar.shulker_preview.empty_slot"}'

data modify storage tryashtar.shulker_preview:data item set from storage tryashtar.shulker_preview:data contents[{slot:19}].item
execute if data storage tryashtar.shulker_preview:data contents[{slot:19}] as 7368756c-6b65-7220-7072-657669657721 run function tryashtar.shulker_preview:row_2/process_item
execute unless data storage tryashtar.shulker_preview:data contents[{slot:19}] run data modify storage tryashtar.shulker_preview:data tooltip append value '{"translate":"tryashtar.shulker_preview.empty_slot"}'

data modify storage tryashtar.shulker_preview:data item set from storage tryashtar.shulker_preview:data contents[{slot:20}].item
execute if data storage tryashtar.shulker_preview:data contents[{slot:20}] as 7368756c-6b65-7220-7072-657669657721 run function tryashtar.shulker_preview:row_2/process_item
execute unless data storage tryashtar.shulker_preview:data contents[{slot:20}] run data modify storage tryashtar.shulker_preview:data tooltip append value '{"translate":"tryashtar.shulker_preview.empty_slot"}'

data modify storage tryashtar.shulker_preview:data item set from storage tryashtar.shulker_preview:data contents[{slot:21}].item
execute if data storage tryashtar.shulker_preview:data contents[{slot:21}] as 7368756c-6b65-7220-7072-657669657721 run function tryashtar.shulker_preview:row_2/process_item
execute unless data storage tryashtar.shulker_preview:data contents[{slot:21}] run data modify storage tryashtar.shulker_preview:data tooltip append value '{"translate":"tryashtar.shulker_preview.empty_slot"}'

data modify storage tryashtar.shulker_preview:data item set from storage tryashtar.shulker_preview:data contents[{slot:22}].item
execute if data storage tryashtar.shulker_preview:data contents[{slot:22}] as 7368756c-6b65-7220-7072-657669657721 run function tryashtar.shulker_preview:row_2/process_item
execute unless data storage tryashtar.shulker_preview:data contents[{slot:22}] run data modify storage tryashtar.shulker_preview:data tooltip append value '{"translate":"tryashtar.shulker_preview.empty_slot"}'

data modify storage tryashtar.shulker_preview:data item set from storage tryashtar.shulker_preview:data contents[{slot:23}].item
execute if data storage tryashtar.shulker_preview:data contents[{slot:23}] as 7368756c-6b65-7220-7072-657669657721 run function tryashtar.shulker_preview:row_2/process_item
execute unless data storage tryashtar.shulker_preview:data contents[{slot:23}] run data modify storage tryashtar.shulker_preview:data tooltip append value '{"translate":"tryashtar.shulker_preview.empty_slot"}'

data modify storage tryashtar.shulker_preview:data item set from storage tryashtar.shulker_preview:data contents[{slot:24}].item
execute if data storage tryashtar.shulker_preview:data contents[{slot:24}] as 7368756c-6b65-7220-7072-657669657721 run function tryashtar.shulker_preview:row_2/process_item
execute unless data storage tryashtar.shulker_preview:data contents[{slot:24}] run data modify storage tryashtar.shulker_preview:data tooltip append value '{"translate":"tryashtar.shulker_preview.empty_slot"}'

data modify storage tryashtar.shulker_preview:data item set from storage tryashtar.shulker_preview:data contents[{slot:25}].item
execute if data storage tryashtar.shulker_preview:data contents[{slot:25}] as 7368756c-6b65-7220-7072-657669657721 run function tryashtar.shulker_preview:row_2/process_item
execute unless data storage tryashtar.shulker_preview:data contents[{slot:25}] run data modify storage tryashtar.shulker_preview:data tooltip append value '{"translate":"tryashtar.shulker_preview.empty_slot"}'

data modify storage tryashtar.shulker_preview:data item set from storage tryashtar.shulker_preview:data contents[{slot:26}].item
execute if data storage tryashtar.shulker_preview:data contents[{slot:26}] as 7368756c-6b65-7220-7072-657669657721 run function tryashtar.shulker_preview:row_2/process_item
execute unless data storage tryashtar.shulker_preview:data contents[{slot:26}] run data modify storage tryashtar.shulker_preview:data tooltip append value '{"translate":"tryashtar.shulker_preview.empty_slot"}'

# don't process any more items this tick
scoreboard players set #ready shulker_preview 0
kill 7368756c-6b65-7220-7072-657669657721
