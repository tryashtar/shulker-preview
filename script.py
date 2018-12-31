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
   if file == "ruby.png":
      return False
   if file == "tipped_arrow_base.png":
      return False
   if file == "spawn_egg.png":
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

items_path = "D:\\Minecraft\\Java Storage\\Game History\\jar\\assets\\minecraft\\textures\\item"
items_path2 = "..\\extra item images"
blocks_path = "..\\block images"

def get_preferred_source(file):
   if file in os.listdir(items_path2):
      return os.path.join(items_path2, item)
   elif file in os.listdir(items_path):
      return os.path.join(items_path, item)

def get_number_translation(number, row):
   digits = [int(d) for d in str(number)]
   if len(digits) == 1:
      return "\\uF807" +get_digit_char(digits[0],row)+ "\\uF806"
   return "\\uF808\\uF805" +get_digit_char(digits[0],row)+ "\\uF801" +get_digit_char(digits[1],row)+ "\\uF806"

def get_durability_translation(durability, row):
   val = 31
   val += (row*14)
   val += durability
   return "\\uF808\\uF808\\uE" +format(val,"03x").upper()+ "\\uF804"

def get_digit_char(digit, row):
   digit += 1
   digit += (row*10)
   return "\\uE" +format(digit,"03x").upper()

import os
import math
from PIL import Image

# get all item PNGs from minecraft files
items = []
blocks = []
all_items = []
for file in os.listdir(items_path):
    if include(file):
      items.append(file)
      all_items.append(file)
for file in os.listdir(items_path2):
    if include(file) and file not in items:
      items.append(file)
      all_items.append(file)
for file in os.listdir(blocks_path):
    if include(file):
      blocks.append(file)
      all_items.append(file)

# create spritesheets
size = 16*math.ceil(math.sqrt(len(items)))
itemgrid = []
itemrow = []
x = 0
y = 0
with Image.new("RGBA", (size, size)) as sheet:
   for item in items:
      image_path = get_preferred_source(item)
      with Image.open(image_path).convert("RGBA") as sprite:
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

size = 64*math.ceil(math.sqrt(len(blocks)))
blockgrid = []
blockrow = []
x = 0
y = 0
with Image.new("RGBA", (size, size-64)) as sheet:
   for block in blocks:
      image_path = os.path.join(blocks_path, block)
      with Image.open(image_path).convert("RGBA") as sprite:
         pixels = sprite.load()
         r,g,b,a = pixels[0,0]
         a = max(a,1)
         pixels[0,0] = (r,g,b,a)
         r,g,b,a = pixels[63,63]
         a = max(a,1)
         pixels[63,63] = (r,g,b,a)
         sheet.paste(sprite, (x, y, x+64, y+64))
      x += 64
      blockrow.append(block)
      if x >= size:
         x = 0
         y += 64
         blockgrid.append(blockrow.copy())
         blockrow = []
   while len(blockrow) < len(blockgrid[0]):
      blockrow.append("")
   blockgrid.append(blockrow.copy())
   sheet.save("resourcepack\\assets\\shulker_item\\textures\\block_sheet.png", "PNG")

