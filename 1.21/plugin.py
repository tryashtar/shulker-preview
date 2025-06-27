import math
import re
import unicodedata
import PIL.Image
import beet
import model_resolver
import model_resolver.utils

def main(ctx: beet.Context):
   target_version = ctx.meta['minecraft_version']
   ctx.meta['model_resolver'] = {
      'minecraft_version': target_version,
      'preferred_minecraft_generated': 'java',
      'special_rendering': True
   }
   render = model_resolver.Render(ctx)
   render.default_render_size = 64
   vanilla = render.getter._vanilla
   components = model_resolver.utils.get_default_components(ctx)
   generated_sprites: list[str] = []
   font = FontManager()
   for name, entry in vanilla.assets.item_models.items():
      squashed_model = squash_conditions(entry.data['model'])
      model_type = canon(squashed_model['type'])
      match model_type:
         case 'minecraft:model':
            model_name = squashed_model['model']
            model = vanilla.assets.models[model_name]
            tints = squashed_model.get('tints')
            layers = generated_layers(vanilla.assets.models, model)
            if layers is not None:
               for layer in layers:
                  font.add_sprite(canon(layer))
            else:
               gen_name = model_name + '.model'
               if gen_name not in generated_sprites:
                  render.add_model_task(
                     model=model_name,
                     path_ctx=gen_name,
                     animation_mode='one_file'
                  )
                  generated_sprites.append(gen_name)
         case 'minecraft:special':
            gen_name = name + '.item'
            if gen_name not in generated_sprites:
               render.add_item_task(
                  item=model_resolver.Item(id=name, components={'minecraft:item_model':name}),
                  path_ctx=gen_name,
                  animation_mode='one_file'
               )
               generated_sprites.append(gen_name)
         case _:
            print(name, squashed_model)
   render.run()
   generated_entries = [(ctx.assets.textures[x].image, x) for x in generated_sprites]
   grid_img, grid_refs = make_grid(generated_entries, render.default_render_size)
   for path in generated_sprites:
      del ctx.assets.textures[path]
   block_sheet_path = 'tryashtar.shulker_preview:block_sheet'
   ctx.assets.textures[block_sheet_path] = beet.Texture(grid_img)
   font.add_grid(block_sheet_path, grid_refs)
   ctx.assets.fonts['tryashtar.shulker_preview:preview'] = font.build()

def squash_conditions(model: dict) -> dict:
   model_type = canon(model['type'])
   match model_type:
      case 'minecraft:condition':
         prop = canon(model['property'])
         model['on_true'] = squash_conditions(model['on_true'])
         model['on_false'] = squash_conditions(model['on_false'])
         if model['on_true'] == model['on_false']:
            return model['on_true']
         match prop:
            case 'minecraft:bundle/has_selected_item' | 'minecraft:carried' | 'minecraft:extended_view' | 'minecraft:fishing_rod/cast' | 'minecraft:keybind_down' | 'minecraft:selected' | 'minecraft:using_item' | 'minecraft:view_entity':
               return model['on_false']
            case _:
               return model
      case 'minecraft:select':
         prop = canon(model['property'])
         if 'fallback' in model:
            model['fallback'] = squash_conditions(model['fallback'])
         for case in model['cases']:
            case['model'] = squash_conditions(case['model'])
         match prop:
            case 'minecraft:context_entity_type' | 'minecraft:local_time':
               return model['fallback']
            case 'minecraft:context_dimension':
               for case in model['cases']:
                  if case['when'] == 'minecraft:overworld' or 'minecraft:overworld' in case['when']:
                     return case['model']
               return model['fallback']
            case 'minecraft:display_context':
               for case in model['cases']:
                  if case['when'] == 'gui' or 'gui' in case['when']:
                     return case['model']
                  return model['fallback']
            case 'minecraft:main_hand':
               for case in model['cases']:
                  if case['when'] == 'right' or 'right' in case['when']:
                     return case['model']
                  return model['fallback']
            case _:
               return model
      case 'minecraft:range_dispatch':
         prop = canon(model['property'])
         if 'fallback' in model:
            model['fallback'] = squash_conditions(model['fallback'])
         for case in model['entries']:
            case['model'] = squash_conditions(case['model'])
         match prop:
            case 'minecraft:compass' | 'minecraft:cooldown' | 'minecraft:crossbow/pull' | 'minecraft:time' | 'minecraft:use_cycle' | 'minecraft:use_duration':
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
         providers.append({'type':'space','spaces':spaces})
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
