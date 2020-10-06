import os
import re
import json
import math
import operator
import numpy
import shutil
from PIL import Image
from collections import OrderedDict

specials=["broken_elytra","crossbow_arrow","crossbow_firework","spawn_egg","spawn_egg_overlay","firework_star_overlay","leather_boots_overlay","leather_chestplate_overlay","leather_helmet_overlay","leather_leggings_overlay","potion_overlay","tipped_arrow_base","tipped_arrow_head", "filled_map_markings"]
def main():
   # load item textures from two sources
   print("Loading icons...")
   mcitems=load_items("D:/Minecraft/Java Storage/History/jar/assets/minecraft/textures/item")
   for item in reused_textures:
      mcitems[item]="."
   for item in spawn_egg_colors:
      mcitems[item]="."
   mcitems["tipped_arrow"]="."
   mcblocks=load_items("../block images")
   mcbanners=load_items("../block images/banner")

   # a few renames
   rename_key(mcitems, "clock_00", "clock")
   rename_key(mcitems, "compass_00", "compass")
   rename_key(mcitems, "crossbow_standby", "crossbow")

   # delete unnecessary textures
   delete_entries_regex(mcitems, r"^clock_\d\d$")
   delete_entries_regex(mcitems, r"^compass_\d\d$")
   delete_entries_regex(mcitems, r"^(cross)?bow_pulling_\d$")
   delete_entries_regex(mcitems, r"^empty_armor_slot_")
   delete_entries(mcitems,["empty_armor_slot", "fishing_rod_cast", "ruby", "crystallized_honey"])
   blockitems=["acacia_sapling","activator_rail","allium","azure_bluet","birch_sapling","black_stained_glass_pane","blue_orchid","blue_stained_glass_pane","brain_coral","brain_coral_fan","brown_mushroom","brown_stained_glass_pane","bubble_coral","bubble_coral_fan","cobweb","cornflower","crimson_fungus","crimson_roots","cyan_stained_glass_pane","dandelion","dark_oak_sapling","dead_brain_coral","dead_brain_coral_fan","dead_bubble_coral","dead_bubble_coral_fan","dead_bush","dead_fire_coral","dead_fire_coral_fan","dead_horn_coral","dead_horn_coral_fan","dead_tube_coral","dead_tube_coral_fan","detector_rail","fern","fire_coral","fire_coral_fan","glass_pane","grass","gray_stained_glass_pane","green_stained_glass_pane","horn_coral","horn_coral_fan","iron_bars","jungle_sapling","ladder","large_fern","lever","light_blue_stained_glass_pane","light_gray_stained_glass_pane","lilac","lily_of_the_valley","lily_pad","lime_stained_glass_pane","magenta_stained_glass_pane","nether_sprouts","oak_sapling","orange_stained_glass_pane","orange_tulip","oxeye_daisy","peony","pink_stained_glass_pane","pink_tulip","poppy","powered_rail","purple_stained_glass_pane","rail","redstone_torch","red_mushroom","red_stained_glass_pane","red_tulip","rose_bush","soul_torch","spruce_sapling","sunflower","tall_grass","torch","tripwire_hook","tube_coral","tube_coral_fan","twisting_vines","vine","warped_fungus","warped_roots","weeping_vines","white_stained_glass_pane","white_tulip","wither_rose","yellow_stained_glass_pane"]
   for blockitem in blockitems:
      mcitems[blockitem]="block"

   check_items(list(mcitems.keys())+list(mcblocks.keys()))

   mcitems=dict(sorted(mcitems.items()))
   mcblocks=dict(sorted(mcblocks.items()))
   mcbanners=dict(sorted(mcbanners.items()))

   mc_block_textures={}
   for k,v in mcblocks.items():
      mc_block_textures[k]=v
   for k,v in mcbanners.items():
      mc_block_textures[f"banner_pattern.{k}"]=v

   # create grids
   print("Creating image sheets...")
   blockgrid=create_grid(mc_block_textures)
   blocksheet=create_image(blockgrid, 64)
   blocksheet.save("resourcepack/assets/tryashtar.shulker_preview/textures/block_sheet.png", "PNG")

   # start creating font providers
   print("Generating font providers...")
   providers=[{"comment":"Many thanks to AmberW#4615 for this invaluable concept","type":"bitmap","file":"tryashtar.shulker_preview:pixel.png","ascent":-32768,"height":-3,"chars":["\uf801"]},{"type":"bitmap","file":"tryashtar.shulker_preview:pixel.png","ascent":-32768,"height":-4,"chars":["\uf802"]},{"type":"bitmap","file":"tryashtar.shulker_preview:pixel.png","ascent":-32768,"height":-5,"chars":["\uf803"]},{"type":"bitmap","file":"tryashtar.shulker_preview:pixel.png","ascent":-32768,"height":-6,"chars":["\uf804"]},{"type":"bitmap","file":"tryashtar.shulker_preview:pixel.png","ascent":-32768,"height":-7,"chars":["\uf805"]},{"type":"bitmap","file":"tryashtar.shulker_preview:pixel.png","ascent":-32768,"height":-8,"chars":["\uf806"]},{"type":"bitmap","file":"tryashtar.shulker_preview:pixel.png","ascent":-32768,"height":-9,"chars":["\uf807"]},{"type":"bitmap","file":"tryashtar.shulker_preview:pixel.png","ascent":-32768,"height":-10,"chars":["\uf808"]},{"type":"bitmap","file":"tryashtar.shulker_preview:pixel.png","ascent":-32768,"height":-18,"chars":["\uf809"]},{"type":"bitmap","file":"tryashtar.shulker_preview:pixel.png","ascent":-32768,"height":-34,"chars":["\uf80a"]},{"type":"bitmap","file":"tryashtar.shulker_preview:pixel.png","ascent":-32768,"height":-66,"chars":["\uf80b"]},{"type":"bitmap","file":"tryashtar.shulker_preview:pixel.png","ascent":-32768,"height":-130,"chars":["\uf80c"]},{"type":"bitmap","file":"tryashtar.shulker_preview:pixel.png","ascent":-32768,"height":-258,"chars":["\uf80d"]},{"type":"bitmap","file":"tryashtar.shulker_preview:pixel.png","ascent":-32768,"height":-514,"chars":["\uf80e"]},{"type":"bitmap","file":"tryashtar.shulker_preview:pixel.png","ascent":-32768,"height":-1026,"chars":["\uf80f"]},{"type":"bitmap","file":"tryashtar.shulker_preview:pixel.png","ascent":-32768,"height":0,"chars":["\uf821"]},{"type":"bitmap","file":"tryashtar.shulker_preview:pixel.png","ascent":-32768,"height":1,"chars":["\uf822"]},{"type":"bitmap","file":"tryashtar.shulker_preview:pixel.png","ascent":-32768,"height":2,"chars":["\uf823"]},{"type":"bitmap","file":"tryashtar.shulker_preview:pixel.png","ascent":-32768,"height":3,"chars":["\uf824"]},{"type":"bitmap","file":"tryashtar.shulker_preview:pixel.png","ascent":-32768,"height":4,"chars":["\uf825"]},{"type":"bitmap","file":"tryashtar.shulker_preview:pixel.png","ascent":-32768,"height":5,"chars":["\uf826"]},{"type":"bitmap","file":"tryashtar.shulker_preview:pixel.png","ascent":-32768,"height":6,"chars":["\uf827"]},{"type":"bitmap","file":"tryashtar.shulker_preview:pixel.png","ascent":-32768,"height":7,"chars":["\uf828"]},{"type":"bitmap","file":"tryashtar.shulker_preview:pixel.png","ascent":-32768,"height":15,"chars":["\uf829"]},{"type":"bitmap","file":"tryashtar.shulker_preview:pixel.png","ascent":-32768,"height":31,"chars":["\uf82a"]},{"type":"bitmap","file":"tryashtar.shulker_preview:pixel.png","ascent":-32768,"height":63,"chars":["\uf82b"]},{"type":"bitmap","file":"tryashtar.shulker_preview:pixel.png","ascent":-32768,"height":127,"chars":["\uf82c"]},{"type":"bitmap","file":"tryashtar.shulker_preview:pixel.png","ascent":-32768,"height":255,"chars":["\uf82d"]},{"type":"bitmap","file":"tryashtar.shulker_preview:pixel.png","ascent":-32768,"height":511,"chars":["\uf82e"]},{"type":"bitmap","file":"tryashtar.shulker_preview:pixel.png","ascent":-32768,"height":1023,"chars":["\uf82f"]},{"type":"bitmap","file":"tryashtar.shulker_preview:pixel.png","ascent":-32770,"height":-32770,"chars":["\uf800"]},{"type":"bitmap","file":"tryashtar.shulker_preview:pixel.png","ascent":-32768,"height":32767,"chars":["\uf820"]},{"type":"bitmap","file":"tryashtar.shulker_preview:pixel.png","ascent":0,"height":0,"chars":[","]}]
   providers.append(register_single("tryashtar.shulker_preview:shulker_tooltip.png", "shulker_tooltip", 23, 78, (get_spacing([-4]),get_spacing([-174]))))
   providers.append(register_single("tryashtar.shulker_preview:shulker_tooltip_header.png", "shulker_tooltip_header", 23, 78, (get_spacing([-4]),get_spacing([-174]))))
   providers.append(register_single("tryashtar.shulker_preview:ender_tooltip.png", "ender_tooltip", 23, 78, (get_spacing([-4]),get_spacing([-174]))))

   providers.extend(register_items(mcitems, 0, -32768, 16, False))
   # per-row icons
   for row in range(0, 3):
      height=-18*row
      numbers=[f"number.{i}.{row}" for i in range(0,10)]
      providers.append(register_grid("tryashtar.shulker_preview:numbers.png", [numbers], height-4, 8, lambda x:(get_spacing([-7]),get_spacing([-5]))))
      dur1=[f"durability.{i}.{row}" for i in range(1,6)]
      dur2=[f"durability.{i}.{row}" for i in range(6,11)]
      dur3=[f"durability.{i}.{row}" for i in range(11,15)]+[None]
      providers.append(register_grid("tryashtar.shulker_preview:durability.png", [dur1,dur2,dur3], height-8, 2, lambda x:(get_spacing([-16]),get_spacing([-3]))))

      # grids
      providers.append(register_grid("tryashtar.shulker_preview:block_sheet.png", apply_to_all(grid_keys(blockgrid), lambda x: block_translation(x,row)), height+5, 16, lambda x: block_spacing(x)))
      providers.extend(register_items(mcitems, row, height+5, 16, True))

      # remaining numbers 10-64
      for n in range(10, 65):
         digit1=str(n)[0]
         digit2=str(n)[1]
         translations[f"tryashtar.shulker_preview.number.{n}.{row}"]=get_spacing([-13])+charmap[f"number.{digit1}.{row}"]+get_spacing([-1])+charmap[f"number.{digit2}.{row}"]+get_spacing([-5])

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
         f"execute if score #count shulker_preview matches 2.. run function tryashtar.shulker_preview:row_{row}/overlay/count"
         ])
      write_lines(lines, f"datapack/data/tryashtar.shulker_preview/functions/row_{row}/process_item.mcfunction")

      # item count overlay
      lines=["# create an entity that draws item counts"]
      for i in range(2, 65):
         n = str(i) if i < 64 else f"{i}.."
         lines.append(f'execute if score #count shulker_preview matches {n} run summon area_effect_cloud ~ ~0.9 ~ {{Tags:["tryashtar.shulker_preview"],CustomName:\'{{"translate":"tryashtar.shulker_preview.number.{i}.{row}"}}\'}}')
      write_lines(lines, f'datapack/data/tryashtar.shulker_preview/functions/row_{row}/overlay/count.mcfunction')

      # overlay/durability
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
         text += f' run summon area_effect_cloud ~ ~0.8 ~ {{Tags:["tryashtar.shulker_preview"],CustomName:\'{{"translate":"tryashtar.shulker_preview.durability.{i}.{row}"}}\'}}'
         lines.append(text)
      write_lines(lines, f'datapack/data/tryashtar.shulker_preview/functions/row_{row}/overlay/durability.mcfunction')

      # potion and arrow overlays
      potion_lines=["# create an entity that draws the proper potion overlay color"]
      arrow_lines=["# create an entity that draws the proper tipped arrow overlay color"]
      for potionname, color in potion_dict.items():
         if_item=f'execute if data storage tryashtar:shulker_preview item{{tag:{{Potion:"minecraft:{potionname}"}}}}'
         potion_lines.append(f'{if_item} run summon area_effect_cloud ~ ~0.1 ~ {{Tags:["tryashtar.shulker_preview"],CustomName:\'{{"translate":"tryashtar.shulker_preview.overlay.potion_overlay.{row}","color":"{color_hex(color)}"}}\'}}')
         arrow_lines.append(f'{if_item} run summon area_effect_cloud ~ ~0.3 ~ {{Tags:["tryashtar.shulker_preview"],CustomName:\'{{"translate":"tryashtar.shulker_preview.overlay.tipped_arrow_head.{row}","color":"{color_hex(color)}"}}\'}}')

      custom_potion_lines=[
         f'# create an entity that draws approximately the correct overlay color',
         f'execute store result score #color shulker_preview run data get storage tryashtar:shulker_preview item.tag.CustomPotionColor',
         f'function tryashtar.shulker_preview:row_{row}/analyze_color'
      ]
      custom_arrow_lines=custom_potion_lines.copy()

      # banner patterns
      banner_lines=[
         f'# recursively draw all banner patterns',
         f'function tryashtar.shulker_preview:row_{row}/overlay/banner_pattern',
         f'data remove storage tryashtar:shulker_preview item.tag.BlockEntityTag.Patterns[0]',
         f'execute if data storage tryashtar:shulker_preview item.tag.BlockEntityTag.Patterns[0] positioned ~ ~0.01 ~ run function tryashtar.shulker_preview:row_{row}/overlay/banner',
      ]
      banner_pattern_lines=[
         f'# create an entity that draws a banner pattern overlay',
         f'data modify storage tryashtar:shulker_preview pattern set from storage tryashtar:shulker_preview item.tag.BlockEntityTag.Patterns[0]'
      ]
      for cid,cname in int_colors.items():
         chex=dye_colors[cname]
         banner_pattern_lines.append(f'execute if data storage tryashtar:shulker_preview pattern{{Color:{cid}}} run function tryashtar.shulker_preview:row_{row}/overlay/banner/{cname}')
         single_pattern_lines=[]
         for i,(pid,pname) in enumerate(banner_pattern_ids.items()):
            single_pattern_lines.append(f'execute if data storage tryashtar:shulker_preview pattern{{Pattern:"{pid}"}} run summon area_effect_cloud ~ ~{round(i*0.0001,4)} ~ {{Tags:["tryashtar.shulker_preview"],CustomName:\'{{"translate":"tryashtar.shulker_preview.banner_pattern.{pname}.{row}","color":"#{chex}"}}\'}}')
         write_lines(single_pattern_lines, f"datapack/data/tryashtar.shulker_preview/functions/row_{row}/overlay/banner/{cname}.mcfunction")


      # dyed armor
      default_armor_lines=[
         f'# create an entity that draws approximately colored armor',
         f'execute store result score #color shulker_preview run data get storage tryashtar:shulker_preview item.tag.display.color',
         f'function tryashtar.shulker_preview:row_{row}/analyze_color',
      ]
      armor_lines={
         "leather_helmet": default_armor_lines.copy(),
         "leather_chestplate": default_armor_lines.copy(),
         "leather_leggings": default_armor_lines.copy(),
         "leather_boots": default_armor_lines.copy(),
         "leather_horse_armor": default_armor_lines.copy()
      }

      # map markings
      map_lines=[
         f'# create an entity that draws the proper map overlay color',
         f'execute store result score #color shulker_preview run data get storage tryashtar:shulker_preview item.tag.display.MapColor'
      ]
      map_unless='execute '
      for color in [3830373, 5393476]:
         map_lines.append(f'execute if score #color shulker_preview matches {color} run summon area_effect_cloud ~ ~0.5 ~ {{Tags:["tryashtar.shulker_preview"],CustomName:\'{{"translate":"tryashtar.shulker_preview.overlay.filled_map_markings.{row}","color":"{color_hex(color)}"}}\'}}')
         map_unless+=f'unless score #color shulker_preview matches {color} '
      map_unless+=f'run function tryashtar.shulker_preview:row_{row}/overlay/custom_map'
      map_lines.append(map_unless)

      custom_map_lines=[
         f'# create an entity that draws approximately the correct overlay color',
         f'function tryashtar.shulker_preview:row_{row}/analyze_color',
      ]

      # color analysis
      lines=[
         "# pick the closest of the 16 dye colors",
         "scoreboard players operation #red shulker_preview = #color shulker_preview",
         "scoreboard players operation #red shulker_preview /= #256 shulker_preview",
         "scoreboard players operation #red shulker_preview /= #256 shulker_preview",
         "scoreboard players operation #red shulker_preview %= #256 shulker_preview",
         "scoreboard players operation #green shulker_preview = #color shulker_preview",
         "scoreboard players operation #green shulker_preview /= #256 shulker_preview",
         "scoreboard players operation #green shulker_preview %= #256 shulker_preview",
         "scoreboard players operation #blue shulker_preview = #color shulker_preview",
         "scoreboard players operation #blue shulker_preview %= #256 shulker_preview",
         "scoreboard players set #nearest shulker_preview 2147483647",
         ""
      ]
      color_assigns=[]
      for i,(color,chex) in enumerate(dye_colors.items()):
         rgb=tuple(int(chex[i:i+2], 16) for i in (0, 2, 4))
         r,g,b=rgb
         rgbint=(r<<16) + (g<<8) + b
         color_assigns.append(f"execute if score #diff{i} shulker_preview = #nearest shulker_preview run scoreboard players set #near_color shulker_preview {rgbint}")
         lines.append(f"# {color}")
         lines.append(f"scoreboard players operation #mean shulker_preview = #red shulker_preview")
         lines.append(f"scoreboard players add #mean shulker_preview {r}")
         lines.append(f"scoreboard players operation #mean shulker_preview /= #2 shulker_preview")
         lines.append(f"scoreboard players set #mean2 shulker_preview 767")
         lines.append(f"scoreboard players operation #mean2 shulker_preview -= #mean shulker_preview")
         lines.append(f"scoreboard players operation #red_diff shulker_preview = #red shulker_preview")
         lines.append(f"scoreboard players remove #red_diff shulker_preview {r}")
         lines.append(f"scoreboard players operation #red_diff shulker_preview *= #red_diff shulker_preview")
         lines.append(f"scoreboard players operation #green_diff shulker_preview = #green shulker_preview")
         lines.append(f"scoreboard players remove #green_diff shulker_preview {g}")
         lines.append(f"scoreboard players operation #green_diff shulker_preview *= #green_diff shulker_preview")
         lines.append(f"scoreboard players operation #blue_diff shulker_preview = #blue shulker_preview")
         lines.append(f"scoreboard players remove #blue_diff shulker_preview {b}")
         lines.append(f"scoreboard players operation #blue_diff shulker_preview *= #blue_diff shulker_preview")
         lines.append(f"scoreboard players add #mean shulker_preview 512")
         lines.append(f"scoreboard players operation #red_diff shulker_preview *= #mean shulker_preview")
         lines.append(f"scoreboard players operation #red_diff shulker_preview /= #256 shulker_preview")
         lines.append(f"scoreboard players operation #green_diff shulker_preview *= #4 shulker_preview")
         lines.append(f"scoreboard players operation #blue_diff shulker_preview *= #mean2 shulker_preview")
         lines.append(f"scoreboard players operation #blue_diff shulker_preview /= #256 shulker_preview")
         lines.append(f"scoreboard players operation #diff{i} shulker_preview = #red_diff shulker_preview")
         lines.append(f"scoreboard players operation #diff{i} shulker_preview += #green_diff shulker_preview")
         lines.append(f"scoreboard players operation #diff{i} shulker_preview += #blue_diff shulker_preview")
         lines.append(f"scoreboard players operation #nearest shulker_preview < #diff{i} shulker_preview")
         lines.append("")
         custom_potion_lines.append(f'execute if score #near_color shulker_preview matches {rgbint} run summon area_effect_cloud ~ ~0.2 ~ {{Tags:["tryashtar.shulker_preview"],CustomName:\'{{"translate":"tryashtar.shulker_preview.overlay.potion_overlay.{row}","color":"#{chex}"}}\'}}')
         custom_arrow_lines.append(f'execute if score #near_color shulker_preview matches {rgbint} run summon area_effect_cloud ~ ~0.4 ~ {{Tags:["tryashtar.shulker_preview"],CustomName:\'{{"translate":"tryashtar.shulker_preview.overlay.tipped_arrow_head.{row}","color":"#{chex}"}}\'}}')
         custom_map_lines.append(f'execute if score #near_color shulker_preview matches {rgbint} run summon area_effect_cloud ~ ~0.6 ~ {{Tags:["tryashtar.shulker_preview"],CustomName:\'{{"translate":"tryashtar.shulker_preview.overlay.filled_map_markings.{row}","color":"#{chex}"}}\'}}')
         for armor,armorlines in armor_lines.items():
            armorlines.append(f'execute if score #near_color shulker_preview matches {rgbint} run summon area_effect_cloud ~ ~ ~ {{Tags:["tryashtar.shulker_preview"],CustomName:\'{{"translate":"tryashtar.shulker_preview.item.{armor}.{row}","color":"#{chex}"}}\'}}')

      lines.extend(color_assigns)
      write_lines(lines, f"datapack/data/tryashtar.shulker_preview/functions/row_{row}/analyze_color.mcfunction")

      write_lines(potion_lines, f"datapack/data/tryashtar.shulker_preview/functions/row_{row}/overlay/potion.mcfunction")
      write_lines(custom_potion_lines, f"datapack/data/tryashtar.shulker_preview/functions/row_{row}/overlay/custom_potion.mcfunction")
      write_lines(arrow_lines, f"datapack/data/tryashtar.shulker_preview/functions/row_{row}/overlay/arrow.mcfunction")
      write_lines(custom_arrow_lines, f"datapack/data/tryashtar.shulker_preview/functions/row_{row}/overlay/custom_arrow.mcfunction")
      write_lines(map_lines, f"datapack/data/tryashtar.shulker_preview/functions/row_{row}/overlay/map.mcfunction")
      write_lines(custom_map_lines, f"datapack/data/tryashtar.shulker_preview/functions/row_{row}/overlay/custom_map.mcfunction")
      write_lines(banner_lines, f"datapack/data/tryashtar.shulker_preview/functions/row_{row}/overlay/banner.mcfunction")
      write_lines(banner_pattern_lines, f"datapack/data/tryashtar.shulker_preview/functions/row_{row}/overlay/banner_pattern.mcfunction")
      for armor,lines in armor_lines.items():
         dye_armor=armor.replace("leather_","").replace("_armor","")
         write_lines(lines, f"datapack/data/tryashtar.shulker_preview/functions/row_{row}/dye_armor/{dye_armor}.mcfunction")


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
            command += f'{{id:shulker_box,Count:1b,Slot:{boxes}b,tag:{{BlockEntityTag:{{Items:['
            boxes += 1
         command += f'{{id:"minecraft:{item}",Count:1b,Slot:{boxslot}b}},'
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

