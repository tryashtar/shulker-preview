import os
import re
import json
import math
import operator
import numpy
import shutil
import zipfile
from PIL import Image
from collections import OrderedDict
from urllib.request import urlopen

minecraft_dir = '%appdata%\\.minecraft'
version = '1.19-pre3'

def main():
   print('Loading Minecraft assets...')
   # get the actual list of item IDs from Misode's generator
   # there's no reliable place in the jar to get them,
   # and while you can get them from the server reports,
   # it would be a waste of time to find the server jar and generate them in this script
   data = urlopen(f'https://raw.githubusercontent.com/misode/mcmeta/{version}-summary/registries/data.json').read()
   item_registry = json.loads(data)["item"]
   item_registry.remove('air')
   jar_path = find_version_jar()
   mc = Minecraft(jar_path, item_registry, read_json('data.json'))
   font = FontAbstraction(3)
   font.add_texture('tryashtar.shulker_preview:missingno', 5, 16)
   print('Generating functions...')
   generate_functions(mc, font, 'datapack')
   font.save('resourcepack')
   shutil.make_archive("Shulker Preview Data Pack (1.19)", 'zip', "datapack")
   shutil.make_archive("Shulker Preview Resource Pack (1.19)", 'zip', "resourcepack")

   # to restore:
   # - potion/arrow/map overlays
   #   - first generate the "normal" command if this item was not special at all
   #   - but instead of writing it, write a function that checks for the colors and replaces color in normal command with appropriate color
   # - banner/shield overlays
   #   - need to use old method of generating grid from screenshots, doubt shaders can do this one
   # - dyed armor color
   #   - just like the other one, generate "normal" command but insert a place to colorize layer0
   # - all the overrides like light blocks
   # - generate test command
   # - sort output files again
   # - leather chestplates are bugged because vanilla overlay is invisible