# create font characters for each
with open("resourcepack\\assets\\minecraft\\font\\default.json", "w") as file:
   num = 73
   file.write("{\"providers\":[{\"type\":\"ttf\",\"file\":\"shulker_item:negative_spaces.ttf\",\"shift\":[0.0,0.0],\"size\":10.0,\"oversample\":1.0},{\"type\":\"bitmap\",\"file\":\"shulker_item:tooltip.png\",\"ascent\":23,\"height\":78,\"chars\":[\"\\uE000\"]},{\"type\":\"bitmap\",\"file\":\"shulker_item:numbers.png\",\"ascent\":-4,\"height\":8,\"chars\":[\"\\uE001\\uE002\\uE003\\uE004\\uE005\\uE006\\uE007\\uE008\\uE009\\uE00A\"]},{\"type\":\"bitmap\",\"file\":\"shulker_item:numbers.png\",\"ascent\":-22,\"height\":8,\"chars\":[\"\\uE00B\\uE00C\\uE00D\\uE00E\\uE00F\\uE010\\uE011\\uE012\\uE013\\uE014\"]},{\"type\":\"bitmap\",\"file\":\"shulker_item:numbers.png\",\"ascent\":-40,\"height\":8,\"chars\":[\"\\uE015\\uE016\\uE017\\uE018\\uE019\\uE01A\\uE01B\\uE01C\\uE01D\\uE01E\"]},{\"type\":\"bitmap\",\"file\":\"shulker_item:durability.png\",\"ascent\":-8,\"height\":2,\"chars\":[\"\\uE01F\\uE020\\uE021\\uE022\\uE023\",\"\\uE024\\uE025\\uE026\\uE027\\uE028\",\"\\uE029\\uE02A\\uE02B\\uE02C\\uE000\"]},{\"type\":\"bitmap\",\"file\":\"shulker_item:durability.png\",\"ascent\":-26,\"height\":2,\"chars\":[\"\\uE02D\\uE02E\\uE02F\\uE030\\uE031\",\"\\uE032\\uE033\\uE034\\uE035\\uE036\",\"\\uE037\\uE038\\uE039\\uE03A\\uE000\"]},{\"type\":\"bitmap\",\"file\":\"shulker_item:durability.png\",\"ascent\":-44,\"height\":2,\"chars\":[\"\\uE03B\\uE03C\\uE03D\\uE03E\\uE03F\",\"\\uE040\\uE041\\uE042\\uE043\\uE044\",\"\\uE045\\uE046\\uE047\\uE048\\uE000\"]},")
   for i in range(0, 3):
      for thing in ["item", "block"]:
         grid = itemgrid
         if thing == "block":
            grid = blockgrid
         ascent = 5-(18*i)
         file.write("{\"type\":\"bitmap\",\"file\":\"shulker_item:" +thing+ "_sheet.png\",   \"ascent\":" +str(ascent)+ ",\"height\":16,\"chars\":[")
         last = len(grid)
         current = 0
         for row in grid:
            current += 1
            file.write("\"")
            for item in row:
               if item == "":
                  file.write("\\u0000")
               else:
                  file.write("\\uE" +format(num,"03x").upper())
                  num += 1
            file.write("\"")
            if current < last:
               file.write(",")
         file.write("]}")
         if i<2 or thing == "item":
            file.write(",")
   file.write("]}")

# create translations for each
with open("resourcepack\\assets\\minecraft\\lang\\en_us.json", "w") as file:
   num = 73
   file.write("{\"If you can see this, you still need to equip the resource pack!\":\"%s\",\"shulker_item.background\":\"\\uF820\\uF804\\uE000\\uF80C\\uF80A\\uF808\\uF801\\uF806\\uF800\",\"shulker_item.empty_slot\":\"\\uF820\\uF828\\uF824\\uF800\",\"shulker_item.row_end\":\"\\uF820\\uF80C\\uF80A\\uF806\\uF802\\uF800\",")
   for i in range(0, 3):
      for number in range(2, 65):
         file.write("\"shulker_item.number." +str(number)+ "." +str(i)+ "\":\"\\uF820" +get_number_translation(number, i)+ "\\uF800\",")
      for durability in range(0, 15):
         file.write("\"shulker_item.durability." +str(durability)+ "." +str(i)+ "\":\"\\uF820" +get_durability_translation(durability, i)+ "\\uF800\",")
      for item in items:
         file.write("\"shulker_item.item." +item_name(item)+ "." +str(i)+ "\":\"\\uF820\\uE" +format(num,"03x").upper()+ "\\uF805\\uF800\",")
         num += 1
      for block in blocks:
         file.write("\"shulker_item.block." +item_name(block)+ "." +str(i)+ "\":\"\\uF820\\uE" +format(num,"03x").upper()+ "\\uF805\\uF800\"")
         if i<2 or block != blocks[-1]:
            file.write(",")
         num += 1
   file.write("}")

