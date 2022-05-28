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
   # - numbers
   #   - create from actual textures and draw including shadows
   # - durability
   #   - still using texture grid for this, need a way to create chars/translations
   #   - how to reference function if it's created in generate_functions but used in generate_item_lines?
   # - potion/arrow/map overlays
   # - banner/shield overlays
   #   - need to use old method of generating grid from screenshots, doubt shaders can do this one
   # - dyed armor color
   #   - still needs overlays
   # - all the overrides like light blocks
   # - generate test command

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
      # create the tooltip characters
      # the tooltip is made by slicing the vanilla texture into rows and assembling them
      tooltip_neg = self.next_char()
      tooltip_1 = self.next_char()
      tooltip_2 = self.next_char()
      tooltip_3 = self.next_char()
      split_2 = ['\u0000'] * 32
      split_3 = ['\u0000'] * 32
      split_2[8] = tooltip_2
      split_3[20] = tooltip_3
      font = [
         # negative version, used to bring the cursor back to draw the next row
         {"type": "bitmap", "file": "minecraft:gui/container/shulker_box.png", "ascent": -32768, "height": -260, "chars": [tooltip_neg]},
         # top: the first two rows of slots and most of the third
         # we can only slice by whole numbers, and a slice any larger would be too big
         {"type": "bitmap", "file": "minecraft:gui/container/shulker_box.png", "ascent": 23, "height": 64, "chars": [tooltip_1, "\u0000", "\u0000", "\u0000"]},
         # middle: the rest of the third row
         {"type": "bitmap", "file": "minecraft:gui/container/shulker_box.png", "ascent": 23-64, "height": 8, "chars": split_2},
         # bottom: the very bottom of the tooltip texture
         {"type": "bitmap", "file": "minecraft:gui/container/shulker_box.png", "ascent": 23-64-8, "height": 8, "chars": split_3}
      ]
      # start by moving back 6 pixels to fully cover the vanilla tooltip
      # then each row and negative in turn
      # then forward 7 pixels, aligning the first item to draw with the first slot
      lang["tryashtar.shulker_preview.shulker_tooltip"] = self.get_space(-6) + tooltip_1 + tooltip_neg + tooltip_2 + tooltip_neg + tooltip_3 + tooltip_neg + self.get_space(7)
      for s, ch in self.spaces.items():
         font.append({"type": "bitmap", "file": "tryashtar.shulker_preview:pixel.png", "ascent": -32768, "height": s, "chars": [ch]})
      for t, data in self.textures.items():
         for i in range(0, self.rows):
            lang[self.translations[i][t]] = self.characters[i][t] + self.negatives[t]
            font.append({"type": "bitmap", "file": t + '.png', "ascent": data['ascent'] - (18 * i), "height": data['height'], "chars": [self.characters[i][t]]})
         font.append({"type": "bitmap", "file": t + '.png', "ascent": -32768, "height": -data['height'], "chars": [self.negatives[t]]})
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
      self.hardcoded_tints = data['hardcoded_tints']
      for k,v in data['spawn_eggs'].items():
         self.hardcoded_tints['layer0'][k] = color_hex(v[0])
         self.hardcoded_tints['layer1'][k] = color_hex(v[1])
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
      process_item = Function(f'tryashtar.shulker_preview:row_{row}/process_item', [
         '# get the length of this item and call the appropriate function',
         'execute store result score #length shulker_preview run data get storage tryashtar.shulker_preview:data item.id'
      ])
      lengths = list(mc.length_dict.keys())
      lengths.sort()
      for length in range(0,100):
         subfunction = Function(f'tryashtar.shulker_preview:row_{row}/process_item/length_{length}', [])
         if length in lengths:
            process_item.lines.append(f'execute if score #length shulker_preview matches {length} run function {subfunction.resource}')
            subfunction.lines.extend(generate_item_lines(mc, mc.length_dict[length], row, font))
            subfunction.save(path)
         else:
            fpath = os.path.join(path, subfunction.file_path)
            if os.path.exists(fpath):
               os.remove(fpath)
      count = Function(f'tryashtar.shulker_preview:row_{row}/overlay/count', ['# create an entity that draws item counts'])
      for i in range(2, 65):
         n = str(i) if i < 64 else f"{i}.."
         count.lines.append(f'execute if score #count shulker_preview matches {n} run summon marker ~ ~0.9 ~ {{Tags:["tryashtar.shulker_preview"],CustomName:\'{{"translate":"tryashtar.shulker_preview.number.{i}.{row}"}}\'}}')
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

def generate_item_lines(mc, items, row, font):
   lines = []
   for item in items:
      if_item=f'execute if data storage tryashtar.shulker_preview:data item{{id:"{add_namespace(item)}"}}'
      model = mc.get_model(f'minecraft:item/{item}')
      if len(model.overrides) > 0:
         if item in []:
            pass
         else:
            print(f'Unhandled item {item}')
         # must be hardcoded
         pass
      elif any(x.resource == 'minecraft:item/generated' for x in model.parents):
         # this is a normal layered item, generate as such
         name = []
         for i in range(0, 99):
            texture = model.textures.get(f'layer{i}')
            if texture is None:
               break
            font.add_texture(texture, 5, 16)
            component = {"translate":font.get_translation(texture, row)}
            hardcoded = mc.hardcoded_tints.get(f'layer{i}', {}).get(item)
            if hardcoded is not None:
               component["color"] = hardcoded
            # prevent color from bleeding across components
            elif i > 0 and name[0] != "" and name[0].get("color") is not None:
               name.insert(0, "")
            name.append(component)
         if len(name) == 0:
            print(f'{item} has no layers?')
         elif len(name) == 1:
            name = json.dumps(name[0], separators=(',', ':'))
         else:
            name = json.dumps(name, separators=(',', ':'))
         lines.append(f'{if_item} run summon marker ~ ~ ~ {{Tags:["tryashtar.shulker_preview"],CustomName:\'{name}\'}}')
      elif any(x.resource == 'minecraft:block/block' for x in model.parents):
         print(item)
      else:
         print(f'Unhandled item {item}')
   return lines

main()