# drawing an image as text with zero width requires multiple characters in the font
class FontAbstraction:
   def __init__(self, rows):
      self.current_char = '\u0900'
      self.characters = {}
      self.negatives = {}
      self.translations = {}
      self.textures = {}
      self.spaces = {}
      self.rows = rows
      for i in range(0, self.rows):
         self.characters[i] = {}
         self.translations[i] = {}

   # there are some ranges that Minecraft can't render, I have not fully determined what they are yet
   def next_char(self):
      i = ord(self.current_char)
      i += 1
      if i >= 0x600 and i <= 0x6ff:
         i = 0x700
      self.current_char = chr(i)
      return self.current_char

   # give a texture, it will generate characters and translations for each row
   def add_texture(self, texture, ascent, height):
      if texture in self.textures:
         return
      self.textures[texture] = {'ascent': ascent, 'height': height}
      for i in range(0, self.rows):
         self.characters[i][texture] = self.next_char()
         translation = remove_namespace(texture).replace('/', '.')
         self.translations[i][texture] = f'tryashtar.shulker_preview.{translation}.{i}'
      self.negatives[texture] = self.next_char()

   def get_translation(self, texture, row):
      return self.translations[row][texture]

   def get_space(self, size):
      if size not in self.spaces:
         self.spaces[size] = self.next_char()
      return self.spaces[size]

   def save(self, path):
      lang = {"%1$s%418634357$s":"%2$s"}
      font = []
      # create the tooltip characters
      # the tooltip is made by slicing the vanilla texture into rows and assembling them
      for tex, tip, bottom in [('shulker_box', 'shulker', 20), ('generic_54', 'ender', 27)]:
         tooltip_1 = self.next_char()
         tooltip_neg1 = self.next_char()
         tooltip_2 = self.next_char()
         tooltip_neg2 = self.next_char()
         tooltip_3 = self.next_char()
         tooltip_neg3 = self.next_char()
         split_2 = ['\u0000'] * 32
         split_neg2 = ['\u0000'] * 32
         split_3 = ['\u0000'] * 32
         split_neg3 = ['\u0000'] * 32
         split_2[8] = tooltip_2
         split_neg2[8] = tooltip_neg2
         split_3[bottom] = tooltip_3
         split_neg3[bottom] = tooltip_neg3
         font.extend([
            # top: the first two rows of slots and most of the third
            # we can only slice by whole numbers, and a slice any larger would be too big
            {"type": "bitmap", "file": f"minecraft:gui/container/{tex}.png", "ascent": 23, "height": 64, "chars": [tooltip_1, "\u0000", "\u0000", "\u0000"]},
            # negative version, used to bring the cursor back to draw the next row
            # in theory we could reuse this for each row, but it breaks if the slices are different widths
            {"type": "bitmap", "file": f"minecraft:gui/container/{tex}.png", "ascent": -32768, "height": -64, "chars": [tooltip_neg1, "\u0000", "\u0000", "\u0000"]},
            # middle: the rest of the third row
            {"type": "bitmap", "file": f"minecraft:gui/container/{tex}.png", "ascent": 23-64, "height": 8, "chars": split_2},
            {"type": "bitmap", "file": f"minecraft:gui/container/{tex}.png", "ascent": -32768, "height": -8, "chars": split_neg2},
            # bottom: the very bottom of the tooltip texture
            {"type": "bitmap", "file": f"minecraft:gui/container/{tex}.png", "ascent": 23-64-7, "height": 8, "chars": split_3},
            {"type": "bitmap", "file": f"minecraft:gui/container/{tex}.png", "ascent": -32768, "height": -8, "chars": split_neg3}
         ])
         # start by moving back a few pixels to fully cover the vanilla tooltip
         # then each row and negative in turn
         # then forward a few pixels, aligning the first item to draw with the first slot
         lang[f"tryashtar.shulker_preview.{tip}_tooltip"] = self.get_space(-4) + tooltip_1 + tooltip_neg1 + self.get_space(-3) + tooltip_2 + tooltip_neg2 + self.get_space(-3) + tooltip_3 + tooltip_neg3 + self.get_space(5)
      # take stack numbers from ascii.png
      empty_row = "".join(['\u0000'] * 16)
      for i in range(0, self.rows):
         nums = "".join([self.next_char() for x in range(0, 10)])
         shadows = "".join([self.next_char() for x in range(0, 10)])
         negs = "".join([self.next_char() for x in range(0, 10)])
         font.append({"type": "bitmap", "file": "minecraft:font/ascii.png", "ascent": -(18 * i) - 4, "height": 8, "chars": [
            empty_row,
            empty_row,
            empty_row,
            nums + "\u0000\u0000\u0000\u0000\u0000\u0000",
            empty_row,
            empty_row,
            empty_row,
            empty_row,
            empty_row,
            empty_row,
            empty_row,
            empty_row,
            empty_row,
            empty_row,
            empty_row,
            empty_row
         ]})
         font.append({"type": "bitmap", "file": "minecraft:font/ascii.png", "ascent": -(18 * i) - 5, "height": 8, "chars": [
            empty_row,
            empty_row,
            empty_row,
            shadows + "\u0000\u0000\u0000\u0000\u0000\u0000",
            empty_row,
            empty_row,
            empty_row,
            empty_row,
            empty_row,
            empty_row,
            empty_row,
            empty_row,
            empty_row,
            empty_row,
            empty_row,
            empty_row
         ]})
         font.append({"type": "bitmap", "file": "minecraft:font/ascii.png", "ascent": -32768, "height": -8, "chars": [
            empty_row,
            empty_row,
            empty_row,
            negs + "\u0000\u0000\u0000\u0000\u0000\u0000",
            empty_row,
            empty_row,
            empty_row,
            empty_row,
            empty_row,
            empty_row,
            empty_row,
            empty_row,
            empty_row,
            empty_row,
            empty_row,
            empty_row
         ]})
         # shadow has to be a separate translation so we can color it
         for j in range(1, 10):
            lang[f"tryashtar.shulker_preview.number.{j}.{i}"] = self.get_space(-4) + negs[j] + nums[j] + self.get_space(1)
            lang[f"tryashtar.shulker_preview.number_shadow.{j}.{i}"] = self.get_space(-3) + negs[j] + shadows[j]
         for j in range(10, 65):
            d1 = j // 10
            d2 = j % 10
            lang[f"tryashtar.shulker_preview.number.{j}.{i}"] = self.get_space(-7) + negs[d1] + negs[d2] + nums[d1] + nums[d2] + self.get_space(1)
            lang[f"tryashtar.shulker_preview.number_shadow.{j}.{i}"] = self.get_space(-6) + negs[d1] + negs[d2] + shadows[d1] + shadows[d2]
         # durability
         dura_chars = "".join([self.next_char() for x in range(0,14)])
         font.append({"type": "bitmap", "file": "tryashtar.shulker_preview:durability.png", "ascent": -8 - (18 * i), "height": 2, "chars": [
            dura_chars[0:5],
            dura_chars[5:10],
            dura_chars[10:15] + '\u0000'
         ]})
         for j in range(1, 15):
            lang[f"tryashtar.shulker_preview.durability.{j}.{i}"] = self.get_space(-16) + dura_chars[j - 1] + self.get_space(2)

      lang["tryashtar.shulker_preview.empty_slot"] = self.get_space(18)
      lang["tryashtar.shulker_preview.overlay"] = self.get_space(-18)
      lang["tryashtar.shulker_preview.row_end"] = self.get_space(-162)
      for t, data in self.textures.items():
         for i in range(0, self.rows):
            lang[self.translations[i][t]] = self.characters[i][t] + self.negatives[t] + self.get_space(15)
            font.append({"type": "bitmap", "file": t + '.png', "ascent": data['ascent'] - (18 * i), "height": data['height'], "chars": [self.characters[i][t]]})
         font.append({"type": "bitmap", "file": t + '.png', "ascent": -32768, "height": -data['height'], "chars": [self.negatives[t]]})
      # I'd prefer to use a space provider, but stuff draws in the wrong order without this method
      for s, ch in self.spaces.items():
         h = s - 2 if s < 0 else s - 1
         font.append({"type": "bitmap", "file": "tryashtar.shulker_preview:space.png", "ascent": -32768, "height": h, "chars": [ch]})
      write_json(lang, os.path.join(path, 'assets/tryashtar.shulker_preview/lang/en_us.json'))
      write_json({"providers":font}, os.path.join(path, 'assets/tryashtar.shulker_preview/font/preview.json'))

# use 'resource' to get the namespaced resource location
# use 'file_path' to get the path relative to the pack root
class Function:
   def __init__(self, resource, lines):
      self.resource = resource
      self.file_path = 'data/' + resource_to_path(self.resource, 'functions', 'mcfunction')
      self.lines = lines

   def save(self, path):
      write_lines(self.lines, os.path.join(path, self.file_path))


class Minecraft:
   def __init__(self, path, item_registry, data):
      self.zip = zipfile.ZipFile(path, 'r')
      self.models = {}
      self.textures = []
      self.items = item_registry
      self.length_dict = {}
      self.data = data
      for k,v in self.data['spawn_eggs'].items():
         self.data['hardcoded_tints']['layer0'][k] = color_hex(v[0])
         self.data['hardcoded_tints']['layer1'][k] = color_hex(v[1])
      for item in self.items:
         namespaced = add_namespace(item)
         length = len(namespaced)
         if length not in self.length_dict:
            self.length_dict[length] = []
         self.length_dict[length].append(item)

   # get model from resource location
   def get_model(self, resource):
      if resource in self.models:
         return self.models[resource]
      return self.load_model('assets/' + resource_to_path(resource, 'models', 'json'))

   # get model from relative file path
   # many models reference a common parent like 'block/block', this class caches and reuses those
   def load_model(self, path):
      resource = path_to_resource(path)
      if resource in self.models:
         return self.models[resource]
      data = json.loads(self.zip.read(path).decode('utf-8'))
      model = Model(resource, data)
      self.models[resource] = model
      current_model = model
      # extract and load override references
      overrides = current_model.data.get('overrides')
      if overrides is not None:
         for o in overrides:
            o_path = 'assets/' + resource_to_path(o['model'], 'models', 'json')
            model.overrides.append(self.load_model(o_path))
      # go through every parent model
      while True:
         # copy textures from the parent
         textures = current_model.data.get('textures')
         if textures is not None:
            for k,v in textures.items():
               if k not in model.textures:
                  model.textures[k] = v
         # find the parent and copy to hierarchy
         parent_path = current_model.data.get('parent')
         if parent_path is not None:
            parent_path = 'assets/' + resource_to_path(parent_path, 'models', 'json')
            # some parents are 'builtin' so aren't in the jar
            if parent_path in self.zip.namelist():
               parent = self.load_model(parent_path)
               model.parents.append(parent)
               current_model = parent
               continue
         break
      # if a texture reference is to an existing defined texture, reflect that
      # otherwise, it means this is a template model whose children define it,
      # and so it's safe to ignore since we don't process template models directly
      for k,v in list(model.textures.items()):
         if v.startswith('#'):
            if v[1:] in model.textures:
               model.textures[k] = model.textures[v[1:]]
            else:
               del model.textures[k]
      for k,v in model.textures.items():
         model.textures[k] = add_namespace(v)
      # keep a master copy of all referenced textures
      for v in model.textures.values():
         if v not in self.textures:
            self.textures.append(v)
      return model

# can't initialize itself effectively because we don't want to load the same parent models every time
# so instead the above class caches them and populates these fields
# 'resource' is the namespaced resource location e.g. 'minecraft:item/apple'
class Model:
   def __init__(self, resource, data):
      self.resource = resource
      self.data = data
      self.parents = []
      self.overrides = []
      self.textures = {}

def add_namespace(rc):
   if ':' in rc:
      return rc
   return 'minecraft:'+rc

def remove_namespace(rc):
   try:
      colon = rc.index(':')
      return rc[colon+1:]
   except ValueError:
      return rc

def resource_to_path(rc, folder, extension):
   try:
      colon = rc.index(':')
      return f"{rc[0:colon]}/{folder}/{rc[colon+1:]}.{extension}"
   except ValueError:
      return f"minecraft/{folder}/{rc}.{extension}"

def path_to_resource(path):
   items = path.replace('\\','/').split('/')
   items[-1] = os.path.splitext(items[-1])[0]
   return f'{items[1]}:{"/".join(items[3:])}'

def find_version_jar():
   for root, subdirs, files in os.walk(os.path.expandvars(minecraft_dir)):
      for file in files:
         if file == version+'.jar':
            return os.path.join(root, file)

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

def color_hex(int_color):
   return "#"+format(int_color,'06x')

def generate_functions(mc, font, path):
   for row in range(0, font.rows):
      fn_start = f'tryashtar.shulker_preview:row_{row}'
      process_item = Function(f'{fn_start}/process_item', [
         '# get the length of this item and call the appropriate function',
         'execute store result score #length shulker_preview run data get storage tryashtar.shulker_preview:data item.id'
      ])
      lengths = list(mc.length_dict.keys())
      lengths.sort()
      for length in range(0,100):
         subfunction = Function(f'{fn_start}/process_item/length_{length}', [])
         if length in lengths:
            process_item.lines.append(f'execute if score #length shulker_preview matches {length} run function {subfunction.resource}')
            subfunction.lines.extend(generate_item_lines(mc, mc.length_dict[length], row, font))
            subfunction.save(path)
         else:
            fpath = os.path.join(path, subfunction.file_path)
            if os.path.exists(fpath):
               os.remove(fpath)
      count = Function(f'{fn_start}/overlay/count', ['# create an entity that draws item counts'])
      for i in range(2, 65):
         n = str(i) if i < 64 else f"{i}.."
         count.lines.append(f'execute if score #count shulker_preview matches {n} run summon marker ~ ~0.9 ~ {{Tags:["tryashtar.shulker_preview"],CustomName:\'[{{"translate":"tryashtar.shulker_preview.number_shadow.{i}.{row}","color":"#3e3e3e"}},{{"translate":"tryashtar.shulker_preview.number.{i}.{row}","color":"white"}}]\'}}')
      count.save(path)
      process_item.lines.extend([
         '',
         '# placeholder if item was not found',
         f'execute unless entity @e[type=marker,tag=tryashtar.shulker_preview,distance=..0.0001] run summon marker ~ ~ ~ {{Tags:["tryashtar.shulker_preview"],CustomName:\'{{"translate":"{font.get_translation("tryashtar.shulker_preview:missingno", row)}"}}\'}}',
         '',
         '# summon in count entity',
         'execute store result score #count shulker_preview run data get storage tryashtar.shulker_preview:data item.Count',
         f'execute if score #count shulker_preview matches 2.. run function {count.resource}'
      ])
      process_item.save(path)

      # durability overlay
      durability = Function(f'{fn_start}/overlay/durability', [
         '# create an entity that draws a durability bar',
         'scoreboard players operation #durability shulker_preview *= #13000 shulker_preview',
         'scoreboard players operation #durability shulker_preview /= #max shulker_preview'
      ])
      for i in range(1, 15):
         text = f'execute if score #durability shulker_preview matches '
         lower = (1000 * i) - 1500
         upper = (1000 * i) - 501
         if i == 14:
            text += f'{lower}..'
         elif i == 1:
            text += f'1..{upper}'
         else:
            text += f'{lower}..{upper}'
         text += f' run summon marker ~ ~0.8 ~ {{Tags:["tryashtar.shulker_preview"],CustomName:\'{{"translate":"tryashtar.shulker_preview.durability.{i}.{row}"}}\'}}'
         durability.lines.append(text)
      durability.save(path)

