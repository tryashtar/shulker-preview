import os
import re
import json
import math
import operator
import numpy
import shutil
from PIL import Image
from collections import OrderedDict

specials=["broken_elytra","crossbow_arrow","crossbow_firework","spawn_egg","spawn_egg_overlay","firework_star_overlay","leather_boots_overlay","leather_chestplate_overlay","leather_helmet_overlay","leather_leggings_overlay","potion_overlay"]
def main():
   # load item textures from two sources
   print("Loading icons...")
   mcitems=load_items("D:/Minecraft/Java Storage/History/jar/assets/minecraft/textures/item", "../extra item images")
   mcblocks=load_items("../block images")
   mcoverlays=load_items("../extra item images/overlay")

   # a few renames
   rename_key(mcitems, "clock_00", "clock")
   rename_key(mcitems, "compass_00", "compass")
   rename_key(mcitems, "crossbow_standby", "crossbow")

   # delete unnecessary textures
   delete_entries_regex(mcitems, r"^clock_\d\d$")
   delete_entries_regex(mcitems, r"^compass_\d\d$")
   delete_entries_regex(mcitems, r"^(cross)?bow_pulling_\d$")
   delete_entries_regex(mcitems, r"^empty_armor_slot_")
   delete_entries(mcitems,["empty_armor_slot", "fishing_rod_cast", "tipped_arrow_head", "filled_map_markings", "ruby", "tipped_arrow_base", "crystallized_honey"])
   blockitems=["acacia_sapling","activator_rail","allium","azure_bluet","birch_sapling","black_stained_glass_pane","blue_orchid","blue_stained_glass_pane","brain_coral","brain_coral_fan","brown_mushroom","brown_stained_glass_pane","bubble_coral","bubble_coral_fan","cobweb","cornflower","crimson_fungus","crimson_roots","cyan_stained_glass_pane","dandelion","dark_oak_sapling","dead_brain_coral","dead_brain_coral_fan","dead_bubble_coral","dead_bubble_coral_fan","dead_bush","dead_fire_coral","dead_fire_coral_fan","dead_horn_coral","dead_horn_coral_fan","dead_tube_coral","dead_tube_coral_fan","detector_rail","fern","fire_coral","fire_coral_fan","glass_pane","grass","gray_stained_glass_pane","green_stained_glass_pane","horn_coral","horn_coral_fan","iron_bars","jungle_sapling","ladder","large_fern","lever","light_blue_stained_glass_pane","light_gray_stained_glass_pane","lilac","lily_of_the_valley","lily_pad","lime_stained_glass_pane","magenta_stained_glass_pane","nether_sprouts","oak_sapling","orange_stained_glass_pane","orange_tulip","oxeye_daisy","peony","pink_stained_glass_pane","pink_tulip","poppy","potion","powered_rail","purple_stained_glass_pane","rail","redstone_torch","red_mushroom","red_stained_glass_pane","red_tulip","rose_bush","soul_torch","spruce_sapling","sunflower","tall_grass","torch","tripwire_hook","tube_coral","tube_coral_fan","twisting_vines","vine","warped_fungus","warped_roots","weeping_vines","white_stained_glass_pane","white_tulip","wither_rose","yellow_stained_glass_pane"]
   for blockitem in blockitems:
      mcitems[blockitem]="block"

   check_items(list(mcitems.keys())+list(mcblocks.keys()))

   mcitems=dict(sorted(mcitems.items()))
   mcblocks=dict(sorted(mcblocks.items()))
   mcoverlays=dict(sorted(mcoverlays.items()))

   # create grids
   print("Creating image sheets...")
   blockgrid=create_grid(mcblocks)
   blocksheet=create_image(blockgrid, 64)
   blocksheet.save("resourcepack/assets/tryashtar.shulker_preview/textures/block_sheet.png", "PNG")

   # start creating font providers
   print("Generating font providers...")
   providers=[{"comment":"Many thanks to AmberW#4615 for this invaluable concept","type":"bitmap","file":"tryashtar.shulker_preview:pixel.png","ascent":-32768,"height":-3,"chars":["\uf801"]},{"type":"bitmap","file":"tryashtar.shulker_preview:pixel.png","ascent":-32768,"height":-4,"chars":["\uf802"]},{"type":"bitmap","file":"tryashtar.shulker_preview:pixel.png","ascent":-32768,"height":-5,"chars":["\uf803"]},{"type":"bitmap","file":"tryashtar.shulker_preview:pixel.png","ascent":-32768,"height":-6,"chars":["\uf804"]},{"type":"bitmap","file":"tryashtar.shulker_preview:pixel.png","ascent":-32768,"height":-7,"chars":["\uf805"]},{"type":"bitmap","file":"tryashtar.shulker_preview:pixel.png","ascent":-32768,"height":-8,"chars":["\uf806"]},{"type":"bitmap","file":"tryashtar.shulker_preview:pixel.png","ascent":-32768,"height":-9,"chars":["\uf807"]},{"type":"bitmap","file":"tryashtar.shulker_preview:pixel.png","ascent":-32768,"height":-10,"chars":["\uf808"]},{"type":"bitmap","file":"tryashtar.shulker_preview:pixel.png","ascent":-32768,"height":-18,"chars":["\uf809"]},{"type":"bitmap","file":"tryashtar.shulker_preview:pixel.png","ascent":-32768,"height":-34,"chars":["\uf80a"]},{"type":"bitmap","file":"tryashtar.shulker_preview:pixel.png","ascent":-32768,"height":-66,"chars":["\uf80b"]},{"type":"bitmap","file":"tryashtar.shulker_preview:pixel.png","ascent":-32768,"height":-130,"chars":["\uf80c"]},{"type":"bitmap","file":"tryashtar.shulker_preview:pixel.png","ascent":-32768,"height":-258,"chars":["\uf80d"]},{"type":"bitmap","file":"tryashtar.shulker_preview:pixel.png","ascent":-32768,"height":-514,"chars":["\uf80e"]},{"type":"bitmap","file":"tryashtar.shulker_preview:pixel.png","ascent":-32768,"height":-1026,"chars":["\uf80f"]},{"type":"bitmap","file":"tryashtar.shulker_preview:pixel.png","ascent":-32768,"height":0,"chars":["\uf821"]},{"type":"bitmap","file":"tryashtar.shulker_preview:pixel.png","ascent":-32768,"height":1,"chars":["\uf822"]},{"type":"bitmap","file":"tryashtar.shulker_preview:pixel.png","ascent":-32768,"height":2,"chars":["\uf823"]},{"type":"bitmap","file":"tryashtar.shulker_preview:pixel.png","ascent":-32768,"height":3,"chars":["\uf824"]},{"type":"bitmap","file":"tryashtar.shulker_preview:pixel.png","ascent":-32768,"height":4,"chars":["\uf825"]},{"type":"bitmap","file":"tryashtar.shulker_preview:pixel.png","ascent":-32768,"height":5,"chars":["\uf826"]},{"type":"bitmap","file":"tryashtar.shulker_preview:pixel.png","ascent":-32768,"height":6,"chars":["\uf827"]},{"type":"bitmap","file":"tryashtar.shulker_preview:pixel.png","ascent":-32768,"height":7,"chars":["\uf828"]},{"type":"bitmap","file":"tryashtar.shulker_preview:pixel.png","ascent":-32768,"height":15,"chars":["\uf829"]},{"type":"bitmap","file":"tryashtar.shulker_preview:pixel.png","ascent":-32768,"height":31,"chars":["\uf82a"]},{"type":"bitmap","file":"tryashtar.shulker_preview:pixel.png","ascent":-32768,"height":63,"chars":["\uf82b"]},{"type":"bitmap","file":"tryashtar.shulker_preview:pixel.png","ascent":-32768,"height":127,"chars":["\uf82c"]},{"type":"bitmap","file":"tryashtar.shulker_preview:pixel.png","ascent":-32768,"height":255,"chars":["\uf82d"]},{"type":"bitmap","file":"tryashtar.shulker_preview:pixel.png","ascent":-32768,"height":511,"chars":["\uf82e"]},{"type":"bitmap","file":"tryashtar.shulker_preview:pixel.png","ascent":-32768,"height":1023,"chars":["\uf82f"]},{"type":"bitmap","file":"tryashtar.shulker_preview:pixel.png","ascent":-32770,"height":-32770,"chars":["\uf800"]},{"type":"bitmap","file":"tryashtar.shulker_preview:pixel.png","ascent":-32768,"height":32767,"chars":["\uf820"]},{"type":"bitmap","file":"tryashtar.shulker_preview:comma.png","ascent":7,"chars":[","]}]
   providers.append(register_single("tryashtar.shulker_preview:shulker_tooltip.png", "shulker_tooltip", 23, 78, (get_spacing(["max",-4]),get_spacing([-175,"-max"]))))
   providers.append(register_single("tryashtar.shulker_preview:shulker_tooltip_header.png", "shulker_tooltip_header", 23, 78, (get_spacing(["max",-4]),get_spacing([-175,"-max"]))))
   providers.append(register_single("tryashtar.shulker_preview:ender_tooltip.png", "ender_tooltip", 23, 78, (get_spacing(["max",-4]),get_spacing([-175,"-max"]))))

   providers.extend(register_items(mcitems, 0, -32768, 16, False))
   # per-row icons
   for row in range(0, 3):
      height=-18*row
      numbers=[f"number.{i}.{row}" for i in range(0,10)]
      providers.append(register_grid("tryashtar.shulker_preview:numbers.png", [numbers], height-4, 8, (get_spacing(["max",-7]),get_spacing([-6,"-max"]))))
      dur1=[f"durability.{i}.{row}" for i in range(1,6)]
      dur2=[f"durability.{i}.{row}" for i in range(6,11)]
      dur3=[f"durability.{i}.{row}" for i in range(11,15)]+[None]
      providers.append(register_grid("tryashtar.shulker_preview:durability.png", [dur1,dur2,dur3], height-8, 2, (get_spacing(["max",-16]),get_spacing([-4,"-max"]))))

      # item/block/overlay grids
      providers.append(register_grid("tryashtar.shulker_preview:block_sheet.png", apply_to_all(grid_keys(blockgrid), lambda x: f"block.{x}.{row}"), height+5, 16, (get_spacing(["max"]),get_spacing([-5,"-max"]))))
      providers.extend(register_items(mcitems, row, height+5, 16, True))

      # remaining numbers 10-64
      for n in range(10, 65):
         digit1=str(n)[0]
         digit2=str(n)[1]
         translations[f"tryashtar.shulker_preview.number.{n}.{row}"]=get_spacing(["max",-13])+charmap[f"number.{digit1}.{row}"]+get_spacing([-1])+charmap[f"number.{digit2}.{row}"]+get_spacing([-6,"-max"])

   # write translations and providers
   print("Writing JSONs...")
   write_json(translations, "resourcepack/assets/tryashtar.shulker_preview/lang/en_us.json")
   write_json({"providers":providers}, "resourcepack/assets/tryashtar.shulker_preview/font/preview.json")

   # create dictionary of item lengths
   print("Creating functions...")
   all_items={i:"item" for i in mcitems.keys()}
   all_items.update({i:"block" for i in mcblocks.keys()})
   for texture in specials:
      del all_items[texture]
   length_dict={}
   for item, itemtype in all_items.items():
      name="minecraft:"+item
      if len(name) in length_dict:
         length_dict[len(name)].append((item,itemtype))
      else:
         length_dict[len(name)]=[(item,itemtype)]

   # write main and subfunctions
   for row in range(0, 3):
      # process_item
      lines=[
      "# get the length of this item and call the appropriate function",
      "execute store result score #length shulker_preview run data get storage tryashtar:shulker_preview item.id"
      ]
      lengths=list(length_dict.keys())
      lengths.sort()
      for length in lengths:
         lines.append(f"execute if score #length shulker_preview matches {length} run function tryashtar.shulker_preview:row_{row}/process_item/length_{length}")
         sublines=process_item_lines(length_dict[length], row)
         write_lines(sublines, f"datapack/data/tryashtar.shulker_preview/functions/row_{row}/process_item\\length_{length}.mcfunction")
      lines.extend([
         "",
         "# summon in count entity",
         "execute store result score #count shulker_preview run data get storage tryashtar:shulker_preview item.Count",
         f"execute if score #count shulker_preview matches 2.. run function tryashtar.shulker_preview:row_{row}/process_count"
         ])
      write_lines(lines, f"datapack/data/tryashtar.shulker_preview/functions/row_{row}/process_item.mcfunction")

      # process_count
      lines=["# create an entity that draws item counts"]
      for i in range(2, 65):
         n = str(i) if i < 64 else f"{i}.."
         lines.append("execute if score #count shulker_preview matches "+n+" run summon area_effect_cloud ~ ~0.2 ~ {Tags:[\"tryashtar.shulker_preview\"],CustomName:'{\"translate\":\"tryashtar.shulker_preview.number."+str(i)+"."+str(row)+"\"}'}")
      write_lines(lines, f"datapack/data/tryashtar.shulker_preview/functions/row_{row}/process_count.mcfunction")

      # process_durability
      lines=[
      "# create an entity that draws a durability bar",
      "scoreboard players operation #durability shulker_preview *= #13000 shulker_preview",
      "scoreboard players operation #durability shulker_preview /= #max shulker_preview"      ]
      for i in range(1, 15):
         text=f"execute if score #durability shulker_preview matches "
         lower=1000*i-1500
         upper=1000*i-501
         if i == 14:
            text += f"{lower}.."
         elif i == 1:
            text += f"1..{upper}"
         else:
            text += f"{lower}..{upper}"
         text += " run summon area_effect_cloud ~ ~0.3 ~ {Tags:[\"tryashtar.shulker_preview\"],CustomName:'{\"translate\":\"tryashtar.shulker_preview.durability."+str(i)+"."+str(row)+"\"}'}"
         lines.append(text)
      write_lines(lines, f"datapack/data/tryashtar.shulker_preview/functions/row_{row}/process_durability.mcfunction")

      # process_potion and process_arrow
      lines1=["# create an entity that draws the proper potion overlay color"]
      lines2=["# create an entity that draws the proper tipped arrow overlay color"]
      for potionname, colorname in potion_dict.items():
         lines1.append("execute if data storage tryashtar:shulker_preview item{tag:{Potion:\"minecraft:"+potionname+"\"}} run summon area_effect_cloud ~ ~0.1 ~ {Tags:[\"tryashtar.shulker_preview\"],CustomName:'{\"translate\":\"tryashtar.shulker_preview.overlay.potion_liquid."+colorname+"."+str(row)+"\"}'}")
         lines2.append("execute if data storage tryashtar:shulker_preview item{tag:{Potion:\"minecraft:"+potionname+"\"}} run summon area_effect_cloud ~ ~0.1 ~ {Tags:[\"tryashtar.shulker_preview\"],CustomName:'{\"translate\":\"tryashtar.shulker_preview.overlay.arrow_dust."+colorname+"."+str(row)+"\"}'}")
      write_lines(lines1, f"datapack/data/tryashtar.shulker_preview/functions/row_{row}/process_potion.mcfunction")
      write_lines(lines2, f"datapack/data/tryashtar.shulker_preview/functions/row_{row}/process_arrow.mcfunction")

   # generate all items for testing
   index = 0
   chest_items=list(all_items.keys())
   while index < len(chest_items):
      boxes = 0
      boxslot = 0
      command = "setblock ~ ~1 ~ chest{Items:["
      while index < len(chest_items) and len(command) < 32000:
         item = chest_items[index]
         if boxslot == 0:
            command += "{id:shulker_box,Count:1b,Slot:" +str(boxes)+ "b,tag:{BlockEntityTag:{Items:["
            boxes += 1
         command += "{id:\"minecraft:" +item+ "\",Count:1b,Slot:" +str(boxslot)+ "b},"
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

   shutil.make_archive("Shulker Preview Data Pack (1.16)", 'zip', "datapack")
   shutil.make_archive("Shulker Preview Resource Pack (1.16)", 'zip', "resourcepack")
   shutil.make_archive("Shulker Preview Dark Theme (1.16)", 'zip', "resourcepack_dark")


