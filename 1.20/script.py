import os
import io
import json
import zipfile
import numpy
import math
import unicodedata
import urllib.request
import PIL.Image
import shutil
import colorsys

def main():
   target_version = '1.20.5'
   version_folder = os.path.expanduser('~/.minecraft/versions')
   item_list = download_json(f'https://raw.githubusercontent.com/misode/mcmeta/{target_version}-registries/item/data.json', f'../cache/items-{target_version}.json')
   banner_list = download_json(f'https://raw.githubusercontent.com/misode/mcmeta/{target_version}-registries/banner_pattern/data.json', f'../cache/banners-{target_version}.json')
   pot_list = download_json(f'https://raw.githubusercontent.com/misode/mcmeta/{target_version}-registries/decorated_pot_patterns/data.json', f'../cache/pots-{target_version}.json')
   item_list.remove('air')
   jar_path = os.path.join(version_folder, target_version, f'{target_version}.jar')
   space_provider = {}
   font = [{"type":"space","advances":space_provider}]
   model_cache = {}
   char_cache = {'prev':0,'generated':{},'external':{},'spaces':{}}
   small_space = get_space(space_provider, char_cache, 1)
   two_space = get_space(space_provider, char_cache, 2)
   one_space = get_space(space_provider, char_cache, 3)
   tooltip_push_fwd = get_space(space_provider, char_cache, 8)
   almost_next_slot = get_space(space_provider, char_cache, 14)
   next_slot = get_space(space_provider, char_cache, 15)
   empty_slot = get_space(space_provider, char_cache, 18)
   back_a_tad = get_space(space_provider, char_cache, -1)
   overlay_offset = get_space(space_provider, char_cache, -3)
   tooltip_push_back = get_space(space_provider, char_cache, -4)
   num_back6 = get_space(space_provider, char_cache, -6)
   one_count_overlay = get_space(space_provider, char_cache, -7)
   dura_overlay = get_space(space_provider, char_cache, -16)
   banner_overlay = get_space(space_provider, char_cache, -17)
   row_end = get_space(space_provider, char_cache, -162)
   lang = {"tryashtar.shulker_preview.translate":"%2$s"}
   for tex, tip, bottom in [('shulker_box', 'shulker', 20), ('generic_54', 'ender', 27)]:
      ascent = 8
      slices = [{'height':8,'range':[0]},{'height':8,'range':[2,3,4,5,6,7,8,bottom]}]
      text = ''
      for section in slices:
         for include in section['range']:
            positive = ['\u0000'] * (256 // section['height'])
            negative = ['\u0000'] * (256 // section['height'])
            pos = next_char(char_cache)
            neg = next_char(char_cache)
            positive[include] = pos
            negative[include] = neg
            font.append({"type": "bitmap", "file": f"minecraft:gui/container/{tex}.png", "ascent": ascent, "height": section['height'], "chars": positive})
            font.append({"type": "bitmap", "file": f"minecraft:gui/container/{tex}.png", "ascent": -32768, "height": -section['height'], "chars": negative})
            ascent -= section['height']
            text += pos + neg + overlay_offset
      lang[f"tryashtar.shulker_preview.{tip}_tooltip"] = tooltip_push_back + text + tooltip_push_fwd
   lang['tryashtar.shulker_preview.empty_slot'] = empty_slot
   lang['tryashtar.shulker_preview.row_end'] = row_end
   lang['tryashtar.shulker_preview.overlay'] = back_a_tad
   lang['tryashtar.shulker_preview.overlay_done'] = small_space
   char_cache['generated']['tryashtar.shulker_preview:missingno'] = new_sprite(char_cache, True)
   special_render_tag = ['#tryashtar.shulker_preview:special_render/overrides']
   override_items = {}
   hardcoded_items = {
      'grass_colored': {"vine":0x48b518,"lily_pad":0x71c35c,"short_grass":0x7bbd6b,"fern":0x7bbd6b,"tall_grass":0x7bbd6b,"large_fern":0x7bbd6b},
      'spawn_eggs': {f'{k}_spawn_egg':v for k,v in {"bogged":(9084018,3231003),"armadillo":(11366765,0x824848),"wither":(0x141414,5075616),"snow_golem":(14283506,8496292),"sniffer":(8855049,2468720),"iron_golem":(14405058,7643954),"ender_dragon":(0x1C1C1C,14711290),"camel":(16565097,13341495),"allay":(56063,44543),"axolotl":(16499171,10890612),"bat":(4996656,986895),"bee":(15582019,4400155),"blaze":(16167425,16775294),"breeze":(11506911,9529055),"cat":(15714446,9794134),"cave_spider":(803406,11013646),"chicken":(10592673,16711680),"cod":(12691306,15058059),"cow":(4470310,10592673),"creeper":(894731,0),"dolphin":(2243405,16382457),"donkey":(5457209,8811878),"drowned":(9433559,7969893),"elder_guardian":(13552826,7632531),"enderman":(1447446,0),"endermite":(1447446,7237230),"evoker":(9804699,1973274),"frog":(13661252,0xFFC77C),"fox":(14005919,13396256),"ghast":(16382457,12369084),"glow_squid":(611926,8778172),"goat":(10851452,5589310),"guardian":(5931634,15826224),"hoglin":(13004373,6251620),"horse":(12623485,15656192),"husk":(7958625,15125652),"llama":(12623485,10051392),"magma_cube":(3407872,16579584),"mooshroom":(10489616,12040119),"mule":(1769984,5321501),"ocelot":(15720061,5653556),"panda":(15198183,1776418),"parrot":(894731,16711680),"phantom":(4411786,8978176),"pig":(15771042,14377823),"piglin":(10051392,16380836),"piglin_brute":(5843472,16380836),"pillager":(5451574,9804699),"polar_bear":(0xEEEEDE,14014157),"pufferfish":(16167425,3654642),"rabbit":(10051392,7555121),"ravager":(7697520,5984329),"salmon":(10489616,951412),"sheep":(15198183,16758197),"shulker":(9725844,5060690),"silverfish":(7237230,3158064),"skeleton":(12698049,4802889),"skeleton_horse":(6842447,15066584),"slime":(5349438,8306542),"spider":(3419431,11013646),"squid":(2243405,7375001),"stray":(6387319,14543594),"strider":(10236982,5065037),"tadpole":(7164733,1444352),"trader_llama":(15377456,4547222),"tropical_fish":(15690005,16775663),"turtle":(15198183,44975),"vex":(8032420,15265265),"villager":(5651507,12422002),"vindicator":(9804699,2580065),"wandering_trader":(4547222,15377456),"warden":(1001033,3790560),"witch":(3407872,5349438),"wither_skeleton":(1315860,4672845),"wolf":(14144467,13545366),"zoglin":(13004373,15132390),"zombie":(44975,7969893),"zombie_horse":(3232308,9945732),"zombified_piglin":(15373203,5009705),"zombie_villager":(5651507,7969893)}.items()}
   }
   potion_colors = {"speed":3402751,"slowness":9154528,"haste":14270531,"mining_fatigue":4866583,"strength":16762624,"instant_health":16262179,"instant_damage":11101546,"jump_boost":16646020,"nausea":5578058,"regeneration":13458603,"resistance":9520880,"fire_resistance":0xFF9900,"water_breathing":10017472,"invisibility":0xF6F6F6,"blindness":2039587,"night_vision":12779366,"hunger":5797459,"weakness":0x484D48,"poison":8889187,"wither":7561558,"health_boost":16284963,"absorption":0x2552A5,"saturation":16262179,"glowing":9740385,"levitation":0xCEFFFF,"luck":5882118,"unluck":12624973,"slow_falling":15978425,"conduit_power":1950417,"dolphins_grace":8954814,"bad_omen":745784,"hero_of_the_village":0x44FF44,"darkness":2696993,"trial_omen":0x16A6A6,"raid_omen":14565464,"wind_charged":12438015,"weaving":7891290,"oozing":10092451,"infested":9214860}
   for name in potion_colors:
      color = potion_colors[name]
      potion_colors[name] = ((color//256//256)%256, (color//256)%256, color%256, 1)
   potion_contents = {"water":{},"mundane":{},"thick":{},"awkward":{},"night_vision":{"night_vision":1},"long_night_vision":{"night_vision":1},"invisibility":{"invisibility":1},"long_invisibility":{"invisibility":1},"leaping":{"jump_boost":1},"long_leaping":{"jump_boost":1},"strong_leaping":{"jump_boost":2},"fire_resistance":{"fire_resistance":1},"long_fire_resistance":{"fire_resistance":1},"swiftness":{"speed":1},"long_swiftness":{"speed":1},"strong_swiftness":{"speed":2},"slowness":{"slowness":1},"long_slowness":{"slowness":1},"strong_slowness":{"slowness":4},"turtle_master":{"slowness":4,"resistance":3},"long_turtle_master":{"slowness":4,"resistance":3},"strong_turtle_master":{"slowness":6,"resistance":4},"water_breathing":{"water_breathing":1},"long_water_breathing":{"water_breathing":1},"healing":{"instant_health":1},"strong_healing":{"instant_health":2},"harming":{"instant_damage":1},"strong_harming":{"instant_damage":2},"poison":{"poison":1},"long_poison":{"poison":1},"strong_poison":{"poison":2},"regeneration":{"regeneration":1},"long_regeneration":{"regeneration":1},"strong_regeneration":{"regeneration":2},"strength":{"strength":1},"long_strength":{"strength":1},"strong_strength":{"strength":2},"weakness":{"weakness":1},"long_weakness":{"weakness":1},"luck":{"luck":1},"slow_falling":{"slow_falling":1},"long_slow_falling":{"slow_falling":1},"wind_charged":{"wind_charged":1},"weaving":{"weaving":1},"oozing":{"oozing":1},"infested":{"infested":1}}
   for name,effects in potion_contents.items():
      if name not in potion_colors:
         total = [0,0,0]
         count = 0
         for effect,level in effects.items():
            r,g,b,_ = potion_colors[effect]
            total[0] += r * level
            total[1] += g * level
            total[2] += b * level
            count += level
         potion_colors[name] = (*total, count)
   colorable_items = {"potion":["potion","splash_potion","lingering_potion","tipped_arrow"],"star":["firework_star"],"map":["filled_map"]}
   init_data = []
   for name,values in hardcoded_items.items():
      write_json({"values":list(sorted(values.keys()))}, f'datapack/data/tryashtar.shulker_preview/tags/items/special_render/{name}.json')
      special_render_tag.append(f'#tryashtar.shulker_preview:special_render/{name}')
      for item,color in values.items():
         if isinstance(color, tuple):
            init_data.append(f'"minecraft:{item}":{{base:"{color_hex(color[0])}",overlay:"{color_hex(color[1])}"}}')
         else:
            init_data.append(f'"minecraft:{item}":{{color:"{color_hex(color)}"}}')
   special_render_tag.append("#dyeable")
   for kind,items in colorable_items.items():
      if len(items) > 1:
         write_json({"values":list(sorted(items))}, f'datapack/data/tryashtar.shulker_preview/tags/items/special_render/{kind}.json')
         special_render_tag.append(f'#tryashtar.shulker_preview:special_render/{kind}')
      else:
         special_render_tag.extend(items)
   init_data = ','.join(init_data)
   all_hex = ','.join([f'"{x:02x}"' for x in range(0, 256)])
   potion_data = ','.join([f'"minecraft:{x}":[{y[0]},{y[1]},{y[2]},{y[3]}]' for x,y in potion_colors.items()])
   dye_map = {"white":"#f9fffe","orange":"#f9801d","magenta":"#c74ebd","light_blue":"#3ab3da","yellow":"#fed83d","lime":"#80c71f","pink":"#f38baa","gray":"#474f52","light_gray":"#9d9d97","cyan":"#169c9c","purple":"#8932b8","blue":"#3c44aa","brown":"#835432","green":"#5e7c16","red":"#b02e26","black":"#1d1d21"}
   dye_data = ','.join(f'{x}:"{y}"' for x,y in dye_map.items())
   write_lines([f'data modify storage tryashtar.shulker_preview:data lookups set value {{hex:[{all_hex}],dyes:{{{dye_data}}},potions:{{{potion_data}}},colors:{{{init_data}}}}}'], 'datapack/data/tryashtar.shulker_preview/functions/meta/initialize_data.mcfunction')
   trim_materials = {'amethyst':'#c98ff3','copper':'#e3826c','diamond':('#cbfff5','#15b3a1'),'emerald':'#82f6ad','gold':('#fffd90','#c29c2a'),'iron':('#c5d2d4','#a2b0b3'),'lapis':'#416e97','netherite':('#5a575a','#2e2829'),'quartz':'#f2efed','redstone':'#e62008'}
   trim_patterns = []
   with zipfile.ZipFile(jar_path, 'r') as jar:
      with io.TextIOWrapper(jar.open('data/minecraft/tags/items/dyeable.json'), encoding='utf-8') as model_file:
         vanilla_dyeables = json.load(model_file)['values']
      def load_textures(item, model):
         result = {'base':[],'overrides':[]}
         if model.get('generated', False):
            layer = 0
            while f'layer{layer}' in model['textures']:
               texture = with_namespace(model['textures'][f'layer{layer}'])
               if texture not in char_cache['generated']:
                  chars = new_sprite(char_cache, True)
                  if texture == 'minecraft:block/sculk_vein':
                     chars['anim_height'] = 4
                  char_cache['generated'][texture] = chars
               result['base'].append(char_cache['generated'][texture])
               layer += 1
         else:
            appearance_hash = calculate_appearance_hash(item, model)
            if appearance_hash in char_cache['external']:
               result['base'].append(char_cache['external'][appearance_hash][0])
            else:
               block_image = f'../../block images/{item}.png'
               if os.path.exists(block_image):
                  chars = new_sprite(char_cache, False)
                  char_cache['external'][appearance_hash] = (chars, block_image)
                  result['base'].append(chars)
         for override in model['overrides']:
            predicate = override['predicate']
            if not ('pulling' in predicate or 'pull' in predicate or 'brushing' in predicate or 'time' in predicate or 'angle' in predicate or 'cast' in predicate or 'tooting' in predicate or 'blocking' in predicate or 'trim_type' in predicate):
               result['overrides'].append((predicate, load_textures(item, get_model(jar, model_cache, override['model']))['base']))
         return result
      for item in item_list:
         model = get_model(jar, model_cache, f'item/{item}')
         textures = load_textures(item, model)
         if len(textures['base']) > 0:
            if item.endswith('_spawn_egg'):
               if item not in hardcoded_items['spawn_eggs']:
                  print(f'WARNING: {item} missing colors')
               add_layered_translations('spawn_egg', textures['base'], lang, next_slot, overlay_offset)
            elif with_namespace(item) in vanilla_dyeables:
               if item in ('leather_chestplate', 'leather_horse_armor'):
                  if len(textures['base']) < 2:
                     textures['base'].append(None)
                  textures['base'][1] = {'rows':[one_space, one_space, one_space], 'negative': ''}
               add_layered_translations(with_namespace(item), textures['base'], lang, next_slot, overlay_offset)
               if item == 'wolf_armor':
                  add_normal_translations('item', with_namespace(item), [textures['base'][0]], lang, next_slot, small_space)
            elif item in colorable_items['potion'] or item in colorable_items['map'] or item in colorable_items['star']:
               add_layered_translations(with_namespace(item), textures['base'], lang, next_slot, overlay_offset)
            else:
               add_normal_translations('item', with_namespace(item), textures['base'], lang, next_slot, small_space)
               if len(textures['overrides']) > 0:
                  override_items[item] = [x[0] for x in textures['overrides']]
                  for num,(_,override) in enumerate(textures['overrides']):
                     add_normal_translations('override', with_namespace(item) + '.' + str(num), override, lang, next_slot, small_space)
         else:
            print(f'WARNING: {item} not handled!')
      for pattern in banner_list:
         image1 = f'../../block images/banner/{pattern}.png'
         image2 = f'../../block images/shield/{pattern}.png'
         if os.path.exists(image1) and os.path.exists(image2):
            chars1 = new_sprite(char_cache, False)
            chars2 = new_sprite(char_cache, False)
            char_cache['external'][hash(pattern + '.banner')] = (chars1, image1)
            char_cache['external'][hash(pattern + '.shield')] = (chars2, image2)
            add_overlay_translations('banner', with_namespace(pattern), [chars1], lang, banner_overlay, '')
            add_overlay_translations('shield', with_namespace(pattern), [chars2], lang, banner_overlay, '')
         else:
            print(f'WARNING: banner pattern {pattern} not handled!')
      for pattern in pot_list:
         if pattern in ('decorated_pot_base', 'decorated_pot_side'):
            continue
         simple_name = pattern.removesuffix('_pottery_pattern')
         item_name = f'{simple_name}_pottery_sherd'
         image1 = f'../../block images/pot/{simple_name}.left.png'
         image2 = f'../../block images/pot/{simple_name}.right.png'
         if os.path.exists(image1) and os.path.exists(image2):
            chars1 = new_sprite(char_cache, False)
            chars2 = new_sprite(char_cache, False)
            char_cache['external'][hash(item_name + '.left')] = (chars1, image1)
            char_cache['external'][hash(item_name + '.right')] = (chars2, image2)
            add_overlay_translations('pot', with_namespace(item_name) + '.left', [chars1], lang, banner_overlay, '')
            add_overlay_translations('pot', with_namespace(item_name) + '.right', [chars2], lang, banner_overlay, '')
         else:
            print(f'WARNING: pot pattern {simple_name} not handled!')
      add_overlay_translations('pot', 'minecraft:brick.left', [{'rows':['', '', '']}], lang, '', '')
      add_overlay_translations('pot', 'minecraft:brick.right', [{'rows':['', '', '']}], lang, '', '')
      got_pats = False
      for path in jar.namelist():
         if path.startswith('data/minecraft/trim_pattern/'):
            got_pats = True
            trim_patterns.append(path.removeprefix('data/minecraft/trim_pattern/').removesuffix('.json'))
         elif got_pats:
            break
   for armor in ('helmet', 'chestplate', 'leggings', 'boots'):
      positive = new_sprite(char_cache, True)
      add_overlay_translations('trim', armor, [positive], lang, banner_overlay, almost_next_slot)
      char_cache['generated'][f'minecraft:trims/items/{armor}_trim'] = positive
   grid = create_grid(char_cache['external'])
   for texture,sprites in char_cache['generated'].items():
      append_sprites(font, texture, {'rows':[[x] for x in sprites['rows']], 'negative':[sprites['negative']]}, sprites.get('anim_height', 1))
   append_sprites(font, 'tryashtar.shulker_preview:block_sheet', {'rows':[[''.join(['\u0000' if entry is None else entry[1][0]['rows'][row] for entry in grid_row]) for grid_row in grid] for row in range(0, 3)]}, 1)
   empty_row = "".join(['\u0000'] * 16)
   for row in range(0, 3):
      nums = ''.join([next_char(char_cache) for x in range(0, 10)])
      shadows = ''.join([next_char(char_cache) for x in range(0, 10)])
      negs = ''.join([next_char(char_cache) for x in range(0, 10)])
      font.append({"type": "bitmap", "file": "minecraft:font/ascii.png", "ascent": -(18 * row) - 11, "height": 8, "chars": [
         empty_row,
         empty_row,
         empty_row,
         nums + '\u0000\u0000\u0000\u0000\u0000\u0000',
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
      font.append({"type": "bitmap", "file": "minecraft:font/ascii.png", "ascent": -(18 * row) - 12, "height": 8, "chars": [
         empty_row,
         empty_row,
         empty_row,
         shadows + '\u0000\u0000\u0000\u0000\u0000\u0000',
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
         negs + '\u0000\u0000\u0000\u0000\u0000\u0000',
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
      for num in range(1, 10):
         lang[f'tryashtar.shulker_preview.number.{num}.{row}'] = tooltip_push_back + negs[num] + nums[num] + small_space
         lang[f'tryashtar.shulker_preview.number_shadow.{num}.{row}'] = overlay_offset + negs[num] + shadows[num]
      for num in range(10, 65):
         d1 = num // 10
         d2 = num % 10
         lang[f'tryashtar.shulker_preview.number.{num}.{row}'] = one_count_overlay + negs[d1] + negs[d2] + nums[d1] + nums[d2] + small_space
         lang[f'tryashtar.shulker_preview.number_shadow.{num}.{row}'] = num_back6 + negs[d1] + negs[d2] + shadows[d1] + shadows[d2]
      dur1 = [next_char(char_cache) for _ in range(1,6)]
      dur2 = [next_char(char_cache) for _ in range(6,11)]
      dur3 = [next_char(char_cache) for _ in range(11,15)]
      durchars = [*dur1, *dur2, *dur3]
      font.append({"type":"bitmap","file":"tryashtar.shulker_preview:durability.png","ascent":-18*row-15,"height":2,"chars":[''.join(dur1),''.join(dur2),''.join(dur3 + ['\u0000'])]})
      for num,char in enumerate(durchars):
         lang[f"tryashtar.shulker_preview.durability.{num}.{row}"] = dura_overlay + char + two_space
      process_item = [
         'data modify entity @s Item set from storage tryashtar.shulker_preview:data item',
         f'execute if items entity @s contents #tryashtar.shulker_preview:special_render run function tryashtar.shulker_preview:render/row_{row}/special with storage tryashtar.shulker_preview:data item',
         f'execute unless items entity @s contents #tryashtar.shulker_preview:special_render run function tryashtar.shulker_preview:render/row_{row}/simple with storage tryashtar.shulker_preview:data item',
         f'execute if items entity @s contents #banners if data storage tryashtar.shulker_preview:data item.components."minecraft:banner_patterns"[0] run function tryashtar.shulker_preview:render/row_{row}/overlay/banner_patterns',
         f'execute if items entity @s contents shield if data storage tryashtar.shulker_preview:data item.components."minecraft:base_color" run function tryashtar.shulker_preview:render/row_{row}/overlay/shield_base',
         f'execute if items entity @s contents shield if data storage tryashtar.shulker_preview:data item.components."minecraft:banner_patterns"[0] run function tryashtar.shulker_preview:render/row_{row}/overlay/shield_patterns',
         f'execute if data storage tryashtar.shulker_preview:data item.components."minecraft:pot_decorations" run function tryashtar.shulker_preview:render/row_{row}/overlay/pot_patterns1',
         f'execute if data storage tryashtar.shulker_preview:data item.components."minecraft:trim" run function tryashtar.shulker_preview:render/row_{row}/overlay/armor_trim',
         f'execute if items entity @s contents *[damage~{{damage:{{min:1}}}},max_damage] run function tryashtar.shulker_preview:render/row_{row}/overlay/durability',
         f'execute if items entity @s contents *[count~{{min:2}}] run function tryashtar.shulker_preview:render/row_{row}/overlay/count with storage tryashtar.shulker_preview:data item',
         f'execute if items entity @s contents bundle[bundle_contents~{{items:{{size:{{min:1}}}}}}] run function tryashtar.shulker_preview:render/row_{row}/overlay/bundle_bar'
      ]
      simple_render = [
         f'$data modify storage tryashtar.shulker_preview:data tooltip append value \'{{"translate":"tryashtar.shulker_preview.item.$(id).{row}","fallback":"%s","with":[{{"translate":"tryashtar.shulker_preview.missingno.{row}"}}]}}\''
      ]
      special_render = [
         '$data modify storage tryashtar.shulker_preview:data item merge from storage tryashtar.shulker_preview:data lookups.colors."$(id)"',
         f'execute if items entity @s contents #tryashtar.shulker_preview:special_render/overrides run return run function tryashtar.shulker_preview:render/row_{row}/special_render/overrides'
      ]
      for name in hardcoded_items:
         special_render.append(f'execute if items entity @s contents #tryashtar.shulker_preview:special_render/{name} run return run function tryashtar.shulker_preview:render/row_{row}/special_render/{name} with storage tryashtar.shulker_preview:data item')
      special_render.append(f'execute if items entity @s contents #dyeable run return run function tryashtar.shulker_preview:render/row_{row}/special_render/dyeable1')
      for kind,items in colorable_items.items():
         if len(items) == 1:
            special_render.append(f'execute if items entity @s contents {items[0]} run return run function tryashtar.shulker_preview:render/row_{row}/special_render/{kind}1')
         else:
            special_render.append(f'execute if items entity @s contents #tryashtar.shulker_preview:special_render/{kind} run return run function tryashtar.shulker_preview:render/row_{row}/special_render/{kind}1')
      write_lines(process_item, f'datapack/data/tryashtar.shulker_preview/functions/render/row_{row}/item.mcfunction')
      write_lines(simple_render, f'datapack/data/tryashtar.shulker_preview/functions/render/row_{row}/simple.mcfunction')
      write_lines(special_render, f'datapack/data/tryashtar.shulker_preview/functions/render/row_{row}/special.mcfunction')
      write_lines([
         f'$data modify storage tryashtar.shulker_preview:data tooltip append value \'{{"translate":"tryashtar.shulker_preview.item.$(id).{row}","color":"$(color)"}}\''
      ], f'datapack/data/tryashtar.shulker_preview/functions/render/row_{row}/special_render/grass_colored.mcfunction')
      write_lines([
         f'$data modify storage tryashtar.shulker_preview:data tooltip append value \'[{{"translate":"tryashtar.shulker_preview.layer.spawn_egg.0.{row}","color":"$(base)"}},{{"translate":"tryashtar.shulker_preview.layer.spawn_egg.1.{row}","color":"$(overlay)"}}]\''
      ], f'datapack/data/tryashtar.shulker_preview/functions/render/row_{row}/special_render/spawn_eggs.mcfunction')
      write_lines([
         'data modify storage tryashtar.shulker_preview:data item merge value {red:"a0",green:"65",blue:"40"}',
         'execute store success score #has_color shulker_preview store result score #color shulker_preview run data get storage tryashtar.shulker_preview:data item.components."minecraft:dyed_color".rgb',
         'execute if score #has_color shulker_preview matches 1 run function tryashtar.shulker_preview:render/convert_color',
         f'function tryashtar.shulker_preview:render/row_{row}/special_render/dyeable2 with storage tryashtar.shulker_preview:data item',
      ], f'datapack/data/tryashtar.shulker_preview/functions/render/row_{row}/special_render/dyeable1.mcfunction')
      write_lines([
         f'$execute if score #has_color shulker_preview matches 1 if items entity @s contents wolf_armor run data modify storage tryashtar.shulker_preview:data tooltip append value \'[{{"translate":"tryashtar.shulker_preview.layer.$(id).0.{row}"}},{{"translate":"tryashtar.shulker_preview.layer.minecraft:wolf_armor.1.{row}","color":"#$(red)$(green)$(blue)"}}]\'',
         f'execute if score #has_color shulker_preview matches 0 if items entity @s contents wolf_armor run data modify storage tryashtar.shulker_preview:data tooltip append value \'{{"translate":"tryashtar.shulker_preview.item.minecraft:wolf_armor.{row}"}}\'',
         f'$execute unless items entity @s contents wolf_armor run data modify storage tryashtar.shulker_preview:data tooltip append value \'[{{"translate":"tryashtar.shulker_preview.layer.$(id).0.{row}","color":"#$(red)$(green)$(blue)"}},{{"translate":"tryashtar.shulker_preview.layer.$(id).1.{row}","color":"white"}}]\''
      ], f'datapack/data/tryashtar.shulker_preview/functions/render/row_{row}/special_render/dyeable2.mcfunction')
      write_lines([
         'data modify storage tryashtar.shulker_preview:data item merge value {red:"38",green:"5d","blue":"c6"}',
         'execute store success score #has_color shulker_preview store result score #color shulker_preview run data get storage tryashtar.shulker_preview:data item.components."minecraft:potion_contents".custom_color',
         'execute if score #has_color shulker_preview matches 1 run function tryashtar.shulker_preview:render/convert_color',
         'execute if score #has_color shulker_preview matches 0 run function tryashtar.shulker_preview:render/potion_color',
         f'function tryashtar.shulker_preview:render/row_{row}/special_render/potion2 with storage tryashtar.shulker_preview:data item',
      ], f'datapack/data/tryashtar.shulker_preview/functions/render/row_{row}/special_render/potion1.mcfunction')
      write_lines([
         f'$data modify storage tryashtar.shulker_preview:data tooltip append value \'[{{"translate":"tryashtar.shulker_preview.layer.$(id).0.{row}","color":"#$(red)$(green)$(blue)"}},{{"translate":"tryashtar.shulker_preview.layer.$(id).1.{row}","color":"white"}}]\''
      ], f'datapack/data/tryashtar.shulker_preview/functions/render/row_{row}/special_render/potion2.mcfunction')
      write_lines([
         'data modify storage tryashtar.shulker_preview:data item merge value {red:"46",green:"40","blue":"2e"}',
         'execute store success score #has_color shulker_preview store result score #color shulker_preview run data get storage tryashtar.shulker_preview:data item.components."minecraft:map_color"',
         'execute if score #has_color shulker_preview matches 1 run function tryashtar.shulker_preview:render/convert_color',
         f'function tryashtar.shulker_preview:render/row_{row}/special_render/map2 with storage tryashtar.shulker_preview:data item',
      ], f'datapack/data/tryashtar.shulker_preview/functions/render/row_{row}/special_render/map1.mcfunction')
      write_lines([
         f'$data modify storage tryashtar.shulker_preview:data tooltip append value \'[{{"translate":"tryashtar.shulker_preview.layer.$(id).0.{row}"}},{{"translate":"tryashtar.shulker_preview.layer.$(id).1.{row}","color":"#$(red)$(green)$(blue)"}}]\''
      ], f'datapack/data/tryashtar.shulker_preview/functions/render/row_{row}/special_render/map2.mcfunction')
      write_lines([
         'data modify storage tryashtar.shulker_preview:data item merge value {red:"8a",green:"8a","blue":"8a"}',
         'function tryashtar.shulker_preview:render/star_color',
         f'function tryashtar.shulker_preview:render/row_{row}/special_render/star2 with storage tryashtar.shulker_preview:data item',
      ], f'datapack/data/tryashtar.shulker_preview/functions/render/row_{row}/special_render/star1.mcfunction')
      write_lines([
         f'$data modify storage tryashtar.shulker_preview:data tooltip append value \'[{{"translate":"tryashtar.shulker_preview.layer.$(id).0.{row}"}},{{"translate":"tryashtar.shulker_preview.layer.$(id).1.{row}","color":"#$(red)$(green)$(blue)"}}]\''
      ], f'datapack/data/tryashtar.shulker_preview/functions/render/row_{row}/special_render/star2.mcfunction')
      write_lines([
         f'$data modify storage tryashtar.shulker_preview:data tooltip append value \'[{{"translate":"tryashtar.shulker_preview.number_shadow.$(count).{row}","color":"#3e3e3e"}},{{"translate":"tryashtar.shulker_preview.number.$(count).{row}","color":"white"}}]\''
      ], f'datapack/data/tryashtar.shulker_preview/functions/render/row_{row}/overlay/count.mcfunction')
      write_lines([
         'data modify storage tryashtar.shulker_preview:data tooltip append value \'{"translate":"tryashtar.shulker_preview.overlay"}\'',
         f'function tryashtar.shulker_preview:render/row_{row}/overlay/banner_patterns_loop',
         'data modify storage tryashtar.shulker_preview:data tooltip append value \'{"translate":"tryashtar.shulker_preview.overlay_done"}\''
      ], f'datapack/data/tryashtar.shulker_preview/functions/render/row_{row}/overlay/banner_patterns.mcfunction')
      write_lines([
         'function tryashtar.shulker_preview:render/banner_color with storage tryashtar.shulker_preview:data item.components."minecraft:banner_patterns"[0]',
         f'function tryashtar.shulker_preview:render/row_{row}/overlay/banner_patterns_one with storage tryashtar.shulker_preview:data item.components."minecraft:banner_patterns"[0]',
         'data remove storage tryashtar.shulker_preview:data item.components."minecraft:banner_patterns"[0]',
         f'execute if data storage tryashtar.shulker_preview:data item.components."minecraft:banner_patterns"[0] run function tryashtar.shulker_preview:render/row_{row}/overlay/banner_patterns_loop'
      ], f'datapack/data/tryashtar.shulker_preview/functions/render/row_{row}/overlay/banner_patterns_loop.mcfunction')
      write_lines([
         f'$data modify storage tryashtar.shulker_preview:data tooltip append value \'{{"translate":"tryashtar.shulker_preview.overlay.banner.$(pattern).{row}","color":"$(color)"}}\''
      ], f'datapack/data/tryashtar.shulker_preview/functions/render/row_{row}/overlay/banner_patterns_one.mcfunction')
      write_lines([
         'data modify storage tryashtar.shulker_preview:data tooltip append value \'{"translate":"tryashtar.shulker_preview.overlay"}\'',
         f'function tryashtar.shulker_preview:render/row_{row}/overlay/shield_patterns_loop',
         'data modify storage tryashtar.shulker_preview:data tooltip append value \'{"translate":"tryashtar.shulker_preview.overlay_done"}\''
      ], f'datapack/data/tryashtar.shulker_preview/functions/render/row_{row}/overlay/shield_patterns.mcfunction')
      write_lines([
         'function tryashtar.shulker_preview:render/banner_color with storage tryashtar.shulker_preview:data item.components."minecraft:banner_patterns"[0]',
         f'function tryashtar.shulker_preview:render/row_{row}/overlay/shield_patterns_one with storage tryashtar.shulker_preview:data item.components."minecraft:banner_patterns"[0]',
         'data remove storage tryashtar.shulker_preview:data item.components."minecraft:banner_patterns"[0]',
         f'execute if data storage tryashtar.shulker_preview:data item.components."minecraft:banner_patterns"[0] run function tryashtar.shulker_preview:render/row_{row}/overlay/shield_patterns_loop'
      ], f'datapack/data/tryashtar.shulker_preview/functions/render/row_{row}/overlay/shield_patterns_loop.mcfunction')
      write_lines([
         f'$data modify storage tryashtar.shulker_preview:data tooltip append value \'{{"translate":"tryashtar.shulker_preview.overlay.shield.$(pattern).{row}","color":"$(color)"}}\''
      ], f'datapack/data/tryashtar.shulker_preview/functions/render/row_{row}/overlay/shield_patterns_one.mcfunction')
      shield_base = []
      for dye,color in dye_map.items():
         shield_base.append(f'execute if data storage tryashtar.shulker_preview:data item.components{{"minecraft:base_color":"{dye}"}} run return run data modify storage tryashtar.shulker_preview:data tooltip append value \'[{{"translate":"tryashtar.shulker_preview.overlay"}},{{"translate":"tryashtar.shulker_preview.overlay.shield.minecraft:base.{row}","color":"{color}"}},{{"translate":"tryashtar.shulker_preview.overlay_done"}}]\'')
      shield_base.append('data modify storage tryashtar.shulker_preview:data tooltip append value \'{"translate":"tryashtar.shulker_preview.overlay_done"}\'')
      write_lines(shield_base, f'datapack/data/tryashtar.shulker_preview/functions/render/row_{row}/overlay/shield_base.mcfunction')
      write_lines([
         'data modify storage tryashtar.shulker_preview:data tooltip append value \'{"translate":"tryashtar.shulker_preview.overlay"}\'',
         'data modify storage tryashtar.shulker_preview:data item.left set from storage tryashtar.shulker_preview:data item.components."minecraft:pot_decorations"[1]',
         'data modify storage tryashtar.shulker_preview:data item.right set from storage tryashtar.shulker_preview:data item.components."minecraft:pot_decorations"[3]',
         f'function tryashtar.shulker_preview:render/row_{row}/overlay/pot_patterns2 with storage tryashtar.shulker_preview:data item',
         'data modify storage tryashtar.shulker_preview:data tooltip append value \'{"translate":"tryashtar.shulker_preview.overlay_done"}\''
      ], f'datapack/data/tryashtar.shulker_preview/functions/render/row_{row}/overlay/pot_patterns1.mcfunction')
      write_lines([
         f'$data modify storage tryashtar.shulker_preview:data tooltip append value \'[{{"translate":"tryashtar.shulker_preview.overlay.pot.$(left).left.{row}"}},{{"translate":"tryashtar.shulker_preview.overlay.pot.$(right).right.{row}"}}]\''
      ], f'datapack/data/tryashtar.shulker_preview/functions/render/row_{row}/overlay/pot_patterns2.mcfunction')
      main_trim = []
      for armor,tag in {'helmet':'head_armor', 'chestplate':'chest_armor', 'leggings':'leg_armor', 'boots':'foot_armor'}.items():
         armor_trim = []
         for material,color in trim_materials.items():
            if isinstance(color, tuple):
               armor_trim.append(f'execute if data storage tryashtar.shulker_preview:data item.components{{"minecraft:trim":{{material:"minecraft:{material}"}}}} if items entity @s contents #tryashtar.shulker_preview:armor_material/{material} run return run data modify storage tryashtar.shulker_preview:data tooltip append value \'[{{"translate":"tryashtar.shulker_preview.overlay"}},{{"translate":"tryashtar.shulker_preview.overlay.trim.{armor}.{row}","color":"{color[1]}"}},{{"translate":"tryashtar.shulker_preview.overlay_done"}}]\'')
               armor_trim.append(f'execute if data storage tryashtar.shulker_preview:data item.components{{"minecraft:trim":{{material:"minecraft:{material}"}}}} run return run data modify storage tryashtar.shulker_preview:data tooltip append value \'[{{"translate":"tryashtar.shulker_preview.overlay"}},{{"translate":"tryashtar.shulker_preview.overlay.trim.{armor}.{row}","color":"{color[0]}"}},{{"translate":"tryashtar.shulker_preview.overlay_done"}}]\'')
            else:
               armor_trim.append(f'execute if data storage tryashtar.shulker_preview:data item.components{{"minecraft:trim":{{material:"minecraft:{material}"}}}} run return run data modify storage tryashtar.shulker_preview:data tooltip append value \'[{{"translate":"tryashtar.shulker_preview.overlay"}},{{"translate":"tryashtar.shulker_preview.overlay.trim.{armor}.{row}","color":"{color}"}},{{"translate":"tryashtar.shulker_preview.overlay_done"}}]\'')
         write_lines(armor_trim, f'datapack/data/tryashtar.shulker_preview/functions/render/row_{row}/overlay/armor_trim/{armor}.mcfunction')
         main_trim.append(f'execute if items entity @s contents #{tag} run return run function tryashtar.shulker_preview:render/row_{row}/overlay/armor_trim/{armor}')
      write_lines(main_trim, f'datapack/data/tryashtar.shulker_preview/functions/render/row_{row}/overlay/armor_trim.mcfunction')
      durability = [
         'execute store result score #damage shulker_preview run data get storage tryashtar.shulker_preview:data item.components."minecraft:damage"'
      ]
      for n in range(0, 13):
         threshold = 1-((0.5 + n) / 13)
         r,g,b = colorsys.hsv_to_rgb((13 - n) / 13 / 3, 1, 1)
         color = color_hex(int(r*255)*256*256 + int(g*255)*256 + int(b*255))
         durability.extend([
            f'item modify entity @s contents {{function:"set_damage",damage:{threshold}}}',
            'execute store result score #threshold shulker_preview run data get entity @s Item.components."minecraft:damage"',
            f'execute if score #damage shulker_preview <= #threshold shulker_preview run return run data modify storage tryashtar.shulker_preview:data tooltip append value \'{{"translate":"tryashtar.shulker_preview.durability.{n}.{row}","color":"{color}"}}\''
         ])
      durability.append(f'data modify storage tryashtar.shulker_preview:data tooltip append value \'{{"translate":"tryashtar.shulker_preview.durability.13.{row}"}}\'')
      write_lines(durability, f'datapack/data/tryashtar.shulker_preview/functions/render/row_{row}/overlay/durability.mcfunction')
      bundle_bar = [
         'scoreboard players set #fullness shulker_preview 0',
         'data modify storage tryashtar.shulker_preview:data bundle_stack set value [{fullness:0}]',
         'data modify storage tryashtar.shulker_preview:data bundle_stack[0].contents set from storage tryashtar.shulker_preview:data item.components."minecraft:bundle_contents"',
         'function tryashtar.shulker_preview:render/bundle_weight',
         f'execute if score #fullness shulker_preview matches 64000.. run return run data modify storage tryashtar.shulker_preview:data tooltip append value \'{{"translate":"tryashtar.shulker_preview.durability.0.{row}","color":"#6666ff"}}\'',
         f'execute if score #fullness shulker_preview matches 59000.. run return run data modify storage tryashtar.shulker_preview:data tooltip append value \'{{"translate":"tryashtar.shulker_preview.durability.1.{row}","color":"#6666ff"}}\'',
         f'execute if score #fullness shulker_preview matches 54000.. run return run data modify storage tryashtar.shulker_preview:data tooltip append value \'{{"translate":"tryashtar.shulker_preview.durability.2.{row}","color":"#6666ff"}}\'',
         f'execute if score #fullness shulker_preview matches 48000.. run return run data modify storage tryashtar.shulker_preview:data tooltip append value \'{{"translate":"tryashtar.shulker_preview.durability.3.{row}","color":"#6666ff"}}\'',
         f'execute if score #fullness shulker_preview matches 43000.. run return run data modify storage tryashtar.shulker_preview:data tooltip append value \'{{"translate":"tryashtar.shulker_preview.durability.4.{row}","color":"#6666ff"}}\'',
         f'execute if score #fullness shulker_preview matches 38000.. run return run data modify storage tryashtar.shulker_preview:data tooltip append value \'{{"translate":"tryashtar.shulker_preview.durability.5.{row}","color":"#6666ff"}}\'',
         f'execute if score #fullness shulker_preview matches 32000.. run return run data modify storage tryashtar.shulker_preview:data tooltip append value \'{{"translate":"tryashtar.shulker_preview.durability.6.{row}","color":"#6666ff"}}\'',
         f'execute if score #fullness shulker_preview matches 27000.. run return run data modify storage tryashtar.shulker_preview:data tooltip append value \'{{"translate":"tryashtar.shulker_preview.durability.7.{row}","color":"#6666ff"}}\'',
         f'execute if score #fullness shulker_preview matches 22000.. run return run data modify storage tryashtar.shulker_preview:data tooltip append value \'{{"translate":"tryashtar.shulker_preview.durability.8.{row}","color":"#6666ff"}}\'',
         f'execute if score #fullness shulker_preview matches 16000.. run return run data modify storage tryashtar.shulker_preview:data tooltip append value \'{{"translate":"tryashtar.shulker_preview.durability.9.{row}","color":"#6666ff"}}\'',
         f'execute if score #fullness shulker_preview matches 11000.. run return run data modify storage tryashtar.shulker_preview:data tooltip append value \'{{"translate":"tryashtar.shulker_preview.durability.10.{row}","color":"#6666ff"}}\'',
         f'execute if score #fullness shulker_preview matches 6000.. run return run data modify storage tryashtar.shulker_preview:data tooltip append value \'{{"translate":"tryashtar.shulker_preview.durability.11.{row}","color":"#6666ff"}}\'',
         f'data modify storage tryashtar.shulker_preview:data tooltip append value \'{{"translate":"tryashtar.shulker_preview.durability.12.{row}","color":"#6666ff"}}\''
      ]
      write_lines(bundle_bar, f'datapack/data/tryashtar.shulker_preview/functions/render/row_{row}/overlay/bundle_bar.mcfunction')
      override_fn = []
      for item,predicates in override_items.items():
         override_fn.append(f'execute if items entity @s contents {item} run return run function tryashtar.shulker_preview:render/row_{row}/special_render/{item} with storage tryashtar.shulker_preview:data item')
         specific_fn = []
         light_check = False
         for num,predicate in reversed(list(enumerate(predicates))):
            if predicate.get('charged', 0) == 1 and predicate.get('firework', 0) == 1:
               del predicate['charged']
            test = []
            for check,value in predicate.items():
               if check == 'charged':
                  test.append('if data storage tryashtar.shulker_preview:data item.components."minecraft:charged_projectiles"[0]')
               elif check == 'firework':
                  test.append('if data storage tryashtar.shulker_preview:data item.components."minecraft:charged_projectiles"[{id:"minecraft:firework_rocket"}]')
               elif check == 'level':
                  level = int(value*16)
                  test.append(f'if data storage tryashtar.shulker_preview:data item.components."minecraft:block_state"{{level:"{level}"}}')
                  light_check = True
               elif check == 'filled':
                  test.append('if items entity @s contents *[bundle_contents~{items:{size:{min:1}}}]')
               elif check == 'broken':
                  test.append('if items entity @s contents *[damage~{durability:{max:0}}]')
               else:
                  print(f'WARNING: unknown predicate {check} in item {item}')
            specific_fn.append(f'execute {" ".join(test)} run return run data modify storage tryashtar.shulker_preview:data tooltip append value \'{{"translate":"tryashtar.shulker_preview.override.minecraft:{item}.{num}.{row}"}}\'')
         if light_check:
            specific_fn.insert(0, 'execute unless data storage tryashtar.shulker_preview:data item.components."minecraft:block_state".level run data modify storage tryashtar.shulker_preview:data item.components."minecraft:block_state".level set value "15"')
         specific_fn.append(f'data modify storage tryashtar.shulker_preview:data tooltip append value \'{{"translate":"tryashtar.shulker_preview.item.minecraft:{item}.{row}"}}\'')
         write_lines(specific_fn, f'datapack/data/tryashtar.shulker_preview/functions/render/row_{row}/special_render/{item}.mcfunction')
      write_lines(override_fn, f'datapack/data/tryashtar.shulker_preview/functions/render/row_{row}/special_render/overrides.mcfunction')
   grid_image = create_image(grid, 64)
   grid_image.save('resourcepack/assets/tryashtar.shulker_preview/textures/block_sheet.png', 'PNG')
   write_json(lang, 'resourcepack/assets/tryashtar.shulker_preview/lang/en_us.json')
   write_json({"providers":font}, 'resourcepack/assets/tryashtar.shulker_preview/font/preview.json')
   write_json({"values":special_render_tag}, 'datapack/data/tryashtar.shulker_preview/tags/items/special_render.json')
   write_json({"values":list(sorted(override_items.keys()))}, 'datapack/data/tryashtar.shulker_preview/tags/items/special_render/overrides.json')
   shutil.make_archive(f'Shulker Preview Data Pack ({target_version})', 'zip', 'datapack')
   shutil.make_archive(f'Shulker Preview Resource Pack ({target_version})', 'zip', 'resourcepack')
   shutil.make_archive(f'Shulker Preview Dark Theme ({target_version})', 'zip', 'resourcepack_dark')

def download_json(url, path):
   if os.path.exists(path):
      with open(path, 'r', encoding='utf-8') as file:
         return json.load(file)
   data = urllib.request.urlopen(url).read()
   with open(path, 'wb') as file:
      file.write(data)
   return json.loads(data)

def calculate_appearance_hash(item, model):
   if len(model.get('elements', {})) == 0:
      return hash(item)
   return hash((json.dumps(model['textures']), json.dumps(model['elements'])))

def color_hex(int_color):
   return f'#{format(int_color, '06x')}'

def add_layered_translations(name, textures, lang, next_slot, overlay_offset):
   result = []
   for row in range(0, 3):
      sub = []
      for layernum,layer in enumerate(textures):
         key = f'tryashtar.shulker_preview.layer.{name}.{layernum}.{row}'
         text = layer['rows'][row] + layer['negative']
         if layernum == len(textures) - 1:
            text += next_slot
         else:
            text += overlay_offset
         lang[key] = text
         sub.append(key)
      result.append(sub)
   return result

def add_overlay_translations(kind, name, textures, lang, back, forth):
   result = []
   for row in range(0, 3):
      key = f'tryashtar.shulker_preview.overlay.{kind}.{name}.{row}'
      value = back
      for layer in textures:
         if 'negative' in layer:
            value += layer['rows'][row] + layer['negative']
         else:
            value += layer['rows'][row]
      value += forth
      lang[key] = value
      result.append(key)
   return result

def add_normal_translations(kind, name, textures, lang, next_slot, one_space):
   result = []
   for row in range(0, 3):
      key = f'tryashtar.shulker_preview.{kind}.{name}.{row}'
      value = ''
      negatives = False
      for layer in textures:
         if 'negative' in layer:
            value += layer['rows'][row] + layer['negative']
            negatives = True
         else:
            value += layer['rows'][row]
      if negatives:
         value += next_slot
      else:
         value += one_space
      lang[key] = value
      result.append(key)
   return result

def append_sprites(font, texture, sprite_chars, anim_height):
   for row in range(0, 3):
      result = list(sprite_chars['rows'][row])
      for _ in range(1, anim_height):
         result.append('\u0000' * len(result[0]))
      font.append({"type":"bitmap","file":f'{texture}.png',"ascent":-2 + (row * -18),"height":16,"chars":result})
   if 'negative' in sprite_chars:
      result = list(sprite_chars['negative'])
      for _ in range(1, anim_height):
         result.append('\u0000' * len(result[0]))
      font.append({"type":"bitmap","file":f'{texture}.png',"ascent":-32768,"height":-16,"chars":result})

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
      path = icon[1][1]
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

def new_sprite(cache, negative):
   result = {
      'rows': [next_char(cache), next_char(cache), next_char(cache)]
   }
   if negative:
      result['negative'] = next_char(cache)
   return result

def next_char(cache):
   char = cache['prev'] + 1
   for low, high in [(0xd800, 0xdbff), (0xdc00, 0xdfff), (0x05c8, 0x05d2), (0x05e8, 0x05ff), (0x061b, 0x0620), (0x0648, 0x065f), (0x066d, 0x066f), (0x070b, 0x0710), (0x072d, 0x072f), (0x074b, 0x074f), (0x07a4, 0x07a5), (0x07b1, 0x07c2), (0x07f4, 0x07f5), (0x07fa, 0x07fc), (0x07fe, 0x0800), (0x082e, 0x0832), (0x083c, 0x0842), (0x0856, 0x0858), (0x085c, 0x0862), (0x0868, 0x0897), (0x08a0, 0x08a2), (0x08b2, 0x08b8), (0x08c5, 0x08c9), (0xfb34, 0xfb48), (0xfbbf, 0xfbd5), (0xfd8d, 0xfd94), (0xfdc5, 0xfdce), (0xfdf0, 0xfdf2), (0xfe72, 0xfe78), (0xfefa, 0xfefe)]:
      if low <= char <= high:
         char = high + 1
   while char in [0x0000, 0x000a, 0x00a7, 0x0025, 0x0590, 0x05be, 0x05c0, 0x05c3, 0x05c6, 0x0608, 0x060b, 0x060d, 0x0712, 0x081a, 0x0824, 0x0828, 0x200f, 0xfb1d, 0xfb1f] or unicodedata.bidirectional(chr(char)) in ['AL', 'R']:
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
      parent_name = model.get('parent')
      if parent_name is not None:
         parent_name = with_namespace(parent_name)
         if parent_name == 'minecraft:builtin/generated':
            model['generated'] = True
         elif not parent_name.startswith('minecraft:builtin/'):
            parent = get_model(jar, cache, parent_name)
            if parent.get('generated', False):
               model['generated'] = True
            for key,value in parent['textures'].items():
               if key not in model['textures']:
                  model['textures'][key] = value
            if 'elements' in parent and 'elements' not in model:
               model['elements'] = parent['elements']
      cache[identifier] = model
      return model

def with_namespace(identifier):
   if ':' in identifier:
      return identifier
   return f'minecraft:{identifier}'

def write_json(data, path):
   os.makedirs(os.path.dirname(path), exist_ok=True)
   with open(path, 'w', encoding='utf-8') as file:
      json.dump(data, file, indent=3, ensure_ascii=True)

def write_lines(lines, path):
   os.makedirs(os.path.dirname(path), exist_ok=True)
   with open(path, 'w', encoding='utf-8') as file:
      for line in lines:
         file.write(line + '\n')

if __name__ == '__main__':
   main()