# create tons of commands
durability_dict = {
   "minecraft:leather_helmet": 55,
   "minecraft:leather_chestplate": 80,
   "minecraft:leather_leggings": 75,
   "minecraft:leather_boots": 65,
   "minecraft:golden_helmet": 77,
   "minecraft:golden_chestplate": 112,
   "minecraft:golden_leggings": 105,
   "minecraft:golden_boots": 91,
   "minecraft:chainmail_helmet": 165,
   "minecraft:chainmail_chestplate": 240,
   "minecraft:chainmail_leggings": 225,
   "minecraft:chainmail_boots": 195,
   "minecraft:iron_helmet": 165,
   "minecraft:iron_chestplate": 240,
   "minecraft:iron_leggings": 225,
   "minecraft:iron_boots": 195,
   "minecraft:diamond_helmet": 363,
   "minecraft:diamond_chestplate": 528,
   "minecraft:diamond_leggings": 495,
   "minecraft:diamond_boots": 429,
   "minecraft:golden_axe": 32,
   "minecraft:golden_pickaxe": 32,
   "minecraft:golden_shovel": 32,
   "minecraft:golden_hoe": 32,
   "minecraft:golden_sword": 32,
   "minecraft:wooden_axe": 59,
   "minecraft:wooden_pickaxe": 59,
   "minecraft:wooden_shovel": 59,
   "minecraft:wooden_hoe": 59,
   "minecraft:wooden_sword": 59,
   "minecraft:stone_axe": 131,
   "minecraft:stone_pickaxe": 131,
   "minecraft:stone_shovel": 131,
   "minecraft:stone_hoe": 131,
   "minecraft:stone_sword": 131,
   "minecraft:iron_axe": 250,
   "minecraft:iron_pickaxe": 250,
   "minecraft:iron_shovel": 250,
   "minecraft:iron_hoe": 250,
   "minecraft:iron_sword": 250,
   "minecraft:diamond_axe": 1561,
   "minecraft:diamond_pickaxe": 1561,
   "minecraft:diamond_shovel": 1561,
   "minecraft:diamond_hoe": 1561,
   "minecraft:diamond_sword": 1561,
   "minecraft:fishing_rod": 64,
   "minecraft:flint_and_steel": 64,
   "minecraft:carrot_on_a_stick": 25,
   "minecraft:shears": 238,
   "minecraft:shield": 336,
   "minecraft:bow": 384,
   "minecraft:trident": 250,
   "minecraft:elytra": 432,
   "minecraft:crossbow": 326
}
with open("datapack\\data\\shulker_item\\functions\\process_box.mcfunction", "w") as file:
   file.write("# scan all the item slots in the sub-global shulker box\nsummon area_effect_cloud ~ ~3 ~ {Tags:[\"shulker_item\"],CustomName:\"{\\\"translate\\\":\\\"shulker_item.background\\\"}\"}\n")
   for i in range(0, 27):
      with open("datapack\\data\\shulker_item\\functions\\process_slot\\" +str(i)+ ".mcfunction", "w") as slotfile:
         row = i//9
         slotfile.write("# check which item is in slot " +str(i)+ " and summon the matching entity\n")
         for item in items:
            slotfile.write("execute if data block ~1 ~ ~ Items[{Slot:" +str(i)+ "b,id:\"minecraft:" +item_name(item)+ "\"}] run summon area_effect_cloud ~ ~" +str(i+4)+ " ~ {Tags:[\"shulker_item\"],CustomName:\"{\\\"translate\\\":\\\"shulker_item.item." +item_name(item)+ "." +str(row)+ "\\\"}\"}\n")
         for block in blocks:
            slotfile.write("execute if data block ~1 ~ ~ Items[{Slot:" +str(i)+ "b,id:\"minecraft:" +item_name(block)+ "\"}] run summon area_effect_cloud ~ ~" +str(i+4)+ " ~ {Tags:[\"shulker_item\"],CustomName:\"{\\\"translate\\\":\\\"shulker_item.block." +item_name(block)+ "." +str(row)+ "\\\"}\"}\n")
         slotfile.write("\n# summon an entity for the item count text\nexecute store result score #count shulker_item run data get block ~1 ~ ~ Items[{Slot:" +str(i)+ "b}].Count\nexecute if score #count shulker_item matches 2.. positioned ~ ~" +str(i+4.1)+ " ~ run function shulker_item:process_count_" +str(row)+ "\n")
         slotfile.write("\n# summon an entity for the item durability bar\n")
         for itemname, damage in durability_dict.items():
            slotfile.write("execute if data block ~1 ~ ~ Items[{Slot:" +str(i)+ "b,id:\"" +itemname+ "\"}] run scoreboard players set #max shulker_item " +str(damage)+ "\n")
         slotfile.write("execute store result score #durability shulker_item run data get block ~1 ~ ~ Items[{Slot:" +str(i)+ "b}].tag.Damage\nexecute if score #durability shulker_item matches 1.. positioned ~ ~" +str(i+4.2)+ " ~ run function shulker_item:process_durability_" +str(row)+ "\n")
      file.write("execute if data block ~1 ~ ~ Items[{Slot:" +str(i)+ "b}] run function shulker_item:process_slot/" +str(i)+ "\n")
      file.write("execute unless data block ~1 ~ ~ Items[{Slot:" +str(i)+ "b}] run summon area_effect_cloud ~ ~" +str(i+4)+ " ~ {Tags:[\"shulker_item\"],CustomName:\"{\\\"translate\\\":\\\"shulker_item.empty_slot\\\"}\"}\n")
      if (i+1)%9 == 0:
         file.write("summon area_effect_cloud ~ ~" +str(i+4.2)+ " ~ {Tags:[\"shulker_item\"],CustomName:\"{\\\"translate\\\":\\\"shulker_item.row_end\\\"}\"}\n")
   file.write("\n# create contents text by copying entity names to sign\ndata merge block ~2 ~ ~ {Text1:\"[\\\"\\\\uF800\\\",{\\\"selector\\\":\\\"@e[type=area_effect_cloud,tag=shulker_item,sort=nearest]\\\",\\\"color\\\":\\\"white\\\",\\\"italic\\\":false}]\"}\n")

