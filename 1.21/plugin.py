import math
import re
import unicodedata
import PIL.Image
import beet
import model_resolver
import model_resolver.utils

def main(ctx: beet.Context):
   icon = beet.PngFile(PIL.Image.open('in/pack.png'))
   ctx.assets.icon = icon
   ctx.data.icon = icon
   # to do: when https://github.com/mcbeet/beet/pull/472 is merged, use 'minecraft' field
   target_version = ctx.meta['minecraft_version']
   ctx.meta['model_resolver'] = {
      'minecraft_version': target_version,
      'preferred_minecraft_generated': 'java',
      'special_rendering': True,
      'use_cache': True
   }
   render = model_resolver.Render(ctx)
   render.default_render_size = 64
   vanilla = render.getter._vanilla
   components = model_resolver.utils.get_default_components(ctx)
   unusual_default_models = {}
   for model, defaults in components.items():
      if defaults['minecraft:item_model'] != model:
         unusual_default_models[model] = defaults['minecraft:item_model']
   generated_sprites: list[str] = []
   font = FontManager()
   next_slot = font.get_space(15)
   overlay = font.get_space(-3)
   translatable_models = {}
   not_fully_macroable = {}
   for name, entry in vanilla.assets.item_models.items():
      squashed_model = squash_conditions(entry.data['model'])
      model_type = short(squashed_model['type'])
      match model_type:
         case 'model':
            model_name = squashed_model['model']
            model = vanilla.assets.models[model_name]
            tints = squashed_model.get('tints')
            if tints is not None:
               not_fully_macroable[name] = {'tints':tints, 'layers':[]}
            layers = generated_layers(vanilla.assets.models, model)
            if layers is not None:
               translatable_models[name] = []
               for layer in layers:
                  layer_name = canon(layer)
                  # technically we should be looking the layers up in the atlas to get the real texture path
                  font.add_sprite(layer_name)
                  translatable_models[name].append(layer_name)
                  if name in not_fully_macroable:
                     not_fully_macroable[name]['layers'].append(layer_name)
            else:
               gen_name = model_name + '.model'
               if gen_name not in generated_sprites:
                  render.add_model_task(
                     model = model_name,
                     path_ctx = gen_name,
                     animation_mode = 'one_file'
                  )
                  generated_sprites.append(gen_name)
               translatable_models[name] = [gen_name]
               if name in not_fully_macroable:
                  not_fully_macroable[name]['sprite'] = gen_name
         case 'special':
            gen_name = name + '.item'
            if gen_name not in generated_sprites:
               render.add_item_task(
                  item = model_resolver.Item(id=name, components={'minecraft:item_model':name}),
                  path_ctx = gen_name,
                  animation_mode = 'one_file'
               )
               generated_sprites.append(gen_name)
            translatable_models[name] = [gen_name]
         case _:
            not_fully_macroable[name] = {'model':squashed_model}
   render.run()
   generated_entries = [(ctx.assets.textures[x].image, x) for x in generated_sprites]
   grid_img, grid_refs = make_grid(generated_entries, render.default_render_size)
   for path in generated_sprites:
      del ctx.assets.textures[path]
   datapack = ctx.data['tryashtar.shulker_preview']
   resourcepack = ctx.assets['tryashtar.shulker_preview']
   resourcepack.textures['block_sheet'] = beet.Texture(grid_img)
   font.add_grid('block_sheet', grid_refs)
   resourcepack.fonts['preview'] = font.build()
   lang = resourcepack.languages['en_us']
   for model, sprites in translatable_models.items():
      data = [font.get_sprite(x) for x in sprites]
      lang.data[f'tryashtar.shulker_preview.item.{model}.0'] = overlay.join([x['rows'][0] + x['negative'] for x in data]) + next_slot
      lang.data[f'tryashtar.shulker_preview.item.{model}.1'] = overlay.join([x['rows'][1] + x['negative'] for x in data]) + next_slot
      lang.data[f'tryashtar.shulker_preview.item.{model}.2'] = overlay.join([x['rows'][2] + x['negative'] for x in data]) + next_slot
   simple_tinted = {}
   for model, special in list(not_fully_macroable.items()):
      if 'tints' in special and len(special['tints']) == 1:
         tint = special['tints'][0]
         if short(tint['type']) == 'grass':
            if tint['downfall'] == 1.0 and tint['temperature'] == 0.5:
               tint['type'] = 'minecraft:constant'
               tint['value'] = 0xff7bbd6b
         if short(tint['type']) == 'constant':
            simple_tinted[model] = tint['value']
            del not_fully_macroable[model]
   for row in range(3):
      item = [
         'data modify entity @s Item set from storage tryashtar.shulker_preview:data item',
         f'function tryashtar.shulker_preview:render/row_{row}/sprite',
      ]
      sprite = []
      simple_tinted_check = '|'.join([f'item_model="{short(x)}"' for x in simple_tinted.keys()])
      sprite.append(f'execute if items entity @s contents *[{simple_tinted_check}] run return run function tryashtar.shulker_preview:render/row_{row}/sprite/simple_tinted')
      sprite_simple_tinted = []
      for model, tint in simple_tinted.items():
         sprite_simple_tinted.append(f'execute if items entity @s contents *[item_model="{short(model)}"] run return run data modify storage tryashtar.shulker_preview:data tooltip append value {{translate:"tryashtar.shulker_preview.item.{model}.{row}",color:"{color_hex(tint)}",fallback:"%s",with:[{{translate:"tryashtar.shulker_preview.missingno.{row}"}}]}}')
      datapack.functions[f'render/row_{row}/item'] = beet.Function(item)
      datapack.functions[f'render/row_{row}/sprite'] = beet.Function(sprite)
      datapack.functions[f'render/row_{row}/sprite/simple_tinted'] = beet.Function(sprite_simple_tinted)
   if len(not_fully_macroable) > 0:
      print('UNHANDLED MODELS:')
      for model, data in not_fully_macroable.items():
         print(model)
         print(data)
         print()

