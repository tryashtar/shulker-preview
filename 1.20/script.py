import os
import io
import json
import zipfile
import numpy
import math
import unicodedata
import urllib.request
import PIL.Image

def main():
   target_version = '1.20.5'
   version_folder = os.path.expanduser('~/.minecraft/versions')
   item_list = json.loads(urllib.request.urlopen(f'https://raw.githubusercontent.com/misode/mcmeta/{target_version}-registries/item/data.json').read())
   item_list.remove('air')
   jar_path = os.path.join(version_folder, target_version, f'{target_version}.jar')
   space_provider = {}
   font = [{"type":"space","advances":space_provider}]
   model_cache = {}
   char_cache = {'prev':0,'items':{},'spaces':{}}
   external_images = {}
   negative_tooltip = get_space(space_provider, char_cache, -169)
   empty_slot = get_space(space_provider, char_cache, 18)
   next_slot = get_space(space_provider, char_cache, 15)
   row_end = get_space(space_provider, char_cache, -162)
   lang = {"tryashtar.shulker_preview.translate":"%2$s"}
   tooltip1 = next_char(char_cache)
   tooltip2 = next_char(char_cache)
   font.append({"type":"bitmap","file":"tryashtar.shulker_preview:shulker_tooltip.png","ascent":23,"height":78,"chars":[tooltip1]})
   font.append({"type":"bitmap","file":"tryashtar.shulker_preview:shulker_tooltip_header.png","ascent":23,"height":78,"chars":[tooltip2]})
   lang['tryashtar.shulker_preview.shulker_tooltip'] = tooltip1 + negative_tooltip
   lang['tryashtar.shulker_preview.shulker_tooltip_header'] = tooltip2 + negative_tooltip
   lang['tryashtar.shulker_preview.empty_slot'] = empty_slot
   lang['tryashtar.shulker_preview.row_end'] = row_end
   unknown_chars = get_chars(font, char_cache, 'tryashtar.shulker_preview:missingno')
   for row,char in enumerate(unknown_chars['rows']):
      lang[f'tryashtar.shulker_preview.missingno.{row}'] = char + unknown_chars['negative'] + next_slot
   grass_colors = {"vine":"#48b518","lily_pad":"#71c35c","short_grass":"#7bbd6b","fern":"#7bbd6b","tall_grass":"#7bbd6b","large_fern":"#7bbd6b"}
   write_json({"values":list(sorted(grass_colors.keys()))}, 'datapack/data/tryashtar.shulker_preview/tags/items/special_render/grass_colored.json')
   special_render = ['#tryashtar.shulker_preview:grass_colored']
   with zipfile.ZipFile(jar_path, 'r') as jar:
      def get_translations(item):
         model = get_model(jar, model_cache, f'item/{item}')
         if model.get('generated', False):
            translations = [''] * 3
            layer = 0
            while f'layer{layer}' in model['textures']:
               texture = model['textures'][f'layer{layer}']
               chars = get_chars(font, char_cache, texture)
               for row,char in enumerate(chars['rows']):
                  translations[row] += char + chars['negative']
               layer += 1
            for row,char in enumerate(translations):
               lang[f'tryashtar.shulker_preview.item.minecraft:{item}.{row}'] = char + next_slot
         else:
            block_image = f'../../block images/{item}.png'
            if os.path.exists(block_image):
               external_images[item] = block_image
            else:
               print(f'WARNING: {item} not handled!')

      for item in item_list:
         translations = get_translations(item)
         
   grid = create_grid(external_images)
   for row in range(0, 3):
      grid_chars = []
      for grid_row in grid:
         string = ""
         for entry in grid_row:
            if entry is None:
               string += '\u0000'
            else:
               char = next_char(char_cache)
               string += char
         grid_chars.append(string)
      font.append({"type":"bitmap","file":'tryashtar.shulker_preview:block_sheet.png',"ascent":5 + (row * -18),"height":16,"chars":grid_chars})
      process_item = [
         'data modify entity 7368756c-6b65-7220-7072-657669657721 Item set from storage tryashtar.shulker_preview:data item',
         f'execute if items entity 7368756c-6b65-7220-7072-657669657721 contents #tryashtar.shulker_preview:special_render run function tryashtar.shulker_preview:row_{row}/special_render',
         f'execute unless items entity 7368756c-6b65-7220-7072-657669657721 contents #tryashtar.shulker_preview:special_render run function tryashtar.shulker_preview:row_{row}/simple_render with storage tryashtar.shulker_preview:data item',
         f'execute if items entity 7368756c-6b65-7220-7072-657669657721 contents *[damage~{{damage:{{min:1}}}},max_damage] run function tryashtar.shulker_preview:row_{row}/overlay/durability',
         f'execute if items entity 7368756c-6b65-7220-7072-657669657721 contents *[count~{{min:2}}] run function tryashtar.shulker_preview:row_{row}/overlay/count'
      ]
      simple_render = [
         f'$data modify storage tryashtar.shulker_preview:data tooltip append value \'{{"translate":"tryashtar.shulker_preview.item.$(id).{row}","fallback":"%s","with":[{{"translate":"tryashtar.shulker_preview.missingno.{row}"}}]}}\''
      ]
      special_render = [

      ]
      write_lines(process_item, f'datapack/data/tryashtar.shulker_preview/functions/row_{row}/process_item.mcfunction')
      write_lines(simple_render, f'datapack/data/tryashtar.shulker_preview/functions/row_{row}/simple_render.mcfunction')
      write_lines(special_render, f'datapack/data/tryashtar.shulker_preview/functions/row_{row}/special_render.mcfunction')
   grid_image = create_image(grid, 64)
   grid_image.save('resourcepack/assets/tryashtar.shulker_preview/textures/block_sheet.png', 'PNG')
   write_json(lang, 'resourcepack/assets/tryashtar.shulker_preview/lang/en_us.json')
   write_json({"providers":font}, 'resourcepack/assets/tryashtar.shulker_preview/font/preview.json')
   write_json({"values":special_render}, 'datapack/data/tryashtar.shulker_preview/tags/items/special_render.json')