# copy status of process_box/0
with open("datapack\\data\\shulker_item\\functions\\process_box\\0.mcfunction", "r") as file:
   text = file.read()
   for i in range(1, 27):
      with open("datapack\\data\\shulker_item\\functions\\process_box\\" +str(i)+ ".mcfunction", "w") as file2:
         file2.write(text.replace("0", str(i)))

# test all items!
import json
with open("D:\\Minecraft\\Java Storage\\Game History\\reports\\registries.json") as file:
   register = json.loads(file.read())
   mc_items = list(register["minecraft:item"]["entries"].keys())

   all_items2 = []
   for i in all_items:
      all_items2.append(item_name(i))
   mc_items2 = []
   for i in mc_items:
      mc_items2.append(i[len("minecraft:"):])
   unsupported = list(set(mc_items2) - set(all_items2))
   extra = list(set(all_items2) - set(mc_items2))
   print("Unsupported Minecraft items:")
   print(unsupported)
   print("Extra items?")
   print(extra)

   index = 0
   while index < len(mc_items):
      boxes = 0
      boxslot = 0
      command = "setblock ~ ~1 ~ chest{Items:["
      while index < len(mc_items) and len(command) < 32000:
         item = mc_items[index]
         if boxslot == 0:
            command += "{id:shulker_box,Count:1b,Slot:" +str(boxes)+ "b,tag:{BlockEntityTag:{Items:["
            boxes += 1
         command += "{id:\"" +item+ "\",Count:1b,Slot:" +str(boxslot)+ "b},"
         index += 1
         boxslot +=1
         if boxslot >= 27:
            boxslot = 0
         if boxslot == 0:
            command += "]}}},"
            if boxes >= 27:
               break
      if boxslot != 0:
         command += "]}}},"
      command += "]}"
      print(command)