def unicode_escape(character):
   return "\\u"+str(character.encode("unicode-escape"))[5:9].upper()

def grid_keys(tuple_grid):
   return apply_to_all(tuple_grid, lambda x: x[0])

def apply_to_all(tuple_grid, lamb):
   return [[(None if j is None else lamb(j)) for j in i] for i in tuple_grid]

def read_json(path):
   with open(path, "r") as file:
      return json.loads(file.read())

def write_json(j, path):
   with open(path, "w") as file:
      file.write(json.dumps(j, indent=3, ensure_ascii=True))

def write_lines(lines, path):
   with open(path, "w") as file:
      for line in lines:
         file.write(line+"\n")

# fewest positive/negative spaces required to move this many pixels
positive_spaces=OrderedDict([(1024,'\uF82F'),(512,'\uF82E'),(256,'\uF82D'),(128,'\uF82C'),(64,'\uF82B'),(32,'\uF82A'),(16,'\uF829'),(8,'\uF828'),(7,'\uF827'),(6,'\uF826'),(5,'\uF825'),(4,'\uF824'),(3,'\uF823'),(2,'\uF822'),(1,'\uF821')])
negative_spaces=OrderedDict([(-1024,'\uF80F'),(-512,'\uF80E'),(-256,'\uF80D'),(-128,'\uF80C'),(-64,'\uF80B'),(-32,'\uF80A'),(-16,'\uF809'),(-8,'\uF808'),(-7,'\uF807'),(-6,'\uF806'),(-5,'\uF805'),(-4,'\uF804'),(-3,'\uF803'),(-2,'\uF802'),(-1,'\uF801')])
# input is list of spaces to apply
# numbers are in pixels, alternativey "max" or "-max" in sequence applies respective size space
def get_spacing(sequence):
   result=""
   for pixels in sequence:
      if pixels=="max":
         result+='\uF820'
      elif pixels=="-max":
         result+='\uF800'
      elif pixels>=0:
         for space in positive_spaces:
            while pixels>=space:
               pixels-=space
               result+=positive_spaces[space]
      else:
         for space in negative_spaces:
            while pixels<=space:
               pixels-=space
               result+=negative_spaces[space]
   return result

