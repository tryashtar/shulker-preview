execute if block ~2 1 ~ jukebox{RecordItem:{id:"minecraft:barrier"}} run summon area_effect_cloud ~ ~ ~ {Tags:["shulker_item"],CustomName:"{\"translate\":\"shulker_item.item.barrier.2\"}"}
execute if block ~2 1 ~ jukebox{RecordItem:{id:"minecraft:chicken"}} run summon area_effect_cloud ~ ~ ~ {Tags:["shulker_item"],CustomName:"{\"translate\":\"shulker_item.item.chicken.2\"}"}
execute if block ~2 1 ~ jukebox{RecordItem:{id:"minecraft:compass"}} run summon area_effect_cloud ~ ~ ~ {Tags:["shulker_item"],CustomName:"{\"translate\":\"shulker_item.item.compass.2\"}"}
execute if block ~2 1 ~ jukebox{RecordItem:{id:"minecraft:diamond"}} run summon area_effect_cloud ~ ~ ~ {Tags:["shulker_item"],CustomName:"{\"translate\":\"shulker_item.item.diamond.2\"}"}
execute if block ~2 1 ~ jukebox{RecordItem:{id:"minecraft:emerald"}} run summon area_effect_cloud ~ ~ ~ {Tags:["shulker_item"],CustomName:"{\"translate\":\"shulker_item.item.emerald.2\"}"}
execute if block ~2 1 ~ jukebox{RecordItem:{id:"minecraft:feather"}} run summon area_effect_cloud ~ ~ ~ {Tags:["shulker_item"],CustomName:"{\"translate\":\"shulker_item.item.feather.2\"}"}
execute if block ~2 1 ~ jukebox{RecordItem:{id:"minecraft:ink_sac"}} run summon area_effect_cloud ~ ~ ~ {Tags:["shulker_item"],CustomName:"{\"translate\":\"shulker_item.item.ink_sac.2\"}"}
execute if block ~2 1 ~ jukebox{RecordItem:{id:"minecraft:lantern"}} run summon area_effect_cloud ~ ~ ~ {Tags:["shulker_item"],CustomName:"{\"translate\":\"shulker_item.item.lantern.2\"}"}
execute if block ~2 1 ~ jukebox{RecordItem:{id:"minecraft:leather"}} run summon area_effect_cloud ~ ~ ~ {Tags:["shulker_item"],CustomName:"{\"translate\":\"shulker_item.item.leather.2\"}"}
execute if block ~2 1 ~ jukebox{RecordItem:{id:"minecraft:red_dye"}} run summon area_effect_cloud ~ ~ ~ {Tags:["shulker_item"],CustomName:"{\"translate\":\"shulker_item.item.red_dye.2\"}"}
execute if block ~2 1 ~ jukebox{RecordItem:{id:"minecraft:trident"}} run summon area_effect_cloud ~ ~ ~ {Tags:["shulker_item"],CustomName:"{\"translate\":\"shulker_item.item.trident.2\"}"}
execute if block ~2 1 ~ jukebox{RecordItem:{id:"minecraft:trident"}} run scoreboard players set #max shulker_item 250
execute if block ~2 1 ~ jukebox{RecordItem:{id:"minecraft:bedrock"}} run summon area_effect_cloud ~ ~ ~ {Tags:["shulker_item"],CustomName:"{\"translate\":\"shulker_item.block.bedrock.2\"}"}
execute if block ~2 1 ~ jukebox{RecordItem:{id:"minecraft:conduit"}} run summon area_effect_cloud ~ ~ ~ {Tags:["shulker_item"],CustomName:"{\"translate\":\"shulker_item.block.conduit.2\"}"}
execute if block ~2 1 ~ jukebox{RecordItem:{id:"minecraft:diorite"}} run summon area_effect_cloud ~ ~ ~ {Tags:["shulker_item"],CustomName:"{\"translate\":\"shulker_item.block.diorite.2\"}"}
execute if block ~2 1 ~ jukebox{RecordItem:{id:"minecraft:dropper"}} run summon area_effect_cloud ~ ~ ~ {Tags:["shulker_item"],CustomName:"{\"translate\":\"shulker_item.block.dropper.2\"}"}
execute if block ~2 1 ~ jukebox{RecordItem:{id:"minecraft:end_rod"}} run summon area_effect_cloud ~ ~ ~ {Tags:["shulker_item"],CustomName:"{\"translate\":\"shulker_item.block.end_rod.2\"}"}
execute if block ~2 1 ~ jukebox{RecordItem:{id:"minecraft:furnace"}} run summon area_effect_cloud ~ ~ ~ {Tags:["shulker_item"],CustomName:"{\"translate\":\"shulker_item.block.furnace.2\"}"}
execute if block ~2 1 ~ jukebox{RecordItem:{id:"minecraft:granite"}} run summon area_effect_cloud ~ ~ ~ {Tags:["shulker_item"],CustomName:"{\"translate\":\"shulker_item.block.granite.2\"}"}
execute if block ~2 1 ~ jukebox{RecordItem:{id:"minecraft:jukebox"}} run summon area_effect_cloud ~ ~ ~ {Tags:["shulker_item"],CustomName:"{\"translate\":\"shulker_item.block.jukebox.2\"}"}
execute if block ~2 1 ~ jukebox{RecordItem:{id:"minecraft:lectern"}} run summon area_effect_cloud ~ ~ ~ {Tags:["shulker_item"],CustomName:"{\"translate\":\"shulker_item.block.lectern.2\"}"}
execute if block ~2 1 ~ jukebox{RecordItem:{id:"minecraft:oak_log"}} run summon area_effect_cloud ~ ~ ~ {Tags:["shulker_item"],CustomName:"{\"translate\":\"shulker_item.block.oak_log.2\"}"}
execute if block ~2 1 ~ jukebox{RecordItem:{id:"minecraft:pumpkin"}} run summon area_effect_cloud ~ ~ ~ {Tags:["shulker_item"],CustomName:"{\"translate\":\"shulker_item.block.pumpkin.2\"}"}
execute if block ~2 1 ~ jukebox{RecordItem:{id:"minecraft:red_bed"}} run summon area_effect_cloud ~ ~ ~ {Tags:["shulker_item"],CustomName:"{\"translate\":\"shulker_item.block.red_bed.2\"}"}
execute if block ~2 1 ~ jukebox{RecordItem:{id:"minecraft:spawner"}} run summon area_effect_cloud ~ ~ ~ {Tags:["shulker_item"],CustomName:"{\"translate\":\"shulker_item.block.spawner.2\"}"}
execute store result score #durability shulker_item run data get block ~2 1 ~ RecordItem.tag.Damage
execute if data block ~2 1 ~ RecordItem.tag.Damage run function shulker_item:row_2/process_durability