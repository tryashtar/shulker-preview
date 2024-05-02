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
   char_cache = {'prev':0,'generated':{},'external':{},'spaces':{}}
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
   char_cache['generated']['tryashtar.shulker_preview:missingno'] = new_sprite(char_cache)
   special_render_tag = []
   hardcoded_items = {
      'grass_colored': {"vine":0x48b518,"lily_pad":0x71c35c,"short_grass":0x7bbd6b,"fern":0x7bbd6b,"tall_grass":0x7bbd6b,"large_fern":0x7bbd6b},
      'spawn_eggs': {f'{k}_spawn_egg':v for k,v in {"bogged":(9084018,3231003),"armadillo":(11366765,0x824848),"wither":(0x141414,5075616),"snow_golem":(14283506,8496292),"sniffer":(8855049,2468720),"iron_golem":(14405058,7643954),"ender_dragon":(0x1C1C1C,14711290),"camel":(16565097,13341495),"allay":(56063,44543),"axolotl":(16499171,10890612),"bat":(4996656,986895),"bee":(15582019,4400155),"blaze":(16167425,16775294),"breeze":(11506911,9529055),"cat":(15714446,9794134),"cave_spider":(803406,11013646),"chicken":(10592673,16711680),"cod":(12691306,15058059),"cow":(4470310,10592673),"creeper":(894731,0),"dolphin":(2243405,16382457),"donkey":(5457209,8811878),"drowned":(9433559,7969893),"elder_guardian":(13552826,7632531),"enderman":(1447446,0),"endermite":(1447446,7237230),"evoker":(9804699,1973274),"frog":(13661252,0xFFC77C),"fox":(14005919,13396256),"ghast":(16382457,12369084),"glow_squid":(611926,8778172),"goat":(10851452,5589310),"guardian":(5931634,15826224),"hoglin":(13004373,6251620),"horse":(12623485,15656192),"husk":(7958625,15125652),"llama":(12623485,10051392),"magma_cube":(3407872,16579584),"mooshroom":(10489616,12040119),"mule":(1769984,5321501),"ocelot":(15720061,5653556),"panda":(15198183,1776418),"parrot":(894731,16711680),"phantom":(4411786,8978176),"pig":(15771042,14377823),"piglin":(10051392,16380836),"piglin_brute":(5843472,16380836),"pillager":(5451574,9804699),"polar_bear":(0xEEEEDE,14014157),"pufferfish":(16167425,3654642),"rabbit":(10051392,7555121),"ravager":(7697520,5984329),"salmon":(10489616,951412),"sheep":(15198183,16758197),"shulker":(9725844,5060690),"silverfish":(7237230,3158064),"skeleton":(12698049,4802889),"skeleton_horse":(6842447,15066584),"slime":(5349438,8306542),"spider":(3419431,11013646),"squid":(2243405,7375001),"stray":(6387319,14543594),"strider":(10236982,5065037),"tadpole":(7164733,1444352),"trader_llama":(15377456,4547222),"tropical_fish":(15690005,16775663),"turtle":(15198183,44975),"vex":(8032420,15265265),"villager":(5651507,12422002),"vindicator":(9804699,2580065),"wandering_trader":(4547222,15377456),"warden":(1001033,3790560),"witch":(3407872,5349438),"wither_skeleton":(1315860,4672845),"wolf":(14144467,13545366),"zoglin":(13004373,15132390),"zombie":(44975,7969893),"zombie_horse":(3232308,9945732),"zombified_piglin":(15373203,5009705),"zombie_villager":(5651507,7969893)}.items()},
      'colored': ["leather_helmet","leather_chestplate","leather_leggings","leather_boots","leather_horse_armor","potion","splash_potion","lingering_potion","firework_star","filled_map","tipped_arrow"]
   }
   special_render_functions = {k:[[],[],[]] for k in hardcoded_items.keys()}
   for name,values in hardcoded_items.items():
      values = values.keys() if isinstance(values, dict) else values
      write_json({"values":list(sorted(values))}, f'datapack/data/tryashtar.shulker_preview/tags/items/special_render/{name}.json')
      special_render_tag.append(f'#tryashtar.shulker_preview:special_render/{name}')
   with zipfile.ZipFile(jar_path, 'r') as jar:
      def load_textures(item, model):
         result = {'base':[],'overrides':[]}
         if model.get('generated', False):
            layer = 0
            while f'layer{layer}' in model['textures']:
               texture = model['textures'][f'layer{layer}']
               chars = new_sprite(char_cache)
               char_cache['generated'][with_namespace(texture)] = chars
               result['base'].append(chars)
               layer += 1
         else:
            block_image = f'../../block images/{item}.png'
            if os.path.exists(block_image):
               chars = new_sprite(char_cache)
               char_cache['external'][block_image] = chars
               result['base'].append(chars)
         for override in model['overrides']:
            predicate = override['predicate']
            if not ('pulling' in predicate or 'pull' in predicate or 'brushing' in predicate or 'time' in predicate or 'angle' in predicate or 'cast' in predicate or 'tooting' in predicate or 'blocking' in predicate or 'trim_type' in predicate):
               result['overrides'].append(load_textures(item, get_model(jar, model_cache, override['model']))['base'])
         return result

      for item in item_list:
         model = get_model(jar, model_cache, f'item/{item}')
         textures = load_textures(item, model)
         if len(textures['base']) > 0:
            if item in hardcoded_items['grass_colored']:
               functions = special_render_functions['grass_colored']
               translations = add_normal_translations(item, textures['base'], lang, next_slot)
               color = hardcoded_items['grass_colored'][item]
               for row,lines in enumerate(functions):
                  lines.append(f'execute if items entity 7368756c-6b65-7220-7072-657669657721 contents {item} run data modify storage tryashtar.shulker_preview:data tooltip append value \'{{"translate":"{translations[row]}","color":"{color_hex(color)}"}}\'')
            elif item.endswith('_spawn_egg'):
               functions = special_render_functions['spawn_eggs']
               translations = add_layered_translations('spawn_egg', textures['base'], lang, next_slot)
               color = hardcoded_items['spawn_eggs'][item]
               for row,lines in enumerate(functions):
                  lines.append(f'execute if items entity 7368756c-6b65-7220-7072-657669657721 contents {item} run data modify storage tryashtar.shulker_preview:data tooltip append value \'[{{"translate":"{translations[row][0]}","color":"{color_hex(color[0])}"}},{{"translate":"{translations[row][1]}","color":"{color_hex(color[1])}"}},{{"translate":"tryashtar"}}]\'')
            else:
               add_normal_translations(item, textures['base'], lang, next_slot)
         else:
            print(f'WARNING: {item} not handled!')
         
   grid = create_grid(char_cache['external'])
   for texture,sprites in char_cache['generated'].items():
      append_sprites(font, texture, {'rows':[[x] for x in sprites['rows']], 'negative':[sprites['negative']]})
   append_sprites(font, 'tryashtar.shulker_preview:block_sheet', {'rows':[[''.join(['\u0000' if entry is None else entry[1]['rows'][row] for entry in grid_row]) for grid_row in grid] for row in range(0, 3)], 'negative':[''.join(['\u0000' if entry is None else entry[1]['negative'] for entry in grid_row]) for grid_row in grid]})
   for row in range(0, 3):
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
      special_render = []
      for name in hardcoded_items:
         special_render.append(f'execute if items entity 7368756c-6b65-7220-7072-657669657721 #tryashtar.shulker_preview:special_render/{name} run function tryashtar.shulker_preview:row_{row}/special_render/{name}')
      write_lines(process_item, f'datapack/data/tryashtar.shulker_preview/functions/row_{row}/process_item.mcfunction')
      write_lines(simple_render, f'datapack/data/tryashtar.shulker_preview/functions/row_{row}/simple_render.mcfunction')
      write_lines(special_render, f'datapack/data/tryashtar.shulker_preview/functions/row_{row}/special_render.mcfunction')
   grid_image = create_image(grid, 64)
   grid_image.save('resourcepack/assets/tryashtar.shulker_preview/textures/block_sheet.png', 'PNG')
   write_json(lang, 'resourcepack/assets/tryashtar.shulker_preview/lang/en_us.json')
   write_json({"providers":font}, 'resourcepack/assets/tryashtar.shulker_preview/font/preview.json')
   write_json({"values":special_render_tag}, 'datapack/data/tryashtar.shulker_preview/tags/items/special_render.json')   