currentchar='\u00b0'
charmap={}
translations={"%1$s%418634357$s":"%2$s","tryashtar.shulker_preview.empty_slot":get_spacing(["max",12,"-max"]),"tryashtar.shulker_preview.row_end":get_spacing(["max",-168,"-max"])}
# create a provider from file name, grid of icon names, and ascent/height
# returns provider and also modifies charmap, a global [icon->character code] dictionary, and translations, which is charmap but with prefixed keys, and values padded with positive/negative spaces as specified in spacing
def register_grid(fileid, icongrid, ascent, height, spacing):
   global currentchar
   base={"type":"bitmap","file":fileid,"ascent":ascent,"height":height}
   chars=[]
   for row in icongrid:
      string=""
      for entry in row:
         if entry is None:
            string+='\u0000'
            continue
         charmap[entry]=currentchar
         if spacing is not None:
            translations[f"tryashtar.shulker_preview.{entry}"]=spacing[0]+currentchar+spacing[1]
         string+=currentchar
         currentchar=chr(ord(currentchar)+1)
      chars.append(string)
   base["chars"]=chars
   return base

def register_items(items, row, ascent, height, real_version):
   global currentchar
   results=[]
   for item,v in items.items():
      if "_spawn_egg" in item or item in reused_textures:
         continue
      location=item.replace("glass_pane","glass")
      location={"large_fern":"large_fern_top","lilac":"lilac_top","peony":"peony_top","rose_bush":"rose_bush_top","sunflower":"sunflower_front","clock":"clock_00","compass":"compass_00","crossbow":"crossbow_standby","tall_grass":"tall_grass_top","tipped_arrow":"tipped_arrow_base","twisting_vines":"twisting_vines_plant","weeping_vines":"weeping_vines_plant"}.get(location,location)
      itype="block" if v=="block" else "item"
      if real_version:
         negative=charmap[f"negative.item.{item}"]
         results.append(register_single(f"minecraft:{itype}/{location}.png", f"item.{item}.{row}", ascent, height, (get_spacing(["max"]),negative+get_spacing([9,"-max"]))))         
      else:
         results.append(register_single(f"minecraft:{itype}/{location}.png", f"negative.item.{item}", -32768, -height, None))
   return results

