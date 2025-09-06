import math
import typing
import re
import collections
import unicodedata
import dataclasses
import PIL.Image
import PIL.ImageChops
import beet

@dataclasses.dataclass
class Grid[T]:
   image: PIL.Image.Image
   entries: list[list[T | None]]

T = typing.TypeVar('T')
U = typing.TypeVar('U')
def make_grid(entries: dict[T, PIL.Image.Image], icon_size: int) -> Grid[T]:
   width, height = grid_dimensions(len(entries))
   image = PIL.Image.new('RGBA', (width * icon_size, height * icon_size))
   name_return: list[list[T | None]] = [[None] * width for _ in range(height)]
   for i, (name, sprite) in enumerate(entries.items()):
      pos_x = i % width
      pos_y = i // width
      name_return[pos_y][pos_x] = name
      x = pos_x * icon_size
      y = pos_y * icon_size
      image.paste(sprite, (x, y, x + icon_size, y + icon_size))
   return Grid(image=image, entries=name_return)

def map_2d(array: list[list[T]], fn: typing.Callable[[T], U]) -> list[list[U]]:
   result = []
   for entry in array:
      mapped = list(map(fn, entry))
      result.append(mapped)
   return result

def grid_dimensions(area: int) -> tuple[int, int]:
   width = math.ceil(math.sqrt(area))
   height = width
   if width * (height - 1) >= area:
      height -= 1
   return (width, height)

def rgba(color: int):
   r = color // 256 // 256 % 256
   g = color // 256 % 256
   b = color % 256
   return (r, g, b, 255)

def colorize(image: PIL.Image.Image, color) -> PIL.Image.Image:
   return PIL.ImageChops.multiply(image, PIL.Image.new('RGBA', image.size, color))

Identifier = str
ResourceLocation = str
JsonDict = dict[str, typing.Any]
NbtCompound = dict[str, typing.Any]

@dataclasses.dataclass
class LayeredModel:
   display: JsonDict
   overrides: list[JsonDict]
   layers: list[ResourceLocation]

@dataclasses.dataclass
class ElementModel:
   display: JsonDict
   overrides: list[JsonDict]
   elements: list[JsonDict]

@dataclasses.dataclass
class EntityModel:
   display: JsonDict
   overrides: list[JsonDict]

def model_data(source: beet.NamespaceProxy[beet.Model], model: beet.Model) -> LayeredModel | ElementModel | EntityModel:
   display: JsonDict = {}
   result: list[ResourceLocation | None] = []
   overrides = model.data.get('overrides', [])
   while True:
      if (model_display := model.data.get('display')) is not None:
         for key, value in model_display.items():
            if key not in display:
               display[key] = value
      if (elements := model.data.get('elements')) is not None:
         return ElementModel(display=display, overrides=overrides, elements=elements)
      if 'textures' in model.data:
         for name, path in model.data['textures'].items():
            match = re.match(r'layer(\d+)', name)
            if match:
               index = int(match.group(1))
               if index >= len(result):
                  result.extend([None] * (index - len(result) + 1))
               if result[index] is None:
                  result[index] = canon(path)
      if (parent := model.data.get('parent')) is not None:
         parent = canon(parent)
         if parent == 'minecraft:builtin/entity':
            return EntityModel(display=display, overrides=overrides)
         if parent == 'minecraft:builtin/generated':
            return LayeredModel(display=display, overrides=overrides, layers=[x for x in result if x is not None])
         model = source[parent]
         continue
      return LayeredModel(display=display, overrides=overrides, layers=[])

def canon(location: ResourceLocation) -> ResourceLocation:
   return f'minecraft:{location}' if ':' not in location else location

def short(location: ResourceLocation) -> ResourceLocation:
   return location.removeprefix('minecraft:')

K = typing.TypeVar('K')
V = typing.TypeVar('V')
def invert_dict(dictionary: dict[K, V]) -> dict[V, list[K]]:
   result: dict[V, list[K]] = collections.defaultdict(list)
   for key, value in dictionary.items():
      result[value].append(key)
   return dict(result)

Char = str

