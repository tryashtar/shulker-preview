# move items one by one to the global jukebox and process them
summon area_effect_cloud ~ ~3 ~ {Tags:["shulker_item"],CustomName:"{\"translate\":\"shulker_item.background\"}"}
data modify block ~2 ~ ~ RecordItem set from block ~1 ~ ~ Items[{Slot:0b}]
execute if data block ~1 ~ ~ Items[{Slot:0b}] positioned ~ ~4 ~ run function shulker_item:row_0/process_item
execute unless data block ~1 ~ ~ Items[{Slot:0b}] run summon area_effect_cloud ~ ~4 ~ {Tags:["shulker_item"],CustomName:"{\"translate\":\"shulker_item.empty_slot\"}"}
data modify block ~2 ~ ~ RecordItem set from block ~1 ~ ~ Items[{Slot:1b}]
execute if data block ~1 ~ ~ Items[{Slot:1b}] positioned ~ ~5 ~ run function shulker_item:row_0/process_item
execute unless data block ~1 ~ ~ Items[{Slot:1b}] run summon area_effect_cloud ~ ~5 ~ {Tags:["shulker_item"],CustomName:"{\"translate\":\"shulker_item.empty_slot\"}"}
data modify block ~2 ~ ~ RecordItem set from block ~1 ~ ~ Items[{Slot:2b}]
execute if data block ~1 ~ ~ Items[{Slot:2b}] positioned ~ ~6 ~ run function shulker_item:row_0/process_item
execute unless data block ~1 ~ ~ Items[{Slot:2b}] run summon area_effect_cloud ~ ~6 ~ {Tags:["shulker_item"],CustomName:"{\"translate\":\"shulker_item.empty_slot\"}"}
data modify block ~2 ~ ~ RecordItem set from block ~1 ~ ~ Items[{Slot:3b}]
execute if data block ~1 ~ ~ Items[{Slot:3b}] positioned ~ ~7 ~ run function shulker_item:row_0/process_item
execute unless data block ~1 ~ ~ Items[{Slot:3b}] run summon area_effect_cloud ~ ~7 ~ {Tags:["shulker_item"],CustomName:"{\"translate\":\"shulker_item.empty_slot\"}"}
data modify block ~2 ~ ~ RecordItem set from block ~1 ~ ~ Items[{Slot:4b}]
execute if data block ~1 ~ ~ Items[{Slot:4b}] positioned ~ ~8 ~ run function shulker_item:row_0/process_item
execute unless data block ~1 ~ ~ Items[{Slot:4b}] run summon area_effect_cloud ~ ~8 ~ {Tags:["shulker_item"],CustomName:"{\"translate\":\"shulker_item.empty_slot\"}"}
data modify block ~2 ~ ~ RecordItem set from block ~1 ~ ~ Items[{Slot:5b}]
execute if data block ~1 ~ ~ Items[{Slot:5b}] positioned ~ ~9 ~ run function shulker_item:row_0/process_item
execute unless data block ~1 ~ ~ Items[{Slot:5b}] run summon area_effect_cloud ~ ~9 ~ {Tags:["shulker_item"],CustomName:"{\"translate\":\"shulker_item.empty_slot\"}"}
data modify block ~2 ~ ~ RecordItem set from block ~1 ~ ~ Items[{Slot:6b}]
execute if data block ~1 ~ ~ Items[{Slot:6b}] positioned ~ ~10 ~ run function shulker_item:row_0/process_item
execute unless data block ~1 ~ ~ Items[{Slot:6b}] run summon area_effect_cloud ~ ~10 ~ {Tags:["shulker_item"],CustomName:"{\"translate\":\"shulker_item.empty_slot\"}"}
data modify block ~2 ~ ~ RecordItem set from block ~1 ~ ~ Items[{Slot:7b}]
execute if data block ~1 ~ ~ Items[{Slot:7b}] positioned ~ ~11 ~ run function shulker_item:row_0/process_item
execute unless data block ~1 ~ ~ Items[{Slot:7b}] run summon area_effect_cloud ~ ~11 ~ {Tags:["shulker_item"],CustomName:"{\"translate\":\"shulker_item.empty_slot\"}"}
data modify block ~2 ~ ~ RecordItem set from block ~1 ~ ~ Items[{Slot:8b}]
execute if data block ~1 ~ ~ Items[{Slot:8b}] positioned ~ ~12 ~ run function shulker_item:row_0/process_item
execute unless data block ~1 ~ ~ Items[{Slot:8b}] run summon area_effect_cloud ~ ~12 ~ {Tags:["shulker_item"],CustomName:"{\"translate\":\"shulker_item.empty_slot\"}"}
data modify block ~2 ~ ~ RecordItem set from block ~1 ~ ~ Items[{Slot:9b}]
execute if data block ~1 ~ ~ Items[{Slot:9b}] positioned ~ ~13 ~ run function shulker_item:row_1/process_item
execute unless data block ~1 ~ ~ Items[{Slot:9b}] run summon area_effect_cloud ~ ~13 ~ {Tags:["shulker_item"],CustomName:"{\"translate\":\"shulker_item.empty_slot\"}"}
data modify block ~2 ~ ~ RecordItem set from block ~1 ~ ~ Items[{Slot:10b}]
execute if data block ~1 ~ ~ Items[{Slot:10b}] positioned ~ ~14 ~ run function shulker_item:row_1/process_item
execute unless data block ~1 ~ ~ Items[{Slot:10b}] run summon area_effect_cloud ~ ~14 ~ {Tags:["shulker_item"],CustomName:"{\"translate\":\"shulker_item.empty_slot\"}"}
data modify block ~2 ~ ~ RecordItem set from block ~1 ~ ~ Items[{Slot:11b}]
execute if data block ~1 ~ ~ Items[{Slot:11b}] positioned ~ ~15 ~ run function shulker_item:row_1/process_item
execute unless data block ~1 ~ ~ Items[{Slot:11b}] run summon area_effect_cloud ~ ~15 ~ {Tags:["shulker_item"],CustomName:"{\"translate\":\"shulker_item.empty_slot\"}"}
data modify block ~2 ~ ~ RecordItem set from block ~1 ~ ~ Items[{Slot:12b}]
execute if data block ~1 ~ ~ Items[{Slot:12b}] positioned ~ ~16 ~ run function shulker_item:row_1/process_item
execute unless data block ~1 ~ ~ Items[{Slot:12b}] run summon area_effect_cloud ~ ~16 ~ {Tags:["shulker_item"],CustomName:"{\"translate\":\"shulker_item.empty_slot\"}"}
data modify block ~2 ~ ~ RecordItem set from block ~1 ~ ~ Items[{Slot:13b}]
execute if data block ~1 ~ ~ Items[{Slot:13b}] positioned ~ ~17 ~ run function shulker_item:row_1/process_item
execute unless data block ~1 ~ ~ Items[{Slot:13b}] run summon area_effect_cloud ~ ~17 ~ {Tags:["shulker_item"],CustomName:"{\"translate\":\"shulker_item.empty_slot\"}"}
data modify block ~2 ~ ~ RecordItem set from block ~1 ~ ~ Items[{Slot:14b}]
execute if data block ~1 ~ ~ Items[{Slot:14b}] positioned ~ ~18 ~ run function shulker_item:row_1/process_item
execute unless data block ~1 ~ ~ Items[{Slot:14b}] run summon area_effect_cloud ~ ~18 ~ {Tags:["shulker_item"],CustomName:"{\"translate\":\"shulker_item.empty_slot\"}"}
data modify block ~2 ~ ~ RecordItem set from block ~1 ~ ~ Items[{Slot:15b}]
execute if data block ~1 ~ ~ Items[{Slot:15b}] positioned ~ ~19 ~ run function shulker_item:row_1/process_item
execute unless data block ~1 ~ ~ Items[{Slot:15b}] run summon area_effect_cloud ~ ~19 ~ {Tags:["shulker_item"],CustomName:"{\"translate\":\"shulker_item.empty_slot\"}"}
data modify block ~2 ~ ~ RecordItem set from block ~1 ~ ~ Items[{Slot:16b}]
execute if data block ~1 ~ ~ Items[{Slot:16b}] positioned ~ ~20 ~ run function shulker_item:row_1/process_item
execute unless data block ~1 ~ ~ Items[{Slot:16b}] run summon area_effect_cloud ~ ~20 ~ {Tags:["shulker_item"],CustomName:"{\"translate\":\"shulker_item.empty_slot\"}"}
data modify block ~2 ~ ~ RecordItem set from block ~1 ~ ~ Items[{Slot:17b}]
execute if data block ~1 ~ ~ Items[{Slot:17b}] positioned ~ ~21 ~ run function shulker_item:row_1/process_item
execute unless data block ~1 ~ ~ Items[{Slot:17b}] run summon area_effect_cloud ~ ~21 ~ {Tags:["shulker_item"],CustomName:"{\"translate\":\"shulker_item.empty_slot\"}"}
data modify block ~2 ~ ~ RecordItem set from block ~1 ~ ~ Items[{Slot:18b}]
execute if data block ~1 ~ ~ Items[{Slot:18b}] positioned ~ ~22 ~ run function shulker_item:row_2/process_item
execute unless data block ~1 ~ ~ Items[{Slot:18b}] run summon area_effect_cloud ~ ~22 ~ {Tags:["shulker_item"],CustomName:"{\"translate\":\"shulker_item.empty_slot\"}"}
data modify block ~2 ~ ~ RecordItem set from block ~1 ~ ~ Items[{Slot:19b}]
execute if data block ~1 ~ ~ Items[{Slot:19b}] positioned ~ ~23 ~ run function shulker_item:row_2/process_item
execute unless data block ~1 ~ ~ Items[{Slot:19b}] run summon area_effect_cloud ~ ~23 ~ {Tags:["shulker_item"],CustomName:"{\"translate\":\"shulker_item.empty_slot\"}"}
data modify block ~2 ~ ~ RecordItem set from block ~1 ~ ~ Items[{Slot:20b}]
execute if data block ~1 ~ ~ Items[{Slot:20b}] positioned ~ ~24 ~ run function shulker_item:row_2/process_item
execute unless data block ~1 ~ ~ Items[{Slot:20b}] run summon area_effect_cloud ~ ~24 ~ {Tags:["shulker_item"],CustomName:"{\"translate\":\"shulker_item.empty_slot\"}"}
data modify block ~2 ~ ~ RecordItem set from block ~1 ~ ~ Items[{Slot:21b}]
execute if data block ~1 ~ ~ Items[{Slot:21b}] positioned ~ ~25 ~ run function shulker_item:row_2/process_item
execute unless data block ~1 ~ ~ Items[{Slot:21b}] run summon area_effect_cloud ~ ~25 ~ {Tags:["shulker_item"],CustomName:"{\"translate\":\"shulker_item.empty_slot\"}"}
data modify block ~2 ~ ~ RecordItem set from block ~1 ~ ~ Items[{Slot:22b}]
execute if data block ~1 ~ ~ Items[{Slot:22b}] positioned ~ ~26 ~ run function shulker_item:row_2/process_item
execute unless data block ~1 ~ ~ Items[{Slot:22b}] run summon area_effect_cloud ~ ~26 ~ {Tags:["shulker_item"],CustomName:"{\"translate\":\"shulker_item.empty_slot\"}"}
data modify block ~2 ~ ~ RecordItem set from block ~1 ~ ~ Items[{Slot:23b}]
execute if data block ~1 ~ ~ Items[{Slot:23b}] positioned ~ ~27 ~ run function shulker_item:row_2/process_item
execute unless data block ~1 ~ ~ Items[{Slot:23b}] run summon area_effect_cloud ~ ~27 ~ {Tags:["shulker_item"],CustomName:"{\"translate\":\"shulker_item.empty_slot\"}"}
data modify block ~2 ~ ~ RecordItem set from block ~1 ~ ~ Items[{Slot:24b}]
execute if data block ~1 ~ ~ Items[{Slot:24b}] positioned ~ ~28 ~ run function shulker_item:row_2/process_item
execute unless data block ~1 ~ ~ Items[{Slot:24b}] run summon area_effect_cloud ~ ~28 ~ {Tags:["shulker_item"],CustomName:"{\"translate\":\"shulker_item.empty_slot\"}"}
data modify block ~2 ~ ~ RecordItem set from block ~1 ~ ~ Items[{Slot:25b}]
execute if data block ~1 ~ ~ Items[{Slot:25b}] positioned ~ ~29 ~ run function shulker_item:row_2/process_item
execute unless data block ~1 ~ ~ Items[{Slot:25b}] run summon area_effect_cloud ~ ~29 ~ {Tags:["shulker_item"],CustomName:"{\"translate\":\"shulker_item.empty_slot\"}"}
data modify block ~2 ~ ~ RecordItem set from block ~1 ~ ~ Items[{Slot:26b}]
execute if data block ~1 ~ ~ Items[{Slot:26b}] positioned ~ ~30 ~ run function shulker_item:row_2/process_item
execute unless data block ~1 ~ ~ Items[{Slot:26b}] run summon area_effect_cloud ~ ~30 ~ {Tags:["shulker_item"],CustomName:"{\"translate\":\"shulker_item.empty_slot\"}"}
summon area_effect_cloud ~ ~12.2 ~ {Tags:["shulker_item"],CustomName:"{\"translate\":\"shulker_item.row_end\"}"}
summon area_effect_cloud ~ ~21.2 ~ {Tags:["shulker_item"],CustomName:"{\"translate\":\"shulker_item.row_end\"}"}
summon area_effect_cloud ~ ~30.2 ~ {Tags:["shulker_item"],CustomName:"{\"translate\":\"shulker_item.row_end\"}"}

# evaluate entities on the sign
data merge block ~3 ~ ~ {Text1:"[\"\\uF800\",{\"selector\":\"@e[type=area_effect_cloud,tag=shulker_item,sort=nearest]\",\"color\":\"white\",\"italic\":false}]"}
kill @e[type=area_effect_cloud,tag=shulker_item]
