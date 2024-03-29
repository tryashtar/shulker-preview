import os
import re
import json
import math
import operator
import numpy
import shutil
from PIL import Image
from collections import OrderedDict
specials=["broken_elytra","crossbow_arrow","crossbow_firework"]
def main():


   shutil.make_archive("Shulker Preview Data Pack (1.15)", 'zip', "datapack")
   shutil.make_archive("Shulker Preview Resource Pack (1.15)", 'zip', "resourcepack")
   shutil.make_archive("Shulker Preview Dark Theme (1.15)", 'zip', "resourcepack_dark")
   return
   

   # load item textures from two sources
   print("Loading icons...")
   mcitems=load_items("D:/Minecraft/Java Storage/History/jar/assets/minecraft/textures/item", "../../extra item images")
   mcblocks=load_items("../../block images")
   mcoverlays=load_items("../../extra item images/overlay")

   # a few renames
   rename_key(mcitems, "clock_00", "clock")
   rename_key(mcitems, "compass_00", "compass")
   rename_key(mcitems, "crossbow_standby", "crossbow")

   # delete unnecessary textures
   delete_entries_regex(mcitems, r"^clock_\d\d$")
   delete_entries_regex(mcitems, r"^compass_\d\d$")
   delete_entries_regex(mcitems, r"^(cross)?bow_pulling_\d$")
   delete_entries_regex(mcitems, r"^empty_armor_slot_")
   delete_entries_regex(mcitems, r"_overlay")
   delete_entries(mcitems,["empty_armor_slot", "fishing_rod_cast", "tipped_arrow_head", "filled_map_markings", "ruby", "tipped_arrow_base", "spawn_egg", "crystallized_honey"])

   # 1.16 changes
   rename_key(mcitems, "zombified_piglin_spawn_egg", "zombie_pigman_spawn_egg")
   delete_entries(mcitems,["weeping_vines","twisting_vines","nether_sprouts","soul_fire_torch","soul_fire_lantern","hoglin_spawn_egg","piglin_spawn_egg","strider_spawn_egg"])
   delete_entries(mcblocks,["target","soul_soil","shroomlight","ancient_debris","crying_obsidian","nether_gold_ore","netherite_block","lodestone","respawn_anchor"])
   delete_entries_regex(mcblocks,r"warped_")
   delete_entries_regex(mcitems,r"warped_")
   delete_entries_regex(mcblocks,r"crimson_")
   delete_entries_regex(mcitems,r"crimson_")
   delete_entries_regex(mcitems,r"netherite_")
   delete_entries_regex(mcblocks,r"basalt")

   check_items(list(mcitems.keys())+list(mcblocks.keys()))

   # create grids
   print("Creating image sheets...")
   itemgrid=create_grid(mcitems)
   itemsheet=create_image(itemgrid, 16)
   itemsheet.save("resourcepack/assets/tryashtar.shulker_preview/textures/item_sheet.png", "PNG")
   blockgrid=create_grid(mcblocks)
   blocksheet=create_image(blockgrid, 64)
   blocksheet.save("resourcepack/assets/tryashtar.shulker_preview/textures/block_sheet.png", "PNG")
   overlaygrid=create_grid(mcoverlays)
   overlaysheet=create_image(overlaygrid, 16)
   overlaysheet.save("resourcepack/assets/tryashtar.shulker_preview/textures/overlay_sheet.png", "PNG")

   # start creating font providers
   print("Generating font providers...")
   providers=[{"comment":"Many thanks to AmberW#4615 for this invaluable concept","type":"bitmap","file":"tryashtar.shulker_preview:pixel.png","ascent":-32768,"height":-3,"chars":["\uf801"]},{"type":"bitmap","file":"tryashtar.shulker_preview:pixel.png","ascent":-32768,"height":-4,"chars":["\uf802"]},{"type":"bitmap","file":"tryashtar.shulker_preview:pixel.png","ascent":-32768,"height":-5,"chars":["\uf803"]},{"type":"bitmap","file":"tryashtar.shulker_preview:pixel.png","ascent":-32768,"height":-6,"chars":["\uf804"]},{"type":"bitmap","file":"tryashtar.shulker_preview:pixel.png","ascent":-32768,"height":-7,"chars":["\uf805"]},{"type":"bitmap","file":"tryashtar.shulker_preview:pixel.png","ascent":-32768,"height":-8,"chars":["\uf806"]},{"type":"bitmap","file":"tryashtar.shulker_preview:pixel.png","ascent":-32768,"height":-9,"chars":["\uf807"]},{"type":"bitmap","file":"tryashtar.shulker_preview:pixel.png","ascent":-32768,"height":-10,"chars":["\uf808"]},{"type":"bitmap","file":"tryashtar.shulker_preview:pixel.png","ascent":-32768,"height":-18,"chars":["\uf809"]},{"type":"bitmap","file":"tryashtar.shulker_preview:pixel.png","ascent":-32768,"height":-34,"chars":["\uf80a"]},{"type":"bitmap","file":"tryashtar.shulker_preview:pixel.png","ascent":-32768,"height":-66,"chars":["\uf80b"]},{"type":"bitmap","file":"tryashtar.shulker_preview:pixel.png","ascent":-32768,"height":-130,"chars":["\uf80c"]},{"type":"bitmap","file":"tryashtar.shulker_preview:pixel.png","ascent":-32768,"height":-258,"chars":["\uf80d"]},{"type":"bitmap","file":"tryashtar.shulker_preview:pixel.png","ascent":-32768,"height":-514,"chars":["\uf80e"]},{"type":"bitmap","file":"tryashtar.shulker_preview:pixel.png","ascent":-32768,"height":-1026,"chars":["\uf80f"]},{"type":"bitmap","file":"tryashtar.shulker_preview:pixel.png","ascent":-32768,"height":0,"chars":["\uf821"]},{"type":"bitmap","file":"tryashtar.shulker_preview:pixel.png","ascent":-32768,"height":1,"chars":["\uf822"]},{"type":"bitmap","file":"tryashtar.shulker_preview:pixel.png","ascent":-32768,"height":2,"chars":["\uf823"]},{"type":"bitmap","file":"tryashtar.shulker_preview:pixel.png","ascent":-32768,"height":3,"chars":["\uf824"]},{"type":"bitmap","file":"tryashtar.shulker_preview:pixel.png","ascent":-32768,"height":4,"chars":["\uf825"]},{"type":"bitmap","file":"tryashtar.shulker_preview:pixel.png","ascent":-32768,"height":5,"chars":["\uf826"]},{"type":"bitmap","file":"tryashtar.shulker_preview:pixel.png","ascent":-32768,"height":6,"chars":["\uf827"]},{"type":"bitmap","file":"tryashtar.shulker_preview:pixel.png","ascent":-32768,"height":7,"chars":["\uf828"]},{"type":"bitmap","file":"tryashtar.shulker_preview:pixel.png","ascent":-32768,"height":15,"chars":["\uf829"]},{"type":"bitmap","file":"tryashtar.shulker_preview:pixel.png","ascent":-32768,"height":31,"chars":["\uf82a"]},{"type":"bitmap","file":"tryashtar.shulker_preview:pixel.png","ascent":-32768,"height":63,"chars":["\uf82b"]},{"type":"bitmap","file":"tryashtar.shulker_preview:pixel.png","ascent":-32768,"height":127,"chars":["\uf82c"]},{"type":"bitmap","file":"tryashtar.shulker_preview:pixel.png","ascent":-32768,"height":255,"chars":["\uf82d"]},{"type":"bitmap","file":"tryashtar.shulker_preview:pixel.png","ascent":-32768,"height":511,"chars":["\uf82e"]},{"type":"bitmap","file":"tryashtar.shulker_preview:pixel.png","ascent":-32768,"height":1023,"chars":["\uf82f"]},{"type":"bitmap","file":"tryashtar.shulker_preview:pixel.png","ascent":-32770,"height":-32770,"chars":["\uf800"]},{"type":"bitmap","file":"tryashtar.shulker_preview:pixel.png","ascent":-32768,"height":32767,"chars":["\uf820"]},{"type":"bitmap","file":"tryashtar.shulker_preview:comma.png","ascent":7,"chars":[","]}]
   providers.append(register_single("tryashtar.shulker_preview:shulker_tooltip.png", "shulker_tooltip", 23, 78, (["max",-4],[-175,"-max"])))
   providers.append(register_single("tryashtar.shulker_preview:shulker_tooltip_header.png", "shulker_tooltip_header", 23, 78, (["max",-4],[-175,"-max"])))
   providers.append(register_single("tryashtar.shulker_preview:ender_tooltip.png", "ender_tooltip", 23, 78, (["max",-4],[-175,"-max"])))

   # per-row icons
   for row in range(0, 3):
      height=-18*row
      numbers=[f"number.{i}.{row}" for i in range(0,10)]
      providers.append(register_grid("tryashtar.shulker_preview:numbers.png", [numbers], height-4, 8, (["max",-7],[-6,"-max"])))
      dur1=[f"durability.{i}.{row}" for i in range(1,6)]
      dur2=[f"durability.{i}.{row}" for i in range(6,11)]
      dur3=[f"durability.{i}.{row}" for i in range(11,15)]+[None]
      providers.append(register_grid("tryashtar.shulker_preview:durability.png", [dur1,dur2,dur3], height-8, 2, (["max",-16],[-4,"-max"])))

      # item/block/overlay grids
      providers.append(register_grid("tryashtar.shulker_preview:item_sheet.png", apply_to_all(grid_keys(itemgrid), lambda x: f"item.{x}.{row}"), height+5, 16, (["max"],[-5,"-max"])))
      providers.append(register_grid("tryashtar.shulker_preview:block_sheet.png", apply_to_all(grid_keys(blockgrid), lambda x: f"block.{x}.{row}"), height+5, 16, (["max"],[-5,"-max"])))
      providers.append(register_grid("tryashtar.shulker_preview:overlay_sheet.png", apply_to_all(grid_keys(overlaygrid), lambda x: f"overlay.{x}.{row}"), height+5, 16, (["max",-18],[-5,"-max"])))

      # remaining numbers 10-64
      for n in range(10, 65):
         digit1=str(n)[0]
         digit2=str(n)[1]
         translations[f"tryashtar.shulker_preview.number.{n}.{row}"]=get_spacing(["max",-13])+charmap[f"number.{digit1}.{row}"]+get_spacing([-1])+charmap[f"number.{digit2}.{row}"]+get_spacing([-6,"-max"])

   # write translations and providers
   print("Writing JSONs...")
   write_json(translations, "resourcepack/assets/minecraft/lang/en_us.json")
   write_json({"providers":providers}, "resourcepack/assets/minecraft/font/default.json")

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

   shutil.make_archive("Shulker Preview Data Pack (1.15)", 'zip', "datapack")
   shutil.make_archive("Shulker Preview Resource Pack (1.15)", 'zip', "resourcepack")
   shutil.make_archive("Shulker Preview Dark Theme (1.15)", 'zip', "resourcepack_dark")


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
      file.write(json.dumps(j, indent=3))

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