def block_translation(key, row):
   if not "." in key:
      key="block."+key
   return f"{key}.{row}"

def block_spacing(key):
   if "banner_pattern." in key:
      return (get_spacing([-18]),get_spacing([-4]))
   return ("",get_spacing([-4]))

def read_json(path):
   with open(path, "r") as file:
      return json.loads(file.read())

def write_json(j, path):
   with open(path, "w") as file:
      file.write(json.dumps(j, indent=3, ensure_ascii=True))

def write_lines(lines, path):
   folder=os.path.dirname(path)
   if not os.path.isdir(folder):
      os.makedirs(folder)
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
translations={"%1$s%418634357$s":"%2$s","tryashtar.shulker_preview.empty_slot":get_spacing([13]),"tryashtar.shulker_preview.row_end":get_spacing([-167])}
# create a provider from file name, grid of icon names, and ascent/height
# returns provider and also modifies charmap, a global [icon->character code] dictionary, and translations, which is charmap but with prefixed keys, and values padded with positive/negative spaces as specified in spacing
def register_grid(fileid, icongrid, ascent, height, spacing_lambda):
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
         spacing=spacing_lambda(entry)
         if spacing is not None:
            translations[f"tryashtar.shulker_preview.{entry}"]=spacing[0]+currentchar+spacing[1]
         string+=currentchar
         currentchar=next_legal_character(currentchar)
      chars.append(string)
   base["chars"]=chars
   return base

