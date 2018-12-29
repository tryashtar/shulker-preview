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
with open("D:\\Minecraft\\Game Directories\\.minecraft\\saves\\tryashtar's Command Land\\Shulker GIT\\resourcepack\\assets\\minecraft\\font\\default.json", "w") as file:
   num = 1
   file.write("{\"providers\":[{\"type\":\"ttf\",\"file\":\"shulker_item:negative_spaces.ttf\",\"shift\":[0.0,0.0],\"size\":10.0,\"oversample\":1.0},{\"type\":\"bitmap\",\"file\":\"shulker_item:tooltip.png\",\"ascent\":23,\"height\":78,\"chars\":[\"\\uE000\"]},")
   for item in items:
      file.write("{\"type\": \"bitmap\",\"file\": \"minecraft:item/" +item+ "\",\"ascent\": 5,\"height\": 16,\"chars\": [\"\\uE" +format(num,"03x").upper()+ "\"]}")
      if item != items[-1]:
         file.write(",")
      num += 1
   file.write("]}")

# create translations for each
with open("D:\\Minecraft\\Game Directories\\.minecraft\\saves\\tryashtar's Command Land\\Shulker GIT\\resourcepack\\assets\\minecraft\\lang\\en_us.json", "w") as file:
   num = 1
   file.write("{\"shulker_item.background\":\"\\uF820\\uF804\\uE000\\uF80C\\uF80A\\uF808\\uF801\\uF806\\uF800\",")
   for item in items:
      file.write("\"shulker_item.item." +item_name(item)+ "\":\"\\uF820\\uE" +format(num,"03x")+ "\\uF823\\uF806\\uF800\"")
      if item != items[-1]:
         file.write(",")
      num += 1
   file.write("}")