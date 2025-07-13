
def main(ctx: beet.Context):
   print("Creating functions...")
   all_items={i:"item" for i in mcitems.keys()}
   all_items.update({i:"block" for i in mcblocks.keys()})
   del all_items["broken_elytra"]
   del all_items["crossbow_arrow"]
   del all_items["crossbow_firework"]
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
      "execute store result score #length shulker_preview run data get block ~1 1 ~ RecordItem.id"
      ]
      lengths=list(length_dict.keys())
      lengths.sort()
      for length in lengths:
         lines.append(f"execute if score #length shulker_preview matches {length} run function tryashtar.shulker_preview:row_{row}/process_item/length_{length}")
         sublines=process_item_lines(length_dict[length], row)
         ctx.data.functions[f'tryashtar.shulker_preview:row_{row}/process_item/length_{length}'] = beet.Function(sublines)
      lines.extend([
         "",
         "# summon in count entity",
         "execute store result score #count shulker_preview run data get block ~1 1 ~ RecordItem.Count",
         f"execute if score #count shulker_preview matches 2.. run function tryashtar.shulker_preview:row_{row}/process_count"
         ])
      ctx.data.functions[f'tryashtar.shulker_preview:row_{row}/process_item'] = beet.Function(lines)

      # process_count
      lines=["# create an entity that draws item counts"]
      for i in range(2, 65):
         n = str(i) if i < 64 else f"{i}.."
         lines.append("execute if score #count shulker_preview matches "+n+" run summon area_effect_cloud ~ ~0.2 ~ {Tags:[\"tryashtar.shulker_preview\"],CustomName:'{\"translate\":\"tryashtar.shulker_preview.number."+str(i)+"."+str(row)+"\"}'}")
      ctx.data.functions[f'tryashtar.shulker_preview:row_{row}/process_count'] = beet.Function(lines)

      # process_durability
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
         text += " run summon area_effect_cloud ~ ~0.3 ~ {Tags:[\"tryashtar.shulker_preview\"],CustomName:'{\"translate\":\"tryashtar.shulker_preview.durability."+str(i)+"."+str(row)+"\"}'}"
         lines.append(text)
      ctx.data.functions[f'tryashtar.shulker_preview:row_{row}/process_durability'] = beet.Function(lines)

      # process_potion and process_arrow
      lines1=["# create an entity that draws the proper potion overlay color"]
      lines2=["# create an entity that draws the proper tipped arrow overlay color"]
      for potionname, colorname in potion_dict.items():
         lines1.append("execute if block ~1 1 ~ jukebox{RecordItem:{tag:{Potion:\"minecraft:"+potionname+"\"}}} run summon area_effect_cloud ~ ~0.1 ~ {Tags:[\"tryashtar.shulker_preview\"],CustomName:'{\"translate\":\"tryashtar.shulker_preview.overlay.potion_liquid."+colorname+"."+str(row)+"\"}'}")
         lines2.append("execute if block ~1 1 ~ jukebox{RecordItem:{tag:{Potion:\"minecraft:"+potionname+"\"}}} run summon area_effect_cloud ~ ~0.1 ~ {Tags:[\"tryashtar.shulker_preview\"],CustomName:'{\"translate\":\"tryashtar.shulker_preview.overlay.arrow_dust."+colorname+"."+str(row)+"\"}'}")
      ctx.data.functions[f'tryashtar.shulker_preview:row_{row}/process_potion'] = beet.Function(lines1)
      ctx.data.functions[f'tryashtar.shulker_preview:row_{row}/process_arrow'] = beet.Function(lines2)

   ctx.data.functions['tryashtar.shulker_preview:meta/player_online'] = beet.Function([
      'execute store result score #version shulker_preview run data get entity @a[limit=1] DataVersion',
      f'execute if score #version shulker_preview matches 1..{version_first['data']-1} run tellraw @a [{{"text":"\\nOutdated Minecraft version!\\nYou need to be on version ","color":"red"}},{{"text":"{version_first['version']}","color":"yellow"}},{{"text":" for shulker previews to work!"}}]',
      f'execute if score #version shulker_preview matches 1..{version_first['data']-1} run scoreboard players set #setup shulker_preview -1',
      f'execute if score #version shulker_preview matches {version_last['data']+1}.. run tellraw @a [{{"text":"\\nOutdated Shulker Preview version!\\nThis data pack is for version ","color":"red"}},{{"text":"{version_first['version']}","color":"yellow"}},{{"text":"!"}}]',
      f'execute if score #version shulker_preview matches {version_last['data']+1}.. run scoreboard players set #setup shulker_preview -1',
      f'execute if score #version shulker_preview matches {version_first['data']}..{version_last['data']} if score #setup shulker_preview matches -1 run scoreboard players set #setup shulker_preview 0',
      '',
      'scoreboard players add #setup shulker_preview 0',
      'execute if score #setup shulker_preview matches 0 run tellraw @a {"translate":"%1$s","with":[{"text":"\\nDon\'t forget to equip the resource pack!\\n","color":"red"},""]}',
      'execute if score #setup shulker_preview matches 0 run tellraw @a [{"text":"Successfully installed ","color":"green"},{"text":"tryashtar\'s","color":"blue","hoverEvent":{"action":"show_text","value":{"text":"(click to see more of my stuff)","color":"gray"}},"clickEvent":{"action":"open_url","value":"https://youtube.com/c/tryashtar"}},{"text":" Shulker Preview Pack!\\nThank you and enjoy.\\n\\n","color":"green"},{"text":"You can also click this text to add previews to Ender Chests.","color":"yellow","hoverEvent":{"action":"show_text","value":[{"text":"NOTE:\\n","color":"red"},{"text":"This is experimental and will prevent ender chests from stacking.","color":"gray"}]},"clickEvent":{"action":"run_command","value":"/function tryashtar.shulker_preview:meta/enable_ender"}}]',
      'execute if score #setup shulker_preview matches 0 run scoreboard players set #setup shulker_preview 1',
      '',
      'scoreboard players add #modded shulker_preview 0',
      'execute if score #modded shulker_preview matches 0 store success score #modded shulker_preview run data get entity @a[limit=1] "Spigot.ticksLived"',
      'execute if score #modded shulker_preview matches 0 store success score #modded shulker_preview run data get entity @a[limit=1] "Bukkit.updateLevel"',
      'execute if score #modded shulker_preview matches 0 store success score #modded shulker_preview run data get entity @a[limit=1] "Paper.SpawnReason"',
      '',
      'execute if score #modded shulker_preview matches 1 run tellraw @a {"text":"\\nModded server detected! There is no guarantee shulker previews will be compatible!","color":"red"}',
      'execute if score #modded shulker_preview matches 1 run scoreboard players set #modded shulker_preview 2',
   ])

# generates a very specific function
def process_item_lines(items, row):
   lines=[]
   potion=False
   durability=False
   arrow=False
   for item, itemtype in sorted(items, key=lambda x: x[0]):
      name="minecraft:"+item
      if item == "elytra":
         lines.extend([
            "execute if block ~1 1 ~ jukebox{RecordItem:{id:\"minecraft:elytra\",tag:{Damage:431}}} run summon area_effect_cloud ~ ~ ~ {Tags:[\"tryashtar.shulker_preview\"],CustomName:'{\"translate\":\"tryashtar.shulker_preview.item.broken_elytra."+str(row)+"\"}'}",
            "execute if block ~1 1 ~ jukebox{RecordItem:{id:\"minecraft:elytra\"}} unless block ~1 1 ~ jukebox{RecordItem:{id:\"minecraft:elytra\",tag:{Damage:431}}} run summon area_effect_cloud ~ ~ ~ {Tags:[\"tryashtar.shulker_preview\"],CustomName:'{\"translate\":\"tryashtar.shulker_preview.item.elytra."+str(row)+"\"}'}"
            ])
      elif item == "crossbow":
         lines.extend([
            "execute if block ~1 1 ~ jukebox{RecordItem:{id:\"minecraft:crossbow\",tag:{ChargedProjectiles:[{id:\"minecraft:arrow\"}]}}} run summon area_effect_cloud ~ ~ ~ {Tags:[\"tryashtar.shulker_preview\"],CustomName:'{\"translate\":\"tryashtar.shulker_preview.item.crossbow_arrow."+str(row)+"\"}'}",
            "execute if block ~1 1 ~ jukebox{RecordItem:{id:\"minecraft:crossbow\",tag:{ChargedProjectiles:[{id:\"minecraft:firework_rocket\"}]}}} run summon area_effect_cloud ~ ~ ~ {Tags:[\"tryashtar.shulker_preview\"],CustomName:'{\"translate\":\"tryashtar.shulker_preview.item.crossbow_firework."+str(row)+"\"}'}",
            "execute if block ~1 1 ~ jukebox{RecordItem:{id:\"minecraft:crossbow\"}} unless block ~1 1 ~ jukebox{RecordItem:{id:\"minecraft:crossbow\",tag:{ChargedProjectiles:[{}]}}} run summon area_effect_cloud ~ ~ ~ {Tags:[\"tryashtar.shulker_preview\"],CustomName:'{\"translate\":\"tryashtar.shulker_preview.item.crossbow."+str(row)+"\"}'}"
            ])
      else:
         lines.append("execute if block ~1 1 ~ jukebox{RecordItem:{id:\""+name+"\"}} run summon area_effect_cloud ~ ~ ~ {Tags:[\"tryashtar.shulker_preview\"],CustomName:'{\"translate\":\"tryashtar.shulker_preview."+itemtype+"."+item+"."+str(row)+"\"}'}")
      if item in ("potion","splash_potion","lingering_potion"):
         potion=True
      if item in durability_dict:
         lines.append("execute if block ~1 1 ~ jukebox{RecordItem:{id:\""+name+"\"}} run scoreboard players set #max shulker_preview "+str(durability_dict[item]))
         durability = True
      if item == "tipped_arrow":
         arrow = True
   if potion:
      lines.append("execute if data block ~1 1 ~ RecordItem.tag.Potion run function tryashtar.shulker_preview:row_"+str(row)+"/process_potion")
   if durability:
      lines.extend([
         "execute store result score #durability shulker_preview run data get block ~1 1 ~ RecordItem.tag.Damage",
         "execute if data block ~1 1 ~ RecordItem.tag.Damage run function tryashtar.shulker_preview:row_"+str(row)+"/process_durability"
         ])
   if arrow:
      lines.append("execute if data block ~1 1 ~ RecordItem.tag.Potion run function tryashtar.shulker_preview:row_"+str(row)+"/process_arrow")
   return lines