def next_legal_character(currentchar):
   i=ord(currentchar)
   i+=1
   if i>=0x600 and i<=0x6ff:
      i=0x700
   return chr(i)

def register_items(items, row, ascent, height, real_version):
   global currentchar
   results=[]
   for item,v in items.items():
      if "_spawn_egg" in item or item in reused_textures:
         continue
      location=item.replace("glass_pane","glass")
      location={"large_fern":"large_fern_top","lilac":"lilac_top","peony":"peony_top","rose_bush":"rose_bush_top","sunflower":"sunflower_front","clock":"clock_00","compass":"compass_00","crossbow":"crossbow_standby","tall_grass":"tall_grass_top","tipped_arrow":"tipped_arrow_base","twisting_vines":"twisting_vines_plant","weeping_vines":"weeping_vines_plant"}.get(location,location)
      itype="block" if v=="block" else "item"
      thingtype="item"
      if item in ["tipped_arrow_head","spawn_egg_overlay","potion_overlay","leather_boots_overlay","leather_chestplate_overlay","leather_helmet_overlay","leather_leggings_overlay","firework_star_overlay","filled_map_markings"]:
         thingtype="overlay"
      if real_version:
         negative=charmap[f"negative.{thingtype}.{item}"]
         firstspace=""
         if thingtype=="overlay":
            firstspace=get_spacing([-18])
         results.append(register_single(f"minecraft:{itype}/{location}.png", f"{thingtype}.{item}.{row}", ascent, height, (firstspace,negative+get_spacing([10]))))         
      else:
         results.append(register_single(f"minecraft:{itype}/{location}.png", f"negative.{thingtype}.{item}", -32768, -height, None))
   return results

# shortcut to create provider from one image
def register_single(fileid, iconname, ascent, height, spacing):
   return register_grid(fileid, [[iconname]], ascent, height, lambda x: spacing)

# take [item name->path] dictionary and form it into an ordered square 2D array of tuples (missing spaces are filled in with None)
def create_grid(icondict):
   size=get_dimensions(len(icondict))
   ordered=list(icondict.items())
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
durability_dict={"leather_helmet":55,"leather_chestplate":80,"leather_leggings":75,"leather_boots":65,"golden_helmet":77,"golden_chestplate":112,"golden_leggings":105,"golden_boots":91,"chainmail_helmet":165,"chainmail_chestplate":240,"chainmail_leggings":225,"chainmail_boots":195,"iron_helmet":165,"iron_chestplate":240,"iron_leggings":225,"iron_boots":195,"diamond_helmet":363,"diamond_chestplate":528,"diamond_leggings":495,"diamond_boots":429,"golden_axe":32,"golden_pickaxe":32,"golden_shovel":32,"golden_hoe":32,"golden_sword":32,"wooden_axe":59,"wooden_pickaxe":59,"wooden_shovel":59,"wooden_hoe":59,"wooden_sword":59,"stone_axe":131,"stone_pickaxe":131,"stone_shovel":131,"stone_hoe":131,"stone_sword":131,"iron_axe":250,"iron_pickaxe":250,"iron_shovel":250,"iron_hoe":250,"iron_sword":250,"diamond_axe":1561,"diamond_pickaxe":1561,"diamond_shovel":1561,"diamond_hoe":1561,"diamond_sword":1561,"fishing_rod":64,"flint_and_steel":64,"carrot_on_a_stick":25,"shears":238,"shield":336,"bow":384,"trident":250,"elytra":432,"crossbow":326,"warped_fungus_on_a_stick":100,"netherite_axe":2031,"netherite_sword":2031,"netherite_pickaxe":2031,"netherite_shovel":2031,"netherite_hoe":2031,"netherite_helmet":407,"netherite_chestplate":592,"netherite_leggings":555,"netherite_boots":481}
potion_dict={"night_vision":2039713,"long_night_vision":2039713,"invisibility":8356754,"long_invisibility":8356754,"leaping":2293580,"strong_leaping":2293580,"long_leaping":2293580,"fire_resistance":14981690,"long_fire_resistance":14981690,"swiftness":8171462,"strong_swiftness":8171462,"long_swiftness":8171462,"water_breathing":3035801,"long_water_breathing":3035801,"healing":16262179,"strong_healing":16262179,"harming":4393481,"strong_harming":4393481,"poison":5149489,"strong_poison":5149489,"long_poison":5149489,"regeneration":13458603,"strong_regeneration":13458603,"long_regeneration":13458603,"strength":9643043,"strong_strength":9643043,"long_strength":9643043,"weakness":4738376,"long_weakness":4738376,"luck":3381504,"turtle_master":0x755b62,"strong_turtle_master":0x735c64,"long_turtle_master":0x755b62,"slow_falling":16773073,"long_slow_falling":16773073,"slowness":5926017,"long_slowness":5926017,"strong_slowness":5926017,"water":3694022,"thick":3694022,"mundane":3694022,"awkward":3694022}
potion_dict=dict(sorted(potion_dict.items()))

int_colors={
   0:"white",
   1:"orange",
   2:"magenta",
   3:"light_blue",
   4:"yellow",
   5:"lime",
   6:"pink",
   7:"gray",
   8:"light_gray",
   9:"cyan",
   10:"purple",
   11:"blue",
   12:"brown",
   13:"green",
   14:"red",
   15:"black"
}

dye_colors={
   "white": "f9fffe",
   "orange": "f9801d",
   "magenta": "c74ebd",
   "light_blue": "3ab3da",
   "yellow": "fed83d",
   "lime": "80c71f",
   "pink": "f38baa",
   "gray": "474f52",
   "light_gray": "9d9d97",
   "cyan": "169c9c",
   "purple": "8932b8",
   "blue": "3c44aa",
   "brown": "835432",
   "green": "5e7c16",
   "red": "b02e26",
   "black": "1d1d21"
}

banner_pattern_ids={
   "bs":"stripe_bottom",
   "ts":"stripe_top",
   "ls":"stripe_left",
   "rs":"stripe_right",
   "cs":"stripe_center",
   "ms":"stripe_middle",
   "drs":"stripe_downright",
   "dls":"stripe_downleft",
   "ss":"small_stripes",
   "cr":"cross",
   "sc":"straight_cross",
   "ld":"diagonal_left",
   "rud":"diagonal_right",
   "lud":"diagonal_up_left",
   "rd":"diagonal_up_right",
   "vh":"half_vertical",
   "vhr":"half_vertical_right",
   "hh":"half_horizontal",
   "hhb":"half_horizontal_bottom",
   "bl":"square_bottom_left",
   "br":"square_bottom_right",
   "tl":"square_top_left",
   "tr":"square_top_right",
   "bt":"triangle_bottom",
   "tt":"triangle_top",
   "bts":"triangles_bottom",
   "tts":"triangles_top",
   "mc":"circle",
   "mr":"rhombus",
   "bo":"border",
   "cbo":"curly_border",
   "bri":"bricks",
   "gra":"gradient",
   "gru":"gradient_up",
   "cre":"creeper",
   "sku":"skull",
   "flo":"flower",
   "moj":"mojang",
   "glb":"globe",
   "pig":"piglin"
}

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
   "piglin_brute_spawn_egg": (5843472, 16380836),
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

