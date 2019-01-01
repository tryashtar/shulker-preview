execute if block ~2 1 ~ jukebox{RecordItem:{id:"minecraft:bow"}} run summon area_effect_cloud ~ ~ ~ {Tags:["shulker_item"],CustomName:"{\"translate\":\"shulker_item.item.bow.2\"}"}
execute if block ~2 1 ~ jukebox{RecordItem:{id:"minecraft:bow"}} run scoreboard players set #max shulker_item 384
execute if block ~2 1 ~ jukebox{RecordItem:{id:"minecraft:cod"}} run summon area_effect_cloud ~ ~ ~ {Tags:["shulker_item"],CustomName:"{\"translate\":\"shulker_item.item.cod.2\"}"}
execute if block ~2 1 ~ jukebox{RecordItem:{id:"minecraft:egg"}} run summon area_effect_cloud ~ ~ ~ {Tags:["shulker_item"],CustomName:"{\"translate\":\"shulker_item.item.egg.2\"}"}
execute if block ~2 1 ~ jukebox{RecordItem:{id:"minecraft:ice"}} run summon area_effect_cloud ~ ~ ~ {Tags:["shulker_item"],CustomName:"{\"translate\":\"shulker_item.block.ice.2\"}"}
execute if block ~2 1 ~ jukebox{RecordItem:{id:"minecraft:map"}} run summon area_effect_cloud ~ ~ ~ {Tags:["shulker_item"],CustomName:"{\"translate\":\"shulker_item.item.map.2\"}"}
execute if block ~2 1 ~ jukebox{RecordItem:{id:"minecraft:tnt"}} run summon area_effect_cloud ~ ~ ~ {Tags:["shulker_item"],CustomName:"{\"translate\":\"shulker_item.block.tnt.2\"}"}
execute store result score #durability shulker_item run data get block ~2 1 ~ RecordItem.tag.Damage
execute if data block ~2 1 ~ RecordItem.tag.Damage run function shulker_item:row_2/process_durability