currentchar='\uE000'
charmap={}
translations={"%1$s":"%2$s","tryashtar.shulker_preview.empty_slot":get_spacing(["max",12,"-max"]),"tryashtar.shulker_preview.row_end":get_spacing(["max",-168,"-max"])}
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
         translations[f"tryashtar.shulker_preview.{entry}"]=get_spacing(spacing[0])+currentchar+get_spacing(spacing[1])
         string+=currentchar
         currentchar=chr(ord(currentchar)+1)
      chars.append(string)
   base["chars"]=chars
   return base

# shortcut to create provider from one image
def register_single(fileid, iconname, ascent, height, spacing):
   return register_grid(fileid, [[iconname]], ascent, height, spacing)

# take [item name->path] dictionary and form it into an ordered square 2D array of tuples (missing spaces are filled in with None)
def create_grid(icondict):
   size=get_dimensions(len(icondict))
   ordered=sorted(icondict.items(), key=lambda x: x[0])
   ordered.extend([None]*(size[0]*size[1]-len(ordered)))
   result=numpy.array(ordered)
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
   from urllib.request import urlopen
   data=urlopen('https://raw.githubusercontent.com/misode/mcmeta/1.15-summary/registries/data.json').read()
   registry=json.loads(data)["item"]
   for item in registry:
      name=item.replace("minecraft:","")
      if name not in items and name!="air":
         print(f"ITEM NOT SUPPORTED: {name}")
   for item in items:
      if name not in registry and item not in specials:
         print(f"UNNECESSARY ITEM? {item}")