# shortcut to create provider from one image
def register_single(fileid, iconname, ascent, height, spacing):
   return register_grid(fileid, [[iconname]], ascent, height, spacing)

# take [item name->path] dictionary and form it into an ordered square 2D array of tuples (missing spaces are filled in with None)
def create_grid(icondict):
   size=get_dimensions(len(icondict))
   ordered=sorted(icondict.items(), key=lambda x: x[0])
   ordered.extend([None]*(size[0]*size[1]-len(ordered)))
   result=numpy.empty(len(ordered), dtype=object)
   result[:]=ordered
   return numpy.reshape(result, size)

# returns an integer square that fits this area
# might remove bottom row if it would be empty
def get_dimensions(area):
   width=math.ceil(math.sqrt(area))
   height=width
   if width*(height-1)>=area:
      height-=1
   return (height,width)

# take square 2D array of (item name, path) tuples and add images to a large image grid
def create_image(grid, icon_size):
   dim=grid.shape
   sheet=Image.new("RGBA", (dim[1]*icon_size,dim[0]*icon_size))
   for pos, icon in numpy.ndenumerate(grid):
      if icon is None:
         continue
      x=pos[1]*icon_size
      y=pos[0]*icon_size
      path=icon[1]
      with Image.open(path).convert("RGBA") as sprite:
         pixels = sprite.load()
         for corner in (0,icon_size-1):
            r,g,b,a = pixels[corner,corner]
            if a==0:
               r,g,b=(139,139,139)
            pixels[corner,corner] = (r,g,b,max(a,18))
         sheet.paste(sprite, (x, y, x+icon_size, y+icon_size))
   return sheet

