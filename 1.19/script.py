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
   data = urlopen(f'https://raw.githubusercontent.com/misode/mcmeta/{version}-summary/registries/data.json').read()
   item_registry = json.loads(data)["item"]
   jar_path = find_version_jar()
   mc = Minecraft(jar_path, item_registry, read_json('data.json'))
   font = FontAbstraction(3)
   font.add_texture('tryashtar.shulker_preview:missingno')
   print('Generating functions...')
   mc.generate_functions(
      font,
      'datapack'
   )
   shutil.make_archive("Shulker Preview Data Pack (1.19)", 'zip', "datapack")
   shutil.make_archive("Shulker Preview Resource Pack (1.19)", 'zip', "resourcepack")

   # to restore:
   # - write font and lang json files
   #   - negative spaces should be created when needed
   # - numbers
   #   - create from actual textures and draw including shadows
   # - tooltip preview
   #   - possibly create from existing textures
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

class FontAbstraction:
   def __init__(self, rows):
      self.current_char = '\u0900'
      self.characters = {}
      self.translations = {}
      self.textures = []
      self.rows = rows
      for i in range(0, self.rows):
         self.characters[i] = {}
         self.translations[i] = {}

   def next_char(self):
      i=ord(self.current_char)
      i+=1
      if i>=0x600 and i<=0x6ff:
         i=0x700
      return chr(i)

   def add_texture(self, texture):
      if texture in self.textures:
         return
      self.textures.append(texture)
      for i in range(0, self.rows):
         self.characters[i][texture] = self.next_char()
         translation = remove_namespace(texture).replace('/', '.')
         self.translations[i][texture] = f'tryashtar.shulker_preview.{translation}.{i}'

   def get_character(self, texture, row):
      return self.characters[row][texture]

   def get_translation(self, texture, row):
      return self.translations[row][texture]


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

   def generate_functions(self, font, path):
      for row in range(0, font.rows):
         process_item = Function(f'tryashtar.shulker_preview:row_{row}/process_item', [
            '# get the length of this item and call the appropriate function',
            'execute store result score #length shulker_preview run data get storage tryashtar.shulker_preview:data item.id'
         ])
         lengths = list(self.length_dict.keys())
         lengths.sort()
         for length in range(0,100):
            subfunction = Function(f'tryashtar.shulker_preview:row_{row}/process_item/length_{length}', [])
            if length in lengths:
               process_item.lines.append(f'execute if score #length shulker_preview matches {length} run function {subfunction.resource}')
               subfunction.lines.extend(self.generate_item_lines(self.length_dict[length], row, font))
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

   def generate_item_lines(self, items, row, font):
      lines = []
      for item in items:
         if_item=f'execute if data storage tryashtar.shulker_preview:data item{{id:"{add_namespace(item)}"}}'
         model = self.get_model(f'minecraft:item/{item}')
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
               font.add_texture(texture)
               component = {"translate":font.get_translation(texture, row)}
               hardcoded = self.hardcoded_tints.get(f'layer{i}', {}).get(item)
               if hardcoded is not None:
                  component["color"] = hardcoded
               # prevent color from bleeding across components
               elif i > 0 and name[0] != "" and name[0].get("color") is not None:
                  name.insert(0, "")
               name.append(component)
            if len(name) == 1:
               name = json.dumps(name[0], separators=(',', ':'))
            else:
               name = json.dumps(name, separators=(',', ':'))
            lines.append(f'{if_item} run summon marker ~ ~ ~ {{Tags:["tryashtar.shulker_preview"],CustomName:\'{name}\'}}')
         elif any(x.resource == 'minecraft:block/block' for x in model.parents):
            print(item)
         else:
            print(f'Unhandled item {item}')
      return lines

   def get_model(self, resource):
      if resource in self.models:
         return self.models[resource]
      return self.load_model('assets/' + resource_to_path(resource, 'models', 'json'))

   def load_model(self, path):
      resource = path_to_resource(path)
      if resource in self.models:
         return self.models[resource]
      data = json.loads(self.zip.read(path).decode('utf-8'))
      model = Model(resource, data)
      self.models[resource] = model
      current_model = model
      # extract and load overrides
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
            if parent_path in self.zip.namelist():
               parent = self.load_model(parent_path)
               model.parents.append(parent)
               current_model = parent
               continue
         break
      # when referencing other textures, replace the reference
      # when expecting a texture from a child model, just remove it
      for k,v in list(model.textures.items()):
         if v.startswith('#'):
            if v[1:] in model.textures:
               model.textures[k] = model.textures[v[1:]]
            else:
               del model.textures[k]
      for k,v in model.textures.items():
         if not v.startswith('minecraft:'):
            model.textures[k] = 'minecraft:'+v
      for v in model.textures.values():
         if v not in self.textures:
            self.textures.append(v)
      return model

class Model:
   def __init__(self, resource, data):
      self.resource = resource
      self.data = data
      self.parents = []
      self.overrides = []
      self.textures = {}

def remove_namespace(rc):
   try:
      colon = rc.index(':')
      return rc[colon+1:]
   except ValueError:
      return rc

def add_namespace(rc):
   if ':' in rc:
      return rc
   return 'minecraft:'+rc

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

main()