# item information
durability_dict={"leather_helmet":55,"leather_chestplate":80,"leather_leggings":75,"leather_boots":65,"golden_helmet":77,"golden_chestplate":112,"golden_leggings":105,"golden_boots":91,"chainmail_helmet":165,"chainmail_chestplate":240,"chainmail_leggings":225,"chainmail_boots":195,"iron_helmet":165,"iron_chestplate":240,"iron_leggings":225,"iron_boots":195,"diamond_helmet":363,"diamond_chestplate":528,"diamond_leggings":495,"diamond_boots":429,"golden_axe":32,"golden_pickaxe":32,"golden_shovel":32,"golden_hoe":32,"golden_sword":32,"wooden_axe":59,"wooden_pickaxe":59,"wooden_shovel":59,"wooden_hoe":59,"wooden_sword":59,"stone_axe":131,"stone_pickaxe":131,"stone_shovel":131,"stone_hoe":131,"stone_sword":131,"iron_axe":250,"iron_pickaxe":250,"iron_shovel":250,"iron_hoe":250,"iron_sword":250,"diamond_axe":1561,"diamond_pickaxe":1561,"diamond_shovel":1561,"diamond_hoe":1561,"diamond_sword":1561,"fishing_rod":64,"flint_and_steel":64,"carrot_on_a_stick":25,"shears":238,"shield":336,"bow":384,"trident":250,"elytra":432,"crossbow":326}
potion_dict={"night_vision":"night_vision","long_night_vision":"night_vision","invisibility":"invisibility","long_invisibility":"invisibility","leaping":"leaping","strong_leaping":"leaping","long_leaping":"leaping","fire_resistance":"fire_resistance","long_fire_resistance":"fire_resistance","swiftness":"swiftness","strong_swiftness":"swiftness","long_swiftness":"swiftness","water_breathing":"water_breathing","long_water_breathing":"water_breathing","healing":"healing","strong_healing":"healing","harming":"harming","strong_harming":"harming","poison":"poison","strong_poison":"poison","long_poison":"poison","regeneration":"regeneration","strong_regeneration":"regeneration","long_regeneration":"regeneration","strength":"strength","strong_strength":"strength","long_strength":"strength","weakness":"weakness","long_weakness":"weakness","luck":"luck","turtle_master":"turtle_master","strong_turtle_master":"turtle_master","long_turtle_master":"turtle_master","slow_falling":"slow_falling","long_slow_falling":"slow_falling"}

# generates a very specific function
def process_item_lines(items, row):
   lines=[]
   potion=False
   durability=False
   arrow=False
   for item, itemtype in sorted(items, key=lambda x: x[0]):
      name="minecraft:"+item
      if item == "elytra":
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
