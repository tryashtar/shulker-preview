# scan all the item slots in the sub-global shulker box
summon area_effect_cloud ~ ~3 ~ {Tags:["shulker_item"],CustomName:"{\"translate\":\"shulker_item.background\"}"}
execute if data block ~1 ~ ~ Items[{Slot:0b}] run function shulker_item:process_slot/0
execute unless data block ~1 ~ ~ Items[{Slot:0b}] run summon area_effect_cloud ~ ~4 ~ {Tags:["shulker_item"],CustomName:"{\"translate\":\"shulker_item.empty_slot\"}"}
execute if data block ~1 ~ ~ Items[{Slot:1b}] run function shulker_item:process_slot/1
execute unless data block ~1 ~ ~ Items[{Slot:1b}] run summon area_effect_cloud ~ ~5 ~ {Tags:["shulker_item"],CustomName:"{\"translate\":\"shulker_item.empty_slot\"}"}
execute if data block ~1 ~ ~ Items[{Slot:2b}] run function shulker_item:process_slot/2
execute unless data block ~1 ~ ~ Items[{Slot:2b}] run summon area_effect_cloud ~ ~6 ~ {Tags:["shulker_item"],CustomName:"{\"translate\":\"shulker_item.empty_slot\"}"}
execute if data block ~1 ~ ~ Items[{Slot:3b}] run function shulker_item:process_slot/3
execute unless data block ~1 ~ ~ Items[{Slot:3b}] run summon area_effect_cloud ~ ~7 ~ {Tags:["shulker_item"],CustomName:"{\"translate\":\"shulker_item.empty_slot\"}"}
execute if data block ~1 ~ ~ Items[{Slot:4b}] run function shulker_item:process_slot/4
execute unless data block ~1 ~ ~ Items[{Slot:4b}] run summon area_effect_cloud ~ ~8 ~ {Tags:["shulker_item"],CustomName:"{\"translate\":\"shulker_item.empty_slot\"}"}
execute if data block ~1 ~ ~ Items[{Slot:5b}] run function shulker_item:process_slot/5
execute unless data block ~1 ~ ~ Items[{Slot:5b}] run summon area_effect_cloud ~ ~9 ~ {Tags:["shulker_item"],CustomName:"{\"translate\":\"shulker_item.empty_slot\"}"}
execute if data block ~1 ~ ~ Items[{Slot:6b}] run function shulker_item:process_slot/6
execute unless data block ~1 ~ ~ Items[{Slot:6b}] run summon area_effect_cloud ~ ~10 ~ {Tags:["shulker_item"],CustomName:"{\"translate\":\"shulker_item.empty_slot\"}"}
execute if data block ~1 ~ ~ Items[{Slot:7b}] run function shulker_item:process_slot/7
execute unless data block ~1 ~ ~ Items[{Slot:7b}] run summon area_effect_cloud ~ ~11 ~ {Tags:["shulker_item"],CustomName:"{\"translate\":\"shulker_item.empty_slot\"}"}
execute if data block ~1 ~ ~ Items[{Slot:8b}] run function shulker_item:process_slot/8
execute unless data block ~1 ~ ~ Items[{Slot:8b}] run summon area_effect_cloud ~ ~12 ~ {Tags:["shulker_item"],CustomName:"{\"translate\":\"shulker_item.empty_slot\"}"}
summon area_effect_cloud ~ ~12.2 ~ {Tags:["shulker_item"],CustomName:"{\"translate\":\"shulker_item.row_end\"}"}
execute if data block ~1 ~ ~ Items[{Slot:9b}] run function shulker_item:process_slot/9
execute unless data block ~1 ~ ~ Items[{Slot:9b}] run summon area_effect_cloud ~ ~13 ~ {Tags:["shulker_item"],CustomName:"{\"translate\":\"shulker_item.empty_slot\"}"}
execute if data block ~1 ~ ~ Items[{Slot:10b}] run function shulker_item:process_slot/10
execute unless data block ~1 ~ ~ Items[{Slot:10b}] run summon area_effect_cloud ~ ~14 ~ {Tags:["shulker_item"],CustomName:"{\"translate\":\"shulker_item.empty_slot\"}"}
execute if data block ~1 ~ ~ Items[{Slot:11b}] run function shulker_item:process_slot/11
execute unless data block ~1 ~ ~ Items[{Slot:11b}] run summon area_effect_cloud ~ ~15 ~ {Tags:["shulker_item"],CustomName:"{\"translate\":\"shulker_item.empty_slot\"}"}
execute if data block ~1 ~ ~ Items[{Slot:12b}] run function shulker_item:process_slot/12
execute unless data block ~1 ~ ~ Items[{Slot:12b}] run summon area_effect_cloud ~ ~16 ~ {Tags:["shulker_item"],CustomName:"{\"translate\":\"shulker_item.empty_slot\"}"}
execute if data block ~1 ~ ~ Items[{Slot:13b}] run function shulker_item:process_slot/13
execute unless data block ~1 ~ ~ Items[{Slot:13b}] run summon area_effect_cloud ~ ~17 ~ {Tags:["shulker_item"],CustomName:"{\"translate\":\"shulker_item.empty_slot\"}"}
execute if data block ~1 ~ ~ Items[{Slot:14b}] run function shulker_item:process_slot/14
execute unless data block ~1 ~ ~ Items[{Slot:14b}] run summon area_effect_cloud ~ ~18 ~ {Tags:["shulker_item"],CustomName:"{\"translate\":\"shulker_item.empty_slot\"}"}
execute if data block ~1 ~ ~ Items[{Slot:15b}] run function shulker_item:process_slot/15
execute unless data block ~1 ~ ~ Items[{Slot:15b}] run summon area_effect_cloud ~ ~19 ~ {Tags:["shulker_item"],CustomName:"{\"translate\":\"shulker_item.empty_slot\"}"}
execute if data block ~1 ~ ~ Items[{Slot:16b}] run function shulker_item:process_slot/16
execute unless data block ~1 ~ ~ Items[{Slot:16b}] run summon area_effect_cloud ~ ~20 ~ {Tags:["shulker_item"],CustomName:"{\"translate\":\"shulker_item.empty_slot\"}"}
execute if data block ~1 ~ ~ Items[{Slot:17b}] run function shulker_item:process_slot/17
execute unless data block ~1 ~ ~ Items[{Slot:17b}] run summon area_effect_cloud ~ ~21 ~ {Tags:["shulker_item"],CustomName:"{\"translate\":\"shulker_item.empty_slot\"}"}
summon area_effect_cloud ~ ~21.2 ~ {Tags:["shulker_item"],CustomName:"{\"translate\":\"shulker_item.row_end\"}"}
execute if data block ~1 ~ ~ Items[{Slot:18b}] run function shulker_item:process_slot/18
execute unless data block ~1 ~ ~ Items[{Slot:18b}] run summon area_effect_cloud ~ ~22 ~ {Tags:["shulker_item"],CustomName:"{\"translate\":\"shulker_item.empty_slot\"}"}
execute if data block ~1 ~ ~ Items[{Slot:19b}] run function shulker_item:process_slot/19
execute unless data block ~1 ~ ~ Items[{Slot:19b}] run summon area_effect_cloud ~ ~23 ~ {Tags:["shulker_item"],CustomName:"{\"translate\":\"shulker_item.empty_slot\"}"}
execute if data block ~1 ~ ~ Items[{Slot:20b}] run function shulker_item:process_slot/20
execute unless data block ~1 ~ ~ Items[{Slot:20b}] run summon area_effect_cloud ~ ~24 ~ {Tags:["shulker_item"],CustomName:"{\"translate\":\"shulker_item.empty_slot\"}"}
execute if data block ~1 ~ ~ Items[{Slot:21b}] run function shulker_item:process_slot/21
execute unless data block ~1 ~ ~ Items[{Slot:21b}] run summon area_effect_cloud ~ ~25 ~ {Tags:["shulker_item"],CustomName:"{\"translate\":\"shulker_item.empty_slot\"}"}
execute if data block ~1 ~ ~ Items[{Slot:22b}] run function shulker_item:process_slot/22
execute unless data block ~1 ~ ~ Items[{Slot:22b}] run summon area_effect_cloud ~ ~26 ~ {Tags:["shulker_item"],CustomName:"{\"translate\":\"shulker_item.empty_slot\"}"}
execute if data block ~1 ~ ~ Items[{Slot:23b}] run function shulker_item:process_slot/23
execute unless data block ~1 ~ ~ Items[{Slot:23b}] run summon area_effect_cloud ~ ~27 ~ {Tags:["shulker_item"],CustomName:"{\"translate\":\"shulker_item.empty_slot\"}"}
execute if data block ~1 ~ ~ Items[{Slot:24b}] run function shulker_item:process_slot/24
execute unless data block ~1 ~ ~ Items[{Slot:24b}] run summon area_effect_cloud ~ ~28 ~ {Tags:["shulker_item"],CustomName:"{\"translate\":\"shulker_item.empty_slot\"}"}
execute if data block ~1 ~ ~ Items[{Slot:25b}] run function shulker_item:process_slot/25
execute unless data block ~1 ~ ~ Items[{Slot:25b}] run summon area_effect_cloud ~ ~29 ~ {Tags:["shulker_item"],CustomName:"{\"translate\":\"shulker_item.empty_slot\"}"}
execute if data block ~1 ~ ~ Items[{Slot:26b}] run function shulker_item:process_slot/26
execute unless data block ~1 ~ ~ Items[{Slot:26b}] run summon area_effect_cloud ~ ~30 ~ {Tags:["shulker_item"],CustomName:"{\"translate\":\"shulker_item.empty_slot\"}"}
summon area_effect_cloud ~ ~30.2 ~ {Tags:["shulker_item"],CustomName:"{\"translate\":\"shulker_item.row_end\"}"}

# create contents text by copying entity names to sign
data merge block ~2 ~ ~ {Text1:"[\"\\uF800\",{\"selector\":\"@e[type=area_effect_cloud,tag=shulker_item,sort=nearest]\",\"color\":\"white\",\"italic\":false}]"}