def get_translation(item):
   

def create_grid(external_images):
   size = get_dimensions(len(external_images))
   ordered = list(external_images.items())
   ordered.extend([None] * (size[0] * size[1] - len(ordered)))
   result = numpy.empty(len(ordered), dtype=object)
   result[:] = ordered
   return numpy.reshape(result, (size[1], size[0]))

def get_dimensions(area):
   width = math.ceil(math.sqrt(area))
   height = width
   if width * (height - 1) >= area:
      height -= 1
   return (width, height)

def create_image(grid, icon_size):
   dim = grid.shape
   sheet = PIL.Image.new('RGBA', (dim[1] * icon_size, dim[0] * icon_size))
   for pos,icon in numpy.ndenumerate(grid):
      if icon is None:
         continue
      x = pos[1] * icon_size
      y = pos[0] * icon_size
      path = icon[1]
      with PIL.Image.open(path).convert('RGBA') as sprite:
         for corner in (0, icon_size - 1):
            r,g,b,a = sprite.getpixel((corner, corner))
            if a == 0:
               r,g,b = (139, 139, 139)
            sprite.putpixel((corner, corner), (r, g, b, max(a, 18)))
         sheet.paste(sprite, (x, y, x + icon_size, y + icon_size))
   return sheet

def get_space(provider, cache, size):
   if size not in cache['spaces']:
      char = next_char(cache)
      provider[char] = size
      cache['spaces'][size] = char
   return cache['spaces'][size]

def get_chars(font, cache, texture):
   texture = with_namespace(texture)
   if texture not in cache['items']:
      rows = []
      for row in range(0, 3):
         char = next_char(cache)
         rows.append(char)
         font.append({"type":"bitmap","file":f'{texture}.png',"ascent":5 + (row * -18),"height":16,"chars":[char]})
      negative = next_char(cache)
      font.append({"type":"bitmap","file":f'{texture}.png',"ascent":-32768,"height":-16,"chars":[negative]})
      cache['items'][texture] = {
         'rows': rows,
         'negative': negative
      }
   return cache['items'][texture]

def next_char(cache):
   char = cache['prev'] + 1
   for low, high in [(0xd800, 0xdbff), (0xdc00, 0xdfff), (0x05c8, 0x05d2), (0x05e8, 0x05ff), (0x061b, 0x0620), (0x0648, 0x065f), (0x066d, 0x066f), (0x070b, 0x0710), (0x072d, 0x072f), (0x074b, 0x074f), (0x07a4, 0x07a5), (0x07b1, 0x07c2), (0x07f4, 0x07f5), (0x07fa, 0x07fc), (0x07fe, 0x0800), (0x082e, 0x0832), (0x083c, 0x0842), (0x0856, 0x0858), (0x085c, 0x0862), (0x0868, 0x0897), (0x08a0, 0x08a2), (0x08b2, 0x08b8), (0x08c5, 0x08c9), (0xfb34, 0xfb48), (0xfbbf, 0xfbd5), (0xfd8d, 0xfd94), (0xfdc5, 0xfdce), (0xfdf0, 0xfdf2), (0xfe72, 0xfe78), (0xfefa, 0xfefe)]:
      if low <= char <= high:
         char = high + 1
   while char in [0x0000, 0x000a, 0x00a7, 0x0590, 0x05be, 0x05c0, 0x05c3, 0x05c6, 0x0608, 0x060b, 0x060d, 0x0712, 0x081a, 0x0824, 0x0828, 0x200f, 0xfb1d, 0xfb1f] or unicodedata.bidirectional(chr(char)) in ['AL', 'R']:
      char += 1
   cache['prev'] = char
   return chr(char)

def get_model(jar, cache, identifier):
   identifier = with_namespace(identifier)
   namespace, path = identifier.split(':')
   model_path = f'assets/{namespace}/models/{path}.json'
   with io.TextIOWrapper(jar.open(model_path), encoding='utf-8') as model_file:
      model = json.load(model_file)
      if 'textures' not in model:
         model['textures'] = {}
      if 'overrides' not in model:
         model['overrides'] = []
      for override in list(model['overrides']):
         predicate = override['predicate']
         if 'pulling' in predicate or 'pull' in predicate or 'brushing' in predicate or 'time' in predicate or 'angle' in predicate or 'cast' in predicate or 'tooting' in predicate or 'blocking' in predicate or 'trim_type' in predicate:
            model['overrides'].remove(override)
      parent = model.get('parent')
      if parent is not None:
         parent = with_namespace(parent)
         if parent == 'minecraft:builtin/generated':
            model['generated'] = True
         elif not parent.startswith('minecraft:builtin/'):
            parent = get_model(jar, cache, parent)
            if parent.get('generated', False):
               model['generated'] = True
            for key,value in parent['textures'].items():
               if key not in model['textures']:
                  model['textures'][key] = value
      cache[identifier] = model
      return model

def with_namespace(identifier):
   if ':' in identifier:
      return identifier
   return f'minecraft:{identifier}'

def write_json(data, path):
   with open(path, 'w', encoding='utf-8') as file:
      json.dump(data, file, indent=3, ensure_ascii=True)

def write_lines(lines, path):
   with open(path, 'w', encoding='utf-8') as file:
      for line in lines:
         file.write(line + '\n')

if __name__ == '__main__':
   main()