def rename_key(dictionary, oldname, newname):
   dictionary[newname]=dictionary.pop(oldname)

def delete_entries_regex(dictionary, regex):
   for k in list(dictionary):
      if re.search(regex,k):
         del dictionary[k] 

def delete_entries(dictionary, keys):
   for k in keys:
      if k in dictionary:
         del dictionary[k]

# create [item name->path] dictionary from reading PNG files in one or more folders
def load_items(*args):
   result={}
   for folder in args:
      for file in os.listdir(folder):
         ext=os.path.splitext(file)[1]
         if ext==".png":
            name=os.path.splitext(file)[0]
            location=os.path.join(folder,file)
            result[name]=location
   return result

def check_items(items):
   registry=read_json("D:/Minecraft/Java Storage/History/reports/registries.json")["minecraft:item"]["entries"]
   for item in registry:
      name=item.replace("minecraft:","")
      if name not in items and name!="air":
         print(f"ITEM NOT SUPPORTED: {name}")
   for item in items:
      name="minecraft:"+item
      if name not in registry and item not in specials:
         print(f"UNNECESSARY ITEM? {item}")

# item information
durability_dict={"leather_helmet":55,"leather_chestplate":80,"leather_leggings":75,"leather_boots":65,"golden_helmet":77,"golden_chestplate":112,"golden_leggings":105,"golden_boots":91,"chainmail_helmet":165,"chainmail_chestplate":240,"chainmail_leggings":225,"chainmail_boots":195,"iron_helmet":165,"iron_chestplate":240,"iron_leggings":225,"iron_boots":195,"diamond_helmet":363,"diamond_chestplate":528,"diamond_leggings":495,"diamond_boots":429,"golden_axe":32,"golden_pickaxe":32,"golden_shovel":32,"golden_hoe":32,"golden_sword":32,"wooden_axe":59,"wooden_pickaxe":59,"wooden_shovel":59,"wooden_hoe":59,"wooden_sword":59,"stone_axe":131,"stone_pickaxe":131,"stone_shovel":131,"stone_hoe":131,"stone_sword":131,"iron_axe":250,"iron_pickaxe":250,"iron_shovel":250,"iron_hoe":250,"iron_sword":250,"diamond_axe":1561,"diamond_pickaxe":1561,"diamond_shovel":1561,"diamond_hoe":1561,"diamond_sword":1561,"fishing_rod":64,"flint_and_steel":64,"carrot_on_a_stick":25,"shears":238,"shield":336,"bow":384,"trident":250,"elytra":432,"crossbow":326}
potion_dict={"night_vision":"night_vision","long_night_vision":"night_vision","invisibility":"invisibility","long_invisibility":"invisibility","leaping":"leaping","strong_leaping":"leaping","long_leaping":"leaping","fire_resistance":"fire_resistance","long_fire_resistance":"fire_resistance","swiftness":"swiftness","strong_swiftness":"swiftness","long_swiftness":"swiftness","water_breathing":"water_breathing","long_water_breathing":"water_breathing","healing":"healing","strong_healing":"healing","harming":"harming","strong_harming":"harming","poison":"poison","strong_poison":"poison","long_poison":"poison","regeneration":"regeneration","strong_regeneration":"regeneration","long_regeneration":"regeneration","strength":"strength","strong_strength":"strength","long_strength":"strength","weakness":"weakness","long_weakness":"weakness","luck":"luck","turtle_master":"turtle_master","strong_turtle_master":"turtle_master","long_turtle_master":"turtle_master","slow_falling":"slow_falling","long_slow_falling":"slow_falling"}
spawn_egg_colors={
   "bat_spawn_egg": (4996656, 986895),
   "bee_spawn_egg": (15582019, 4400155),
   "blaze_spawn_egg": (16167425, 16775294),
   "cat_spawn_egg": (15714446, 9794134),
   "cave_spider_spawn_egg": (803406, 11013646),
   "chicken_spawn_egg": (10592673, 16711680),
   "cod_spawn_egg": (12691306, 15058059),
   "cow_spawn_egg": (4470310, 10592673),
   "creeper_spawn_egg": (894731, 0),
   "dolphin_spawn_egg": (2243405, 16382457),
   "donkey_spawn_egg": (5457209, 8811878),
   "drowned_spawn_egg": (9433559, 7969893),
   "elder_guardian_spawn_egg": (13552826, 7632531),
   "enderman_spawn_egg": (1447446, 0),
   "endermite_spawn_egg": (1447446, 7237230),
   "evoker_spawn_egg": (9804699, 1973274),
   "fox_spawn_egg": (14005919, 13396256),
   "ghast_spawn_egg": (16382457, 12369084),
   "guardian_spawn_egg": (5931634, 15826224),
   "hoglin_spawn_egg": (13004373, 6251620),
   "horse_spawn_egg": (12623485, 15656192),
   "husk_spawn_egg": (7958625, 15125652),
   "llama_spawn_egg": (12623485, 10051392),
   "magma_cube_spawn_egg": (3407872, 16579584),
   "mooshroom_spawn_egg": (10489616, 12040119),
   "mule_spawn_egg": (1769984, 5321501),
   "ocelot_spawn_egg": (15720061, 5653556),
   "panda_spawn_egg": (15198183, 1776418),
   "parrot_spawn_egg": (894731, 16711680),
   "phantom_spawn_egg": (4411786, 8978176),
   "pig_spawn_egg": (15771042, 14377823),
   "piglin_spawn_egg": (10051392, 16380836),
   "pillager_spawn_egg": (5451574, 9804699),
   "polar_bear_spawn_egg": (15921906, 9803152),
   "pufferfish_spawn_egg": (16167425, 3654642),
   "rabbit_spawn_egg": (10051392, 7555121),
   "ravager_spawn_egg": (7697520, 5984329),
   "salmon_spawn_egg": (10489616, 951412),
   "sheep_spawn_egg": (15198183, 16758197),
   "shulker_spawn_egg": (9725844, 5060690),
   "silverfish_spawn_egg": (7237230, 3158064),
   "skeleton_spawn_egg": (12698049, 4802889),
   "skeleton_horse_spawn_egg": (6842447, 15066584),
   "slime_spawn_egg": (5349438, 8306542),
   "spider_spawn_egg": (3419431, 11013646),
   "squid_spawn_egg": (2243405, 7375001),
   "stray_spawn_egg": (6387319, 14543594),
   "strider_spawn_egg": (10236982, 5065037),
   "trader_llama_spawn_egg": (15377456, 4547222),
   "tropical_fish_spawn_egg": (15690005, 16775663),
   "turtle_spawn_egg": (15198183, 44975),
   "vex_spawn_egg": (8032420, 15265265),
   "villager_spawn_egg": (5651507, 12422002),
   "vindicator_spawn_egg": (9804699, 2580065),
   "wandering_trader_spawn_egg": (4547222, 15377456),
   "witch_spawn_egg": (3407872, 5349438),
   "wither_skeleton_spawn_egg": (1315860, 4672845),
   "wolf_spawn_egg": (14144467, 13545366),
   "zoglin_spawn_egg": (13004373, 15132390),
   "zombie_spawn_egg": (44975, 7969893),
   "zombie_horse_spawn_egg": (3232308, 9945732),
   "zombified_piglin_spawn_egg": (15373203, 5009705),
   "zombie_villager_spawn_egg": (5651507, 7969893),
}
reused_textures={"debug_stick":"stick","enchanted_golden_apple":"golden_apple"}
grass_colors={"vine":"#48b518","lily_pad":"#71c35c","grass":"#7bbd6b","fern":"#7bbd6b","tall_grass":"#7bbd6b","large_fern":"#7bbd6b"}