@dataclasses.dataclass
class GridData:
   rows: list[list[str]]
   negative: list[str]

@dataclasses.dataclass
class SpriteData:
   rows: list[str]
   negative: str

class FontManager:
   def __init__(self, rows: int):
      self.legacy_space_texture: ResourceLocation | None = None
      self.rows: int = rows
      self.upcoming_char: int = 1
      self.spaces: dict[int, Char] = {}
      self.sprites: dict[str, SpriteData] = {}
      self.grids: dict[str, GridData] = {}
      self.sprite_map: dict[str, SpriteData] = {}
      self.providers: list[JsonDict] = []
   
   def add_sprite(self, texture: ResourceLocation) -> SpriteData:
      if texture not in self.sprite_map:
         data = SpriteData(rows=[self.next_char() for _ in range(self.rows)], negative=self.next_char())
         self.sprites[texture + '.png'] = data
         self.sprite_map[texture] = data
      return self.sprite_map[texture]
   
   def add_grid(self, grid: ResourceLocation, textures: list[list[ResourceLocation | None]]) -> GridData:
      rows: list[list[str]] = [[] for _ in range(self.rows)]
      negative: list[str] = []
      for row in textures:
         for x in rows:
            x.append('')
         negative.append('')
         for texture in row:
            if texture is not None:
               rowchars = []
               for x in rows:
                  ch = self.next_char()
                  x[-1] += ch
                  rowchars.append(ch)
               n = self.next_char()
               negative[-1] += n
               self.sprite_map[texture] = SpriteData(rows=rowchars, negative=n)
            else:
               for x in rows:
                  x[-1] += '\u0000'
               negative[-1] += '\u0000'
      data = GridData(rows=rows, negative=negative)
      self.grids[grid + '.png'] = data
      return data
   
   def add_provider(self, provider: JsonDict):
      self.providers.append(provider)
      
   def get_sprite(self, name: str) -> SpriteData:
      return self.sprite_map[name]
   
   def next_char(self) -> Char:
      char = self.upcoming_char
      for low, high in [(0xd800, 0xdbff), (0xdc00, 0xdfff), (0x05c8, 0x05d2), (0x05e8, 0x06ff), (0x070b, 0x0710), (0x072d, 0x072f), (0x074b, 0x074f), (0x07a4, 0x07a5), (0x07b1, 0x07c2), (0x07f4, 0x07f5), (0x07fa, 0x07fc), (0x07fe, 0x0800), (0x082e, 0x0832), (0x083c, 0x0842), (0x0856, 0x0858), (0x085c, 0x0862), (0x0868, 0x0897), (0x08a0, 0x08a2), (0x08b2, 0x08b8), (0x08c5, 0x08c9), (0xfb34, 0xfb48), (0xfbbf, 0xfbd5), (0xfd8d, 0xfd94), (0xfdc5, 0xfdce), (0xfdf0, 0xfdf2), (0xfe72, 0xfe78), (0xfefa, 0xfefe)]:
         if low <= char <= high:
            char = high + 1
      while char in [0x0000, 0x000a, 0x00a7, 0x0025, 0x0590, 0x05be, 0x05c0, 0x05c3, 0x05c6, 0x0608, 0x060b, 0x060d, 0x0712, 0x081a, 0x0824, 0x0828, 0x200f, 0xfb1d, 0xfb1f] or unicodedata.bidirectional(chr(char)) in ['AL', 'R', 'NSM']:
         char += 1
      self.upcoming_char = char + 1
      return chr(char)
      
   def get_space(self, width: int) -> Char:
      if width in self.spaces:
         return self.spaces[width]
      char = self.next_char()
      self.spaces[width] = char
      return char
   
   def build(self) -> beet.Font:
      result = beet.Font()
      providers: list[JsonDict] = []
      if len(self.spaces) > 0:
         if self.legacy_space_texture is None:
            spaces = {}
            for width, char in self.spaces.items():
               spaces[char] = width
            providers.append({'type':'space','advances':spaces})
         else:
            for width, char in self.spaces.items():
               height = width - 1 if width >= 0 else width - 2
               providers.append({
                  'type':'bitmap',
                  'file': self.legacy_space_texture + '.png',
                  'ascent': -65536,
                  'height': height,
                  'chars': [char],
               })
      providers.extend(self.providers)
      for path, data in self.sprites.items():
         for row, entry in enumerate(data.rows):
            providers.append({'type':'bitmap','file':path,'ascent':-2 + (row * -18),'height':16,'chars':[entry]})
         providers.append({'type':'bitmap','file':path,'ascent':-32768,'height':-16,'chars':[data.negative]})
      for path, data in self.grids.items():
         for row, entry in enumerate(data.rows):
            providers.append({'type':'bitmap','file':path,'ascent':-2 + (row * -18),'height':16,'chars':entry})
         providers.append({'type':'bitmap','file':path,'ascent':-32768,'height':-16,'chars':data.negative})
      result.data['providers'] = providers
      return result