def generate_item_lines(mc, items, row, font):
   lines = []
   durability = False
   for item in items:
      handled = False
      if_item=f'execute if data storage tryashtar.shulker_preview:data item{{id:"{add_namespace(item)}"}}'
      model = mc.get_model(f'minecraft:item/{item}')
      if len(model.overrides) > 0:
         # these items have overrides but should always look the same
         if item in ['bow', 'clock', 'compass', 'goat_horn', 'fishing_rod', 'recovery_compass']:
            pass
         else:
            # must be hardcoded
            print(f'Unhandled item {item}')
            handled = True
         pass
      if not handled and any(x.resource == 'minecraft:item/generated' for x in model.parents):
         # this is a normal layered item, generate as such
         handled = True
         name = []
         for i in range(0, 99):
            texture = model.textures.get(f'layer{i}')
            if texture is None:
               break
            font.add_texture(texture, 5, 16)
            component = {"translate":font.get_translation(texture, row)}
            hardcoded = mc.data['hardcoded_tints'].get(f'layer{i}', {}).get(item)
            if hardcoded is not None:
               component["color"] = hardcoded
            # prevent color from bleeding across components
            elif i > 0 and name[0] != "" and name[0].get("color") is not None:
               name.insert(0, "")
            if i > 0:
               name.append({"translate":"tryashtar.shulker_preview.overlay"})
            name.append(component)
         if len(name) == 0:
            print(f'{item} has no layers?')
         elif len(name) == 1:
            name = json.dumps(name[0], separators=(',', ':'))
         else:
            name = json.dumps(name, separators=(',', ':'))
         lines.append(f'{if_item} run summon marker ~ ~ ~ {{Tags:["tryashtar.shulker_preview"],CustomName:\'{name}\'}}')
      if not handled and any(x.resource == 'minecraft:block/cube_all' for x in model.parents):
         texture = model.textures.get('all')
         font.add_texture(texture, 5, 16)
         lines.append(f'{if_item} run summon marker ~ ~ ~ {{Tags:["tryashtar.shulker_preview"],CustomName:\'{{"translate":"{font.get_translation(texture, row)}","color":"#0007fc"}}\'}}')
      if not handled:
         print(f'Unhandled item {item}')
      dura = mc.data['durability'].get(item)
      if dura is not None:
         durability = True
         lines.append(f'{if_item} run scoreboard players set #max shulker_preview {dura}')
   if durability:
      lines.extend([
         f'execute store result score #durability shulker_preview run data get storage tryashtar.shulker_preview:data item.tag.Damage',
         f'execute if data storage tryashtar.shulker_preview:data item.tag.Damage run function tryashtar.shulker_preview:row_{row}/overlay/durability'
      ])
   return lines

main()
