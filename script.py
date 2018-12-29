def include(file):
   if not file.endswith(".png"):
      return False
   if file == "clock_00.png":
      return True
   if file.startswith("clock_"):
      return False
   if file == "compass_00.png":
      return True
   if file.startswith("compass_"):
      return False
   if file.startswith("bow_pulling_"):
      return False
   if file == "crossbow_standby.png":
      return True
   if file.startswith("crossbow_"):
      return False
   if file.startswith("empty_armor_slot"):
      return False
   if "overlay" in file:
      return False
   if file == "fishing_rod_cast.png":
      return False
   if file == "tipped_arrow_head.png":
      return False
   if file == "broken_elytra.png":
      return False
   if file == "filled_map_markings":
      return False
   return True

def item_name(file):
   if file == "clock_00.png":
      return "clock"
   if file == "compass_00.png":
      return "compass"
   if file == "crossbow_standby.png":
      return "crossbow"
   return os.path.splitext(file)[0]

import os
path = "D:\\Minecraft\\Java Storage\\Game History\\jar\\assets\\minecraft\\textures\\item"

# get all item PNGs from minecraft files
items = []
for file in os.listdir(path):
    if include(file):
      items.append(file)

# create font characters for each
with open("resourcepack\\assets\\minecraft\\font\\default.json", "w") as file:
   num = 1
   file.write("{\"providers\":[{\"type\":\"ttf\",\"file\":\"shulker_item:negative_spaces.ttf\",\"shift\":[0.0,0.0],\"size\":10.0,\"oversample\":1.0},{\"type\":\"bitmap\",\"file\":\"shulker_item:tooltip.png\",\"ascent\":23,\"height\":78,\"chars\":[\"\\uE000\"]},")
   for item in items:
      for i in range(0, 3):
         file.write("{\"type\":\"bitmap\",\"file\":\"minecraft:item/" +item+ "\",\"ascent\":")
         ascent = 5-(18*i)
         file.write(str(ascent))
         file.write(",\"height\":16,\"chars\":[\"\\uE" +format(num,"03x").upper()+ "\"]}")
         if i<2 or item != items[-1]:
            file.write(",")
         num += 1
   file.write("]}")

# create translations for each
with open("resourcepack\\assets\\minecraft\\lang\\en_us.json", "w") as file:
   num = 1
   file.write("{\"shulker_item.background\":\"\\uF820\\uF804\\uE000\\uF80C\\uF80A\\uF808\\uF801\\uF806\\uF800\",\"shulker_item.empty_slot\":\"\\uF820\\uF828\\uF824\\uF800\",\"shulker_item.row_end\":\"\\uF820\\uF80C\\uF80A\\uF806\\uF802\\uF800\",")
   for item in items:
      for i in range(0, 3):
         file.write("\"shulker_item.item." +item_name(item)+ "." +str(i)+ "\":\"\\uF820\\uE" +format(num,"03x").upper()+ "\\uF805\\uF800\"")
         if i<2 or item != items[-1]:
            file.write(",")
         num += 1
   file.write("}")

# create tons of commands
with open("datapack\\data\\shulker_item\\functions\\process_box.mcfunction", "w") as file:
   file.write("summon area_effect_cloud ~ ~3 ~ {Tags:[\"shulker_item\"],CustomName:\"{\\\"translate\\\":\\\"shulker_item.background\\\"}\"}\n")
   for i in range(0, 27):
      for item in items:
         file.write("execute if data block ~ ~1 ~ Items[{Slot:" +str(i)+ "b,id:\"minecraft:" +item_name(item)+ "\"}] run summon area_effect_cloud ~ ~" +str(i+4)+ " ~ {Tags:[\"shulker_item\"],CustomName:\"{\\\"translate\\\":\\\"shulker_item.item." +item_name(item)+ "." +str(i//9)+ "\\\"}\"}\n")
      file.write("execute unless data block ~ ~1 ~ Items[{Slot:" +str(i)+ "b}] run summon area_effect_cloud ~ ~" +str(i+4)+ " ~ {Tags:[\"shulker_item\"],CustomName:\"{\\\"translate\\\":\\\"shulker_item.empty_slot\\\"}\"}\n")
      if (i+1)%9 == 0:
         file.write("summon area_effect_cloud ~ ~" +str(i+4.5)+ " ~ {Tags:[\"shulker_item\"],CustomName:\"{\\\"translate\\\":\\\"shulker_item.row_end\\\"}\"}\n")
   file.write("data merge block ~ ~2 ~ {Text1:\"[\\\"\\\\uF800\\\",{\\\"selector\\\":\\\"@e[type=area_effect_cloud,tag=shulker_item,sort=nearest]\\\",\\\"color\\\":\\\"white\\\",\\\"italic\\\":false}]\"}")