def add_tooltip(font: FontManager, texture: ResourceLocation, bottom: int) -> str:
   ascent = 8
   slices: list[tuple[int, list[int]]] = [(8, [0]), (8, [2,3,4,5,6,7,8,bottom])]
   text = ''
   for height, ranges in slices:
      for include in ranges:
         positive = ['\u0000'] * (256 // height)
         negative = ['\u0000'] * (256 // height)
         pos = font.next_char()
         neg = font.next_char()
         positive[include] = pos
         negative[include] = neg
         font.add_provider({
            'type': 'bitmap',
            'file': texture + '.png',
            'ascent': ascent,
            'height': height,
            'chars': positive
         })
         font.add_provider({
            'type': 'bitmap',
            'file': texture + '.png',
            'ascent': -32768,
            'height': -height,
            'chars': negative
         })
         ascent -= height
         text += pos + neg + get_space(font, -3)
   return text

@dataclasses.dataclass
class NumberData:
   normal: list[str]
   shadow: list[str]
   negative: str

def add_numbers(font: FontManager) -> list[NumberData]:
   result: list[NumberData] = []
   for _ in range(10):
      data = NumberData(
         normal=[font.next_char() for _ in range(font.rows)],
         shadow=[font.next_char() for _ in range(font.rows)],
         negative=font.next_char(),
      )
      result.append(data)
   empty_row = '\u0000' * 16
   negatives = ''.join([x.negative for x in result])
   for row in range(font.rows):
      normals = ''.join([x.normal[row] for x in result])
      shadows = ''.join([x.shadow[row] for x in result])
      def get_grid(numbers: str):
         return [*([empty_row] * 3), numbers + ('\u0000' * 6), *([empty_row] * 12)]
      font.add_provider({
         'type': 'bitmap',
         'file': 'minecraft:font/ascii.png',
         'ascent': -(18 * row) - 11,
         'height': 8,
         'chars': get_grid(normals)
      })
      font.add_provider({
         'type': 'bitmap',
         'file': 'minecraft:font/ascii.png',
         'ascent': -(18 * row) - 12,
         'height': 8,
         'chars': get_grid(shadows)
      })
      font.add_provider({
         'type': 'bitmap',
         'file': 'minecraft:font/ascii.png',
         'ascent': -32768,
         'height': -8,
         'chars': get_grid(negatives)
      })
   return result

def make_change(coins: list[int], target: int) -> dict[int, int]:
   queue: collections.deque[tuple[int, dict[int, int]]] = collections.deque([(0, {})])
   visited: set[int] = {0}
   while len(queue) > 0:
      current_total, used = queue.popleft()
      for coin in coins:
         new_total = current_total + coin
         new_used = used.copy()
         new_used[coin] = new_used.get(coin, 0) + 1
         if new_total == target:
            return new_used
         if new_total not in visited:
            visited.add(new_total)
            queue.append((new_total, new_used))
   raise ValueError(target)

def get_space(font: FontManager, width: int) -> str:
   coins = list(font.spaces.keys())
   change = make_change(coins, width)
   result = ''
   for entry, amount in change.items():
      result += font.spaces[entry] * amount
   return result