def color_hex(color: int):
   if color < 0:
      color += 2**32
   color %= 2**24
   return f'#{format(color, '06x')}'

def squash_conditions(model: dict) -> dict:
   model_type = short(model['type'])
   match model_type:
      case 'condition':
         prop = short(model['property'])
         model['on_true'] = squash_conditions(model['on_true'])
         model['on_false'] = squash_conditions(model['on_false'])
         if model['on_true'] == model['on_false']:
            return model['on_true']
         match prop:
            case 'bundle/has_selected_item' | 'carried' | 'extended_view' | 'fishing_rod/cast' | 'keybind_down' | 'selected' | 'using_item' | 'view_entity':
               return model['on_false']
            case _:
               return model
      case 'select':
         prop = short(model['property'])
         if 'fallback' in model:
            model['fallback'] = squash_conditions(model['fallback'])
         for case in model['cases']:
            case['model'] = squash_conditions(case['model'])
         match prop:
            case 'context_entity_type' | 'local_time':
               return model['fallback']
            case 'context_dimension':
               for case in model['cases']:
                  if case['when'] == 'overworld' or 'overworld' in case['when']:
                     return case['model']
               return model['fallback']
            case 'display_context':
               for case in model['cases']:
                  if case['when'] == 'gui' or 'gui' in case['when']:
                     return case['model']
                  return model['fallback']
            case 'main_hand':
               for case in model['cases']:
                  if case['when'] == 'right' or 'right' in case['when']:
                     return case['model']
                  return model['fallback']
            case _:
               return model
      case 'range_dispatch':
         prop = short(model['property'])
         if 'fallback' in model:
            model['fallback'] = squash_conditions(model['fallback'])
         for case in model['entries']:
            case['model'] = squash_conditions(case['model'])
         match prop:
            case 'compass' | 'cooldown' | 'crossbow/pull' | 'time' | 'use_cycle' | 'use_duration':
               for case in model['entries']:
                  if case['threshold'] == 0:
                     return case['model']
               return model['fallback']
            case _:
               return model
      case _:
         return model
   return model

def make_grid(entries: list[tuple[PIL.Image.Image, str]], icon_size: int) -> tuple[PIL.Image.Image, list[list[str | None]]]:
   width, height = grid_dimensions(len(entries))
   image = PIL.Image.new('RGBA', (width * icon_size, height * icon_size))
   path_return: list[list[str | None]] = [[None]*width for _ in range(height)]
   for i, (sprite, path) in enumerate(entries):
      pos_x = i % width
      pos_y = i // width
      path_return[pos_y][pos_x] = path
      x = pos_x * icon_size
      y = pos_y * icon_size
      image.paste(sprite, (x, y, x + icon_size, y + icon_size))
      # to do: with negatives, is this still necessary?
      for corner in (0, icon_size - 1):
         r,g,b,a = sprite.getpixel((corner, corner))
         if a == 0:
            r,g,b = (139, 139, 139)
         image.putpixel((x + corner, y + corner), (r, g, b, max(a, 18)))
   return (image, path_return)

def grid_dimensions(area: int) -> tuple[int, int]:
   width = math.ceil(math.sqrt(area))
   height = width
   if width * (height - 1) >= area:
      height -= 1
   return (width, height)