# generates a very specific function
def process_item_lines(items, row):
   lines=[]
   potion=False
   durability=False
   arrow=False
   for item, itemtype in sorted(items, key=lambda x: x[0]):
      name="minecraft:"+item
      reused=reused_textures.get(item)
      grass=grass_colors.get(item)
      if reused is not None:
         lines.append("execute if data storage tryashtar:shulker_preview item{id:\""+name+"\"} run summon area_effect_cloud ~ ~ ~ {Tags:[\"tryashtar.shulker_preview\"],CustomName:'{\"translate\":\"tryashtar.shulker_preview."+itemtype+"."+reused+"."+str(row)+"\"}'}")
      elif grass is not None:
         lines.append("execute if data storage tryashtar:shulker_preview item{id:\""+name+"\"} run summon area_effect_cloud ~ ~ ~ {Tags:[\"tryashtar.shulker_preview\"],CustomName:'{\"translate\":\"tryashtar.shulker_preview."+itemtype+"."+item+"."+str(row)+"\",\"color\":\""+grass+"\"}'}")
      elif "spawn_egg" in item:
         color=spawn_egg_colors[item]
         lines.append("execute if data storage tryashtar:shulker_preview item{id:\""+name+"\"} run summon area_effect_cloud ~ ~ ~ {Tags:[\"tryashtar.shulker_preview\"],CustomName:'[{\"translate\":\"tryashtar.shulker_preview.item.spawn_egg."+str(row)+"\",\"color\":\"#"+format(color[0],'06x')+"\"},\", \",{\"translate\":\"tryashtar.shulker_preview.item.spawn_egg_overlay."+str(row)+"\",\"color\":\"#"+format(color[1],'06x')+"\"}]'}")
      elif item == "elytra":
         lines.extend([
            "execute if data storage tryashtar:shulker_preview item{id:\"minecraft:elytra\",tag:{Damage:431}} run summon area_effect_cloud ~ ~ ~ {Tags:[\"tryashtar.shulker_preview\"],CustomName:'{\"translate\":\"tryashtar.shulker_preview.item.broken_elytra."+str(row)+"\"}'}",
            "execute if data storage tryashtar:shulker_preview item{id:\"minecraft:elytra\"} unless data storage tryashtar:shulker_preview item{id:\"minecraft:elytra\",tag:{Damage:431}} run summon area_effect_cloud ~ ~ ~ {Tags:[\"tryashtar.shulker_preview\"],CustomName:'{\"translate\":\"tryashtar.shulker_preview.item.elytra."+str(row)+"\"}'}"
            ])
      elif item == "crossbow":
         lines.extend([
            "execute if data storage tryashtar:shulker_preview item{id:\"minecraft:crossbow\",tag:{ChargedProjectiles:[{id:\"minecraft:arrow\"}]}} run summon area_effect_cloud ~ ~ ~ {Tags:[\"tryashtar.shulker_preview\"],CustomName:'{\"translate\":\"tryashtar.shulker_preview.item.crossbow_arrow."+str(row)+"\"}'}",
            "execute if data storage tryashtar:shulker_preview item{id:\"minecraft:crossbow\",tag:{ChargedProjectiles:[{id:\"minecraft:firework_rocket\"}]}} run summon area_effect_cloud ~ ~ ~ {Tags:[\"tryashtar.shulker_preview\"],CustomName:'{\"translate\":\"tryashtar.shulker_preview.item.crossbow_firework."+str(row)+"\"}'}",
            "execute if data storage tryashtar:shulker_preview item{id:\"minecraft:crossbow\"} unless data storage tryashtar:shulker_preview item{id:\"minecraft:crossbow\",tag:{ChargedProjectiles:[{}]}} run summon area_effect_cloud ~ ~ ~ {Tags:[\"tryashtar.shulker_preview\"],CustomName:'{\"translate\":\"tryashtar.shulker_preview.item.crossbow."+str(row)+"\"}'}"
            ])
      else:
         lines.append("execute if data storage tryashtar:shulker_preview item{id:\""+name+"\"} run summon area_effect_cloud ~ ~ ~ {Tags:[\"tryashtar.shulker_preview\"],CustomName:'{\"translate\":\"tryashtar.shulker_preview."+itemtype+"."+item+"."+str(row)+"\"}'}")
      if item in ("potion","splash_potion","lingering_potion"):
         potion=True
      if item in durability_dict:
         lines.append("execute if data storage tryashtar:shulker_preview item{id:\""+name+"\"} run scoreboard players set #max shulker_preview "+str(durability_dict[item]))
         durability = True
      if item == "tipped_arrow":
         arrow = True
   if potion:
      lines.append("execute if data storage tryashtar:shulker_preview item.tag.Potion run function tryashtar.shulker_preview:row_"+str(row)+"/process_potion")
   if durability:
      lines.extend([
         "execute store result score #durability shulker_preview run data get storage tryashtar:shulker_preview item.tag.Damage",
         "execute if data storage tryashtar:shulker_preview item.tag.Damage run function tryashtar.shulker_preview:row_"+str(row)+"/process_durability"
         ])
   if arrow:
      lines.append("execute if data storage tryashtar:shulker_preview item.tag.Potion run function tryashtar.shulker_preview:row_"+str(row)+"/process_arrow")
   return lines

main()