def color_hex(int_color):
   return f'#{format(int_color, '06x')}'

def add_layered_translations(name, textures, lang, next_slot):
   result = []
   for row in range(0, 3):
      sub = []
      for layernum,layer in enumerate(textures):
         key = f'tryashtar.shulker_preview.layer.{name}.{layernum}.{row}'
         text = layer['rows'][row] + layer['negative']
         if layernum == len(textures) - 1:
            text += next_slot
         lang[key] = text
         sub.append(key)
      result.append(sub)
   return result

def add_normal_translations(item, textures, lang, next_slot):
   result = []
   for row in range(0, 3):
      key = f'tryashtar.shulker_preview.item.{with_namespace(item)}.{row}'
      lang[key] = ''.join([layer['rows'][row] + layer['negative'] for layer in textures]) + next_slot
      result.append(key)
   return result

def append_sprites(font, texture, sprite_chars):
   for row in range(0, 3):
      font.append({"type":"bitmap","file":f'{texture}.png',"ascent":5 + (row * -18),"height":16,"chars":sprite_chars['rows'][row]})
   font.append({"type":"bitmap","file":f'{texture}.png',"ascent":-32768,"height":-16,"chars":sprite_chars['negative']})

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
      path = icon[0]
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

def new_sprite(cache):
   return {
      'rows': [next_char(cache), next_char(cache), next_char(cache)],
      'negative': next_char(cache)
   }

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
