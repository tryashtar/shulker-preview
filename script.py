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
   if file == "filled_map_markings.png":
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

def get_number_translation(number, row):
   digits = [int(d) for d in str(number)]
   if len(digits) == 1:
      return "\\uF807" +get_digit_char(digits[0],row)+ "\\uF806"
   return "\\uF808\\uF805" +get_digit_char(digits[0],row)+ "\\uF801" +get_digit_char(digits[1],row)+ "\\uF806"

def get_digit_char(digit, row):
   digit += 1
   digit += (row*10)
   return "\\uE" +format(digit,"03x").upper()

import os
import math
from PIL import Image
path = "D:\\Minecraft\\Java Storage\\Game History\\jar\\assets\\minecraft\\textures\\item"

# get all item PNGs from minecraft files
items = []
for file in os.listdir(path):
    if include(file):
      items.append(file)

# create spritesheet
size = 16*math.ceil(math.sqrt(len(items)))
itemgrid = []
itemrow = []
x = 0
y = 0
with Image.new("RGBA", (size, size-16)) as sheet:
   for item in items:
      with Image.open(os.path.join(path, item)).convert("RGBA") as sprite:
         pixels = sprite.load()
         r,g,b,a = pixels[0,0]
         a = max(a,1)
         pixels[0,0] = (r,g,b,a)
         r,g,b,a = pixels[15,15]
         a = max(a,1)
         pixels[15,15] = (r,g,b,a)
         sheet.paste(sprite, (x, y, x+16, y+16))
      x += 16
      itemrow.append(item)
      if x >= size:
         x = 0
         y += 16
         itemgrid.append(itemrow.copy())
         itemrow = []
   while len(itemrow) < len(itemgrid[0]):
      itemrow.append("")
   itemgrid.append(itemrow.copy())
   sheet.save("resourcepack\\assets\\shulker_item\\textures\\item_sheet.png", "PNG")

# create font characters for each
with open("resourcepack\\assets\\minecraft\\font\\default.json", "w") as file:
   num = 31
   file.write("{\"providers\":[{\"type\":\"ttf\",\"file\":\"shulker_item:negative_spaces.ttf\",\"shift\":[0.0,0.0],\"size\":10.0,\"oversample\":1.0},{\"type\":\"bitmap\",\"file\":\"shulker_item:tooltip.png\",\"ascent\":23,\"height\":78,\"chars\":[\"\\uE000\"]},{\"type\":\"bitmap\",\"file\":\"shulker_item:numbers.png\",\"ascent\":-4,\"height\":8,\"chars\":[\"\\uE001\\uE002\\uE003\\uE004\\uE005\\uE006\\uE007\\uE008\\uE009\\uE00A\"]},{\"type\":\"bitmap\",\"file\":\"shulker_item:numbers.png\",\"ascent\":-22,\"height\":8,\"chars\":[\"\\uE00B\\uE00C\\uE00D\\uE00E\\uE00F\\uE010\\uE011\\uE012\\uE013\\uE014\"]},{\"type\":\"bitmap\",\"file\":\"shulker_item:numbers.png\",\"ascent\":-40,\"height\":8,\"chars\":[\"\\uE015\\uE016\\uE017\\uE018\\uE019\\uE01A\\uE01B\\uE01C\\uE01D\\uE01E\"]},")
   for i in range(0, 3):
      ascent = 5-(18*i)
      file.write("{\"type\":\"bitmap\",\"file\":\"shulker_item:item_sheet.png\",\"ascent\":" +str(ascent)+ ",\"height\":16,\"chars\":[")
      last = len(itemgrid)
      current = 0
      for itemrow in itemgrid:
         current += 1
         file.write("\"")
         for item in itemrow:
            if item == "":
               file.write("\\u0000")
            else:
               file.write("\\uE" +format(num,"03x").upper())
               num += 1
         file.write("\"")
         if current < last:
            file.write(",")
      file.write("]}")
      if i<2:
         file.write(",")
   file.write("]}")

# create translations for each
with open("resourcepack\\assets\\minecraft\\lang\\en_us.json", "w") as file:
   num = 31
   file.write("{\"shulker_item.background\":\"\\uF820\\uF804\\uE000\\uF80C\\uF80A\\uF808\\uF801\\uF806\\uF800\",\"shulker_item.empty_slot\":\"\\uF820\\uF828\\uF824\\uF800\",\"shulker_item.row_end\":\"\\uF820\\uF80C\\uF80A\\uF806\\uF802\\uF800\",")
   for i in range(0, 3):
      for number in range(2, 65):
         file.write("\"shulker_item.number." +str(number)+ "." + str(i) + "\":\"\\uF820" +get_number_translation(number, i)+ "\\uF800\",")
      for item in items:
         file.write("\"shulker_item.item." +item_name(item)+ "." +str(i)+ "\":\"\\uF820\\uE" +format(num,"03x").upper()+ "\\uF805\\uF800\"")
         if i<2 or item != items[-1]:
            file.write(",")
         num += 1
   file.write("}")

# create tons of commands
with open("datapack\\data\\shulker_item\\functions\\process_box.mcfunction", "w") as file:
   file.write("summon area_effect_cloud ~ ~3 ~ {Tags:[\"shulker_item\"],CustomName:\"{\\\"translate\\\":\\\"shulker_item.background\\\"}\"}\n")
   for i in range(0, 27):
      row = i//9
      for item in items:
         file.write("execute if data block ~ ~1 ~ Items[{Slot:" +str(i)+ "b,id:\"minecraft:" +item_name(item)+ "\"}] run summon area_effect_cloud ~ ~" +str(i+4)+ " ~ {Tags:[\"shulker_item\"],CustomName:\"{\\\"translate\\\":\\\"shulker_item.item." +item_name(item)+ "." +str(row)+ "\\\"}\"}\n")
      file.write("execute unless data block ~ ~1 ~ Items[{Slot:" +str(i)+ "b}] run summon area_effect_cloud ~ ~" +str(i+4)+ " ~ {Tags:[\"shulker_item\"],CustomName:\"{\\\"translate\\\":\\\"shulker_item.empty_slot\\\"}\"}\nexecute store result score #count shulker_item run data get block ~ ~1 ~ Items[{Slot:" +str(i)+ "b}].Count\nexecute positioned ~ ~" +str(i+4.1)+ " ~ run function shulker_item:process_count_" +str(row)+ "\n")
      if (i+1)%9 == 0:
         file.write("summon area_effect_cloud ~ ~" +str(i+4.2)+ " ~ {Tags:[\"shulker_item\"],CustomName:\"{\\\"translate\\\":\\\"shulker_item.row_end\\\"}\"}\n")
   file.write("data merge block ~ ~2 ~ {Text1:\"[\\\"\\\\uF800\\\",{\\\"selector\\\":\\\"@e[type=area_effect_cloud,tag=shulker_item,sort=nearest]\\\",\\\"color\\\":\\\"white\\\",\\\"italic\\\":false}]\"}")

# copy status of process_box/0
with open("datapack\\data\\shulker_item\\functions\\process_box\\0.mcfunction", "r") as file:
   text = file.read()
   for i in range(1, 27):
      with open("datapack\\data\\shulker_item\\functions\\process_box\\" +str(i)+ ".mcfunction", "w") as file2:
         file2.write(text.replace("0", str(i)))