def color_hex(int_color):
   return "#"+format(int_color,'06x')

# generates a very specific function
def process_item_lines(items, row):
   lines=[]
   potion=False
   durability=False
   arrow=False
   filledmap=False
   banner=False
   for item, itemtype in sorted(items, key=lambda x: x[0]):
      name="minecraft:"+item
      if_item=f'execute if data storage tryashtar:shulker_preview item{{id:"{name}"}}'
      reused=reused_textures.get(item)
      grass=grass_colors.get(item)
      if reused is not None:
         lines.append(f'{if_item} run summon area_effect_cloud ~ ~ ~ {{Tags:["tryashtar.shulker_preview"],CustomName:\'{{"translate":"tryashtar.shulker_preview.{itemtype}.{reused}.{row}"}}\'}}')
      elif grass is not None:
         lines.append(f'{if_item} run summon area_effect_cloud ~ ~ ~ {{Tags:["tryashtar.shulker_preview"],CustomName:\'{{"translate":"tryashtar.shulker_preview.{itemtype}.{item}.{row}","color":"{grass}"}}\'}}')
      elif "spawn_egg" in item:
         color=spawn_egg_colors[item]
         lines.append(f'{if_item} run summon area_effect_cloud ~ ~ ~ {{Tags:["tryashtar.shulker_preview"],CustomName:\'[{{"translate":"tryashtar.shulker_preview.item.spawn_egg.{row}","color":"{color_hex(color[0])}"}},", ",{{"translate":"tryashtar.shulker_preview.overlay.spawn_egg_overlay.{row}","color":"{color_hex(color[1])}"}}]\'}}')
      elif item == "elytra":
         lines.extend([
            f'execute if data storage tryashtar:shulker_preview item{{id:"minecraft:elytra",tag:{{Damage:431}}}} run summon area_effect_cloud ~ ~ ~ {{Tags:["tryashtar.shulker_preview"],CustomName:\'{{"translate":"tryashtar.shulker_preview.item.broken_elytra.{row}"}}\'}}',
            f'{if_item} unless data storage tryashtar:shulker_preview item{{tag:{{Damage:431}}}} run summon area_effect_cloud ~ ~ ~ {{Tags:["tryashtar.shulker_preview"],CustomName:\'{{"translate":"tryashtar.shulker_preview.item.elytra.{row}"}}\'}}'
            ])
      elif item == "crossbow":
         lines.extend([
            f'execute if data storage tryashtar:shulker_preview item{{id:"minecraft:crossbow",tag:{{ChargedProjectiles:[{{id:"minecraft:arrow"}}]}}}} run summon area_effect_cloud ~ ~ ~ {{Tags:["tryashtar.shulker_preview"],CustomName:\'{{"translate":"tryashtar.shulker_preview.item.crossbow_arrow.{row}"}}\'}}',
            f'execute if data storage tryashtar:shulker_preview item{{id:"minecraft:crossbow",tag:{{ChargedProjectiles:[{{id:"minecraft:firework_rocket"}}]}}}} run summon area_effect_cloud ~ ~ ~ {{Tags:["tryashtar.shulker_preview"],CustomName:\'{{"translate":"tryashtar.shulker_preview.item.crossbow_firework.{row}"}}\'}}',
            f'{if_item} unless data storage tryashtar:shulker_preview item{{tag:{{ChargedProjectiles:[{{}}]}}}} run summon area_effect_cloud ~ ~ ~ {{Tags:["tryashtar.shulker_preview"],CustomName:\'{{"translate":"tryashtar.shulker_preview.item.crossbow.{row}"}}\'}}'
            ])
      elif item in ["leather_helmet","leather_chestplate","leather_leggings","leather_boots","leather_horse_armor"]:
         dye_armor=item.replace("leather_","").replace("_armor","")
         lines.append(f'{if_item} unless data storage tryashtar:shulker_preview item.tag.display.color run summon area_effect_cloud ~ ~ ~ {{Tags:["tryashtar.shulker_preview"],CustomName:\'{{"translate":"tryashtar.shulker_preview.item.{item}.{row}","color":"{color_hex(10511680)}"}}\'}}')
         lines.append(f'{if_item} if data storage tryashtar:shulker_preview item.tag.display.color run function tryashtar.shulker_preview:row_{row}/dye_armor/{dye_armor}')
         if item not in ("leather_chestplate","leather_horse_armor"):
            lines.append(f'{if_item} run summon area_effect_cloud ~ ~ ~ {{Tags:["tryashtar.shulker_preview"],CustomName:\'{{"translate":"tryashtar.shulker_preview.overlay.{item}_overlay.{row}"}}\'}}')
      elif item in ("potion","splash_potion","lingering_potion"):
         lines.append(f'{if_item} run summon area_effect_cloud ~ ~ ~ {{Tags:["tryashtar.shulker_preview"],CustomName:\'[{{"translate":"tryashtar.shulker_preview.item.{item}.{row}"}},", ",{{"translate":"tryashtar.shulker_preview.overlay.potion_overlay.{row}","color":"{color_hex(16253176)}"}}]\'}}')
         potion=True
      elif item=="firework_star":
         lines.append(f'{if_item} run summon area_effect_cloud ~ ~ ~ {{Tags:["tryashtar.shulker_preview"],CustomName:\'[{{"translate":"tryashtar.shulker_preview.item.{item}.{row}"}},", ",{{"translate":"tryashtar.shulker_preview.overlay.firework_star_overlay.{row}","color":"{color_hex(9079434)}"}}]\'}}')
      elif item=="filled_map":
         lines.append(f'{if_item} run summon area_effect_cloud ~ ~ ~ {{Tags:["tryashtar.shulker_preview"],CustomName:\'{{"translate":"tryashtar.shulker_preview.item.{item}.{row}"}}\'}}')
         lines.append(f'{if_item} unless data storage tryashtar:shulker_preview item.tag.display.MapColor run summon area_effect_cloud ~ ~ ~ {{Tags:["tryashtar.shulker_preview"],CustomName:\'{{"translate":"tryashtar.shulker_preview.overlay.filled_map_markings.{row}","color":"#46402d"}}\'}}')
         filledmap=True
      elif item=="tipped_arrow":
         lines.append(f'{if_item} run summon area_effect_cloud ~ ~ ~ {{Tags:["tryashtar.shulker_preview"],CustomName:\'[{{"translate":"tryashtar.shulker_preview.item.{item}.{row}"}},", ",{{"translate":"tryashtar.shulker_preview.overlay.tipped_arrow_head.{row}","color":"{color_hex(16253176)}"}}]\'}}')
         arrow=True
      else:
         lines.append(f'{if_item} run summon area_effect_cloud ~ ~ ~ {{Tags:["tryashtar.shulker_preview"],CustomName:\'{{"translate":"tryashtar.shulker_preview.{itemtype}.{item}.{row}"}}\'}}')
      if "banner" in item and "pattern" not in item:
         banner=True
      if item in durability_dict:
         lines.append(f'{if_item} run scoreboard players set #max shulker_preview {durability_dict[item]}')
         durability=True
   if potion:
      lines.append(f'execute if data storage tryashtar:shulker_preview item.tag.Potion run function tryashtar.shulker_preview:row_{row}/overlay/potion')
      lines.append(f'execute if data storage tryashtar:shulker_preview item.tag.CustomPotionColor run function tryashtar.shulker_preview:row_{row}/overlay/custom_potion')
   if arrow:
      lines.append(f'execute if data storage tryashtar:shulker_preview item.tag.Potion run function tryashtar.shulker_preview:row_{row}/overlay/arrow')
      lines.append(f'execute if data storage tryashtar:shulker_preview item.tag.CustomPotionColor run function tryashtar.shulker_preview:row_{row}/overlay/custom_arrow')
   if filledmap:
      lines.append(f'execute if data storage tryashtar:shulker_preview item.tag.display.MapColor run function tryashtar.shulker_preview:row_{row}/overlay/map')
   if banner:
      lines.append(f'execute if data storage tryashtar:shulker_preview item.tag.BlockEntityTag.Patterns[0] positioned ~ ~0.7 ~ run function tryashtar.shulker_preview:row_{row}/overlay/banner')
   if durability:
      lines.extend([
         f'execute store result score #durability shulker_preview run data get storage tryashtar:shulker_preview item.tag.Damage',
         f'execute if data storage tryashtar:shulker_preview item.tag.Damage run function tryashtar.shulker_preview:row_{row}/overlay/durability'
         ])
   return lines

main()