class FontManager:
   def __init__(self):
      self.last_char = 0
      self.spaces: dict[int, str] = {}
      self.sprites: dict[str, dict] = {}
      self.grids: dict[str, dict] = {}
      self.sprite_map: dict[str, dict] = {}
   
   def add_sprite(self, texture: str):
      data = {'rows': [self.next_char(), self.next_char(), self.next_char()], 'negative': self.next_char()}
      self.sprites[texture] = data
      self.sprite_map[texture] = data
   
   def add_grid(self, grid: str, textures: list[list[str | None]]):
      rows: list[list[str]] = [[], [], []]
      negative: list[str] = []
      for row in textures:
         rows[0].append('')
         rows[1].append('')
         rows[2].append('')
         negative.append('')
         for texture in row:
            if texture is not None:
               r0 = self.next_char()
               r1 = self.next_char()
               r2 = self.next_char()
               n = self.next_char()
               rows[0][-1] += r0
               rows[1][-1] += r1
               rows[2][-1] += r2
               negative[-1] += n
               self.sprite_map[texture] = {'rows': [r0, r1, r2], 'negative': n}
            else:
               rows[0][-1] += '\u0000'
               rows[1][-1] += '\u0000'
               rows[2][-1] += '\u0000'
               negative[-1] += '\u0000'
      self.grids[grid] = {'rows': rows, 'negative': negative}
      
   def get_sprite(self, texture: str) -> dict:
      return self.sprite_map[texture]
   
   def next_char(self):
      char = self.last_char + 1
      for low, high in [(0xd800, 0xdbff), (0xdc00, 0xdfff), (0x05c8, 0x05d2), (0x05e8, 0x06ff), (0x070b, 0x0710), (0x072d, 0x072f), (0x074b, 0x074f), (0x07a4, 0x07a5), (0x07b1, 0x07c2), (0x07f4, 0x07f5), (0x07fa, 0x07fc), (0x07fe, 0x0800), (0x082e, 0x0832), (0x083c, 0x0842), (0x0856, 0x0858), (0x085c, 0x0862), (0x0868, 0x0897), (0x08a0, 0x08a2), (0x08b2, 0x08b8), (0x08c5, 0x08c9), (0xfb34, 0xfb48), (0xfbbf, 0xfbd5), (0xfd8d, 0xfd94), (0xfdc5, 0xfdce), (0xfdf0, 0xfdf2), (0xfe72, 0xfe78), (0xfefa, 0xfefe)]:
         if low <= char <= high:
            char = high + 1
      while char in [0x0000, 0x000a, 0x00a7, 0x0025, 0x0590, 0x05be, 0x05c0, 0x05c3, 0x05c6, 0x0608, 0x060b, 0x060d, 0x0712, 0x081a, 0x0824, 0x0828, 0x200f, 0xfb1d, 0xfb1f] or unicodedata.bidirectional(chr(char)) in ['AL', 'R', 'NSM']:
         char += 1
      self.last_char = char
      return chr(char)
      
   def get_space(self, width: int) -> str:
      if width in self.spaces:
         return self.spaces[width]
      char = self.next_char()
      self.spaces[width] = char
      return char
   
   def build(self) -> beet.Font:
      result = beet.Font()
      providers = []
      if len(self.spaces) > 0:
         spaces = {}
         for width, char in self.spaces.items():
            spaces[char] = width
         providers.append({'type':'space','advances':spaces})
      for path, data in self.sprites.items():
         for row, entry in enumerate(data['rows']):
            providers.append({'type':'bitmap','file':path,'ascent':-2 + (row * -18),'height':16,'chars':[entry]})
         providers.append({'type':'bitmap','file':path,'ascent':-32768,'height':-16,'chars':[data['negative']]})
      for path, data in self.grids.items():
         for row, entry in enumerate(data['rows']):
            providers.append({'type':'bitmap','file':path,'ascent':-2 + (row * -18),'height':16,'chars':entry})
         providers.append({'type':'bitmap','file':path,'ascent':-32768,'height':-16,'chars':data['negative']})
      result.data['providers'] = providers
      return result

def canon(location: str) -> str:
   return f'minecraft:{location}' if ':' not in location else location

def short(location: str) -> str:
   return location.removeprefix('minecraft:')

def generated_layers(source: beet.NamespaceProxy[beet.Model], model: beet.Model) -> list[str] | None:
   result = []
   while 'parent' in model.data:
      if 'textures' in model.data:
         for name, path in model.data['textures'].items():
            match = re.match(r'layer(\d+)', name)
            if match:
               index = int(match.group(1))
               if index >= len(result):
                  result.extend([None] * (index - len(result) + 1))
               result[index] = path
      parent = canon(model.data['parent'])
      if parent == 'minecraft:builtin/generated':
         return result
      model = source[parent]
   return None
