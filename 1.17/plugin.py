import os
import re
import json
import math
import subprocess
import beet.contrib
import beet.contrib.vanilla
import copy
import model_resolver
import model_resolver.utils
import model_resolver.item_model.special
import numpy
import beet
from PIL import Image, ImageChops
from collections import OrderedDict

specials=["broken_elytra","crossbow_arrow","crossbow_firework","spawn_egg","spawn_egg_overlay","firework_star_overlay","leather_boots_overlay","leather_chestplate_overlay","leather_helmet_overlay","leather_leggings_overlay","potion_overlay","tipped_arrow_base","tipped_arrow_head","filled_map_markings","bundle_filled","light_00","light_01","light_02","light_03","light_04","light_05","light_06","light_07","light_08","light_09","light_10","light_11","light_12","light_13","light_14","light_15"]
def main(ctx: beet.Context):
   
   minecraft_version = '1.17'
   
   # load item textures from two sources
   print("Loading icons...")
   vanilla = beet.contrib.vanilla.Vanilla(ctx=ctx, minecraft_version=minecraft_version)
   vanilla_items = [x.removeprefix('minecraft:') for x in get_items(ctx, vanilla, minecraft_version).keys()]
   vanilla_items.extend(['broken_elytra','crossbow_arrow','crossbow_firework','spawn_egg','spawn_egg_overlay','firework_star_overlay','leather_boots_overlay','leather_leggings_overlay','leather_chestplate_overlay','leather_helmet_overlay','potion_overlay','tipped_arrow_base','tipped_arrow_head','filled_map_markings','dirt_path'])

   mcitems = {}
   for path, texture in vanilla.assets.textures.items():
      if 'item/' in path:
         itemname = path.split('/')[-1]
         if itemname in vanilla_items:
            mcitems[itemname] = texture.image.convert('RGBA')
   mcitems['clock'] = vanilla.assets.textures['minecraft:item/clock_00'].image.convert('RGBA')
   mcitems['compass'] = vanilla.assets.textures['minecraft:item/compass_00'].image.convert('RGBA')
   mcitems['crossbow'] = vanilla.assets.textures['minecraft:item/crossbow_standby'].image.convert('RGBA')
   mcitems['bundle_filled'] = vanilla.assets.textures['minecraft:item/bundle_filled'].image.convert('RGBA')
   mcitems['light_00'] = vanilla.assets.textures['minecraft:item/light_00'].image.convert('RGBA')
   mcitems['light_01'] = vanilla.assets.textures['minecraft:item/light_01'].image.convert('RGBA')
   mcitems['light_02'] = vanilla.assets.textures['minecraft:item/light_02'].image.convert('RGBA')
   mcitems['light_03'] = vanilla.assets.textures['minecraft:item/light_03'].image.convert('RGBA')
   mcitems['light_04'] = vanilla.assets.textures['minecraft:item/light_04'].image.convert('RGBA')
   mcitems['light_05'] = vanilla.assets.textures['minecraft:item/light_05'].image.convert('RGBA')
   mcitems['light_06'] = vanilla.assets.textures['minecraft:item/light_06'].image.convert('RGBA')
   mcitems['light_07'] = vanilla.assets.textures['minecraft:item/light_07'].image.convert('RGBA')
   mcitems['light_08'] = vanilla.assets.textures['minecraft:item/light_08'].image.convert('RGBA')
   mcitems['light_09'] = vanilla.assets.textures['minecraft:item/light_09'].image.convert('RGBA')
   mcitems['light_10'] = vanilla.assets.textures['minecraft:item/light_10'].image.convert('RGBA')
   mcitems['light_11'] = vanilla.assets.textures['minecraft:item/light_11'].image.convert('RGBA')
   mcitems['light_12'] = vanilla.assets.textures['minecraft:item/light_12'].image.convert('RGBA')
   mcitems['light_13'] = vanilla.assets.textures['minecraft:item/light_13'].image.convert('RGBA')
   mcitems['light_14'] = vanilla.assets.textures['minecraft:item/light_14'].image.convert('RGBA')
   mcitems['light_15'] = vanilla.assets.textures['minecraft:item/light_15'].image.convert('RGBA')
   
   for item in reused_textures:
      mcitems[item]="."
   for item in spawn_egg_colors:
      mcitems[item]="."
   mcitems["tipped_arrow"]="."
   
   blocknames = ['acacia_button','acacia_fence','acacia_fence_gate','acacia_leaves','acacia_log','acacia_planks','acacia_pressure_plate','acacia_slab','acacia_stairs','acacia_trapdoor','acacia_wood','amethyst_block','ancient_debris','andesite','andesite_slab','andesite_stairs','andesite_wall','anvil','azalea','azalea_leaves','barrel','basalt','beacon','bedrock','bee_nest','beehive','big_dripleaf','birch_button','birch_fence','birch_fence_gate','birch_leaves','birch_log','birch_planks','birch_pressure_plate','birch_slab','birch_stairs','birch_trapdoor','birch_wood','black_banner','black_bed','black_carpet','black_concrete','black_concrete_powder','black_glazed_terracotta','black_shulker_box','black_stained_glass','black_terracotta','black_wool','blackstone','blackstone_slab','blackstone_stairs','blackstone_wall','blast_furnace','blue_banner','blue_bed','blue_carpet','blue_concrete','blue_concrete_powder','blue_glazed_terracotta','blue_ice','blue_shulker_box','blue_stained_glass','blue_terracotta','blue_wool','bone_block','bookshelf','brain_coral_block','brick_slab','brick_stairs','brick_wall','bricks','brown_banner','brown_bed','brown_carpet','brown_concrete','brown_concrete_powder','brown_glazed_terracotta','brown_mushroom_block','brown_shulker_box','brown_stained_glass','brown_terracotta','brown_wool','bubble_coral_block','budding_amethyst','cactus','calcite','cartography_table','carved_pumpkin','chain_command_block','chest','chipped_anvil','chiseled_deepslate','chiseled_nether_bricks','chiseled_polished_blackstone','chiseled_quartz_block','chiseled_red_sandstone','chiseled_sandstone','chiseled_stone_bricks','chorus_flower','chorus_plant','clay','coal_block','coal_ore','coarse_dirt','cobbled_deepslate','cobbled_deepslate_slab','cobbled_deepslate_stairs','cobbled_deepslate_wall','cobblestone','cobblestone_slab','cobblestone_stairs','cobblestone_wall','command_block','composter','conduit','copper_block','copper_ore','cracked_deepslate_bricks','cracked_deepslate_tiles','cracked_nether_bricks','cracked_polished_blackstone_bricks','cracked_stone_bricks','crafting_table','creeper_head','crimson_button','crimson_fence','crimson_fence_gate','crimson_hyphae','crimson_nylium','crimson_planks','crimson_pressure_plate','crimson_slab','crimson_stairs','crimson_stem','crimson_trapdoor','crying_obsidian','cut_copper','cut_copper_slab','cut_copper_stairs','cut_red_sandstone','cut_red_sandstone_slab','cut_sandstone','cut_sandstone_slab','cyan_banner','cyan_bed','cyan_carpet','cyan_concrete','cyan_concrete_powder','cyan_glazed_terracotta','cyan_shulker_box','cyan_stained_glass','cyan_terracotta','cyan_wool','damaged_anvil','dark_oak_button','dark_oak_fence','dark_oak_fence_gate','dark_oak_leaves','dark_oak_log','dark_oak_planks','dark_oak_pressure_plate','dark_oak_slab','dark_oak_stairs','dark_oak_trapdoor','dark_oak_wood','dark_prismarine','dark_prismarine_slab','dark_prismarine_stairs','daylight_detector','dead_brain_coral_block','dead_bubble_coral_block','dead_fire_coral_block','dead_horn_coral_block','dead_tube_coral_block','deepslate','deepslate_brick_slab','deepslate_brick_stairs','deepslate_brick_wall','deepslate_bricks','deepslate_coal_ore','deepslate_copper_ore','deepslate_diamond_ore','deepslate_emerald_ore','deepslate_gold_ore','deepslate_iron_ore','deepslate_lapis_ore','deepslate_redstone_ore','deepslate_tile_slab','deepslate_tile_stairs','deepslate_tile_wall','deepslate_tiles','diamond_block','diamond_ore','diorite','diorite_slab','diorite_stairs','diorite_wall','dirt','dirt_path','dispenser','dragon_egg','dragon_head','dried_kelp_block','dripstone_block','dropper','emerald_block','emerald_ore','enchanting_table','end_portal_frame','end_rod','end_stone','end_stone_brick_slab','end_stone_brick_stairs','end_stone_brick_wall','end_stone_bricks','ender_chest','exposed_copper','exposed_cut_copper','exposed_cut_copper_slab','exposed_cut_copper_stairs','farmland','fire_coral_block','fletching_table','flowering_azalea','flowering_azalea_leaves','furnace','gilded_blackstone','glass','glowstone','gold_block','gold_ore','granite','granite_slab','granite_stairs','granite_wall','grass_block','gravel','gray_banner','gray_bed','gray_carpet','gray_concrete','gray_concrete_powder','gray_glazed_terracotta','gray_shulker_box','gray_stained_glass','gray_terracotta','gray_wool','green_banner','green_bed','green_carpet','green_concrete','green_concrete_powder','green_glazed_terracotta','green_shulker_box','green_stained_glass','green_terracotta','green_wool','grindstone','hay_block','heavy_weighted_pressure_plate','honey_block','honeycomb_block','horn_coral_block','ice','infested_chiseled_stone_bricks','infested_cobblestone','infested_cracked_stone_bricks','infested_deepslate','infested_mossy_stone_bricks','infested_stone','infested_stone_bricks','iron_block','iron_ore','iron_trapdoor','jack_o_lantern','jigsaw','jukebox','jungle_button','jungle_fence','jungle_fence_gate','jungle_leaves','jungle_log','jungle_planks','jungle_pressure_plate','jungle_slab','jungle_stairs','jungle_trapdoor','jungle_wood','lapis_block','lapis_ore','lectern','light_blue_banner','light_blue_bed','light_blue_carpet','light_blue_concrete','light_blue_concrete_powder','light_blue_glazed_terracotta','light_blue_shulker_box','light_blue_stained_glass','light_blue_terracotta','light_blue_wool','light_gray_banner','light_gray_bed','light_gray_carpet','light_gray_concrete','light_gray_concrete_powder','light_gray_glazed_terracotta','light_gray_shulker_box','light_gray_stained_glass','light_gray_terracotta','light_gray_wool','light_weighted_pressure_plate','lightning_rod','lime_banner','lime_bed','lime_carpet','lime_concrete','lime_concrete_powder','lime_glazed_terracotta','lime_shulker_box','lime_stained_glass','lime_terracotta','lime_wool','lodestone','loom','magenta_banner','magenta_bed','magenta_carpet','magenta_concrete','magenta_concrete_powder','magenta_glazed_terracotta','magenta_shulker_box','magenta_stained_glass','magenta_terracotta','magenta_wool','magma_block','melon','moss_block','moss_carpet','mossy_cobblestone','mossy_cobblestone_slab','mossy_cobblestone_stairs','mossy_cobblestone_wall','mossy_stone_brick_slab','mossy_stone_brick_stairs','mossy_stone_brick_wall','mossy_stone_bricks','mushroom_stem','mycelium','nether_brick_fence','nether_brick_slab','nether_brick_stairs','nether_brick_wall','nether_bricks','nether_gold_ore','nether_quartz_ore','nether_wart_block','netherite_block','netherrack','note_block','oak_button','oak_fence','oak_fence_gate','oak_leaves','oak_log','oak_planks','oak_pressure_plate','oak_slab','oak_stairs','oak_trapdoor','oak_wood','observer','obsidian','orange_banner','orange_bed','orange_carpet','orange_concrete','orange_concrete_powder','orange_glazed_terracotta','orange_shulker_box','orange_stained_glass','orange_terracotta','orange_wool','oxidized_copper','oxidized_cut_copper','oxidized_cut_copper_slab','oxidized_cut_copper_stairs','packed_ice','petrified_oak_slab','pink_banner','pink_bed','pink_carpet','pink_concrete','pink_concrete_powder','pink_glazed_terracotta','pink_shulker_box','pink_stained_glass','pink_terracotta','pink_wool','piston','player_head','podzol','polished_andesite','polished_andesite_slab','polished_andesite_stairs','polished_basalt','polished_blackstone','polished_blackstone_brick_slab','polished_blackstone_brick_stairs','polished_blackstone_brick_wall','polished_blackstone_bricks','polished_blackstone_button','polished_blackstone_pressure_plate','polished_blackstone_slab','polished_blackstone_stairs','polished_blackstone_wall','polished_deepslate','polished_deepslate_slab','polished_deepslate_stairs','polished_deepslate_wall','polished_diorite','polished_diorite_slab','polished_diorite_stairs','polished_granite','polished_granite_slab','polished_granite_stairs','prismarine','prismarine_brick_slab','prismarine_brick_stairs','prismarine_bricks','prismarine_slab','prismarine_stairs','prismarine_wall','pumpkin','purple_banner','purple_bed','purple_carpet','purple_concrete','purple_concrete_powder','purple_glazed_terracotta','purple_shulker_box','purple_stained_glass','purple_terracotta','purple_wool','purpur_block','purpur_pillar','purpur_slab','purpur_stairs','quartz_block','quartz_bricks','quartz_pillar','quartz_slab','quartz_stairs','raw_copper_block','raw_gold_block','raw_iron_block','red_banner','red_bed','red_carpet','red_concrete','red_concrete_powder','red_glazed_terracotta','red_mushroom_block','red_nether_brick_slab','red_nether_brick_stairs','red_nether_brick_wall','red_nether_bricks','red_sand','red_sandstone','red_sandstone_slab','red_sandstone_stairs','red_sandstone_wall','red_shulker_box','red_stained_glass','red_terracotta','red_wool','redstone_block','redstone_lamp','redstone_ore','repeating_command_block','respawn_anchor','rooted_dirt','sand','sandstone','sandstone_slab','sandstone_stairs','sandstone_wall','scaffolding','sculk_sensor','sea_lantern','shield','shroomlight','shulker_box','skeleton_skull','slime_block','small_dripleaf','smithing_table','smoker','smooth_basalt','smooth_quartz','smooth_quartz_slab','smooth_quartz_stairs','smooth_red_sandstone','smooth_red_sandstone_slab','smooth_red_sandstone_stairs','smooth_sandstone','smooth_sandstone_slab','smooth_sandstone_stairs','smooth_stone','smooth_stone_slab','snow','snow_block','soul_sand','soul_soil','spawner','sponge','spore_blossom','spruce_button','spruce_fence','spruce_fence_gate','spruce_leaves','spruce_log','spruce_planks','spruce_pressure_plate','spruce_slab','spruce_stairs','spruce_trapdoor','spruce_wood','sticky_piston','stone','stone_brick_slab','stone_brick_stairs','stone_brick_wall','stone_bricks','stone_button','stone_pressure_plate','stone_slab','stone_stairs','stonecutter','stripped_acacia_log','stripped_acacia_wood','stripped_birch_log','stripped_birch_wood','stripped_crimson_hyphae','stripped_crimson_stem','stripped_dark_oak_log','stripped_dark_oak_wood','stripped_jungle_log','stripped_jungle_wood','stripped_oak_log','stripped_oak_wood','stripped_spruce_log','stripped_spruce_wood','stripped_warped_hyphae','stripped_warped_stem','structure_block','target','terracotta','tinted_glass','tnt','trapped_chest','tube_coral_block','tuff','warped_button','warped_fence','warped_fence_gate','warped_hyphae','warped_nylium','warped_planks','warped_pressure_plate','warped_slab','warped_stairs','warped_stem','warped_trapdoor','warped_wart_block','waxed_copper_block','waxed_cut_copper','waxed_cut_copper_slab','waxed_cut_copper_stairs','waxed_exposed_copper','waxed_exposed_cut_copper','waxed_exposed_cut_copper_slab','waxed_exposed_cut_copper_stairs','waxed_oxidized_copper','waxed_oxidized_cut_copper','waxed_oxidized_cut_copper_slab','waxed_oxidized_cut_copper_stairs','waxed_weathered_copper','waxed_weathered_cut_copper','waxed_weathered_cut_copper_slab','waxed_weathered_cut_copper_stairs','weathered_copper','weathered_cut_copper','weathered_cut_copper_slab','weathered_cut_copper_stairs','wet_sponge','white_banner','white_bed','white_carpet','white_concrete','white_concrete_powder','white_glazed_terracotta','white_shulker_box','white_stained_glass','white_terracotta','white_wool','wither_skeleton_skull','yellow_banner','yellow_bed','yellow_carpet','yellow_concrete','yellow_concrete_powder','yellow_glazed_terracotta','yellow_shulker_box','yellow_stained_glass','yellow_terracotta','yellow_wool','zombie_head']
   
   banner = model_resolver.item_model.special.SpecialModelBanner(type='banner', color='red')
   for entry in blocknames:
      if 'shulker_box' in entry:
         tx = ('shulker_' + entry.removesuffix('shulker_box')).removesuffix('_')
         sbox = model_resolver.item_model.special.SpecialModelShulkerBox(type='shulker_box', texture=tx)
         model = sbox.get_model(None, None)
         ctx.assets.models[f'minecraft:item/{entry}'] = beet.Model(model)
      if 'banner' in entry:
         color = '_'.join(entry.split('_')[:-1])
         display = vanilla.assets.models['minecraft:item/template_banner'].data
         model = banner.get_model(None, None)
         model['display'] = display['display']
         model['textures']['0'] = f'render:banner_{color}'
         ctx.assets.models[f'minecraft:item/{entry}'] = beet.Model(model)
      if '_bed' in entry:
         bed = model_resolver.item_model.special.SpecialModelBed(type='bed', texture=entry.removesuffix('_bed'))
         display = vanilla.assets.models['minecraft:item/template_bed'].data
         model = bed.get_model(None, None)
         model['display'] = display['display']
         ctx.assets.models[f'minecraft:item/{entry}'] = beet.Model(model)
      if '_head' in entry or '_skull' in entry:
         if entry == 'player_head':
            model = {"textures":{"1":"minecraft:entity/steve"},"elements":[{"from":[4, 0, 4],"to":[12, 8, 12],"rotation":{"angle":0,"axis":"y","origin":[8, 8, 8]},"faces":{"north":{"uv":[6, 2, 8, 4],"texture":"#1"},"east":{"uv":[4, 2, 6, 4],"texture":"#1"},"south":{"uv":[2, 2, 4, 4],"texture":"#1"},"west":{"uv":[0, 2, 2, 4],"texture":"#1"},"up":{"uv":[2, 0, 4, 2],"rotation":180,"texture":"#1"},"down":{"uv":[4, 0, 6, 2],"rotation":180,"texture":"#1"}}},{"from":[3.75, -0.25, 3.75],"to":[12.25, 8.25, 12.25],"rotation":{"angle":0,"axis":"y","origin":[8, 8, 8]},"faces":{"north":{"uv":[14, 2, 16, 4],"texture":"#1"},"east":{"uv":[12, 2, 14, 4],"texture":"#1"},"south":{"uv":[10, 2, 12, 4],"texture":"#1"},"west":{"uv":[8, 2, 10, 4],"texture":"#1"},"up":{"uv":[10, 0, 12, 2],"rotation":180,"texture":"#1"},"down":{"uv":[12, 0, 14, 2],"rotation":180,"texture":"#1"}}}]}
         else:
            head = model_resolver.item_model.special.SpecialModelHead(type='head', kind=entry.removesuffix('_head').removesuffix('_skull'))
            model = head.get_model(None, None)
         if entry == 'dragon_head':
            display = copy.deepcopy(vanilla.assets.models['minecraft:item/dragon_head'].data)
            model['display'] = display['display']
            model['display']['gui']['scale'] = [0.6 * 0.75, 0.6 * 0.75, 0.6 * 0.75]
         else:
            display = copy.deepcopy(vanilla.assets.models['minecraft:item/template_skull'].data)
            model['display'] = display['display']
         ctx.assets.models[f'minecraft:item/{entry}'] = beet.Model(model)
      if entry == 'conduit':
         conduit = model_resolver.item_model.special.SpecialModelConduit(type='conduit')
         display = vanilla.assets.models['minecraft:item/conduit'].data
         model = conduit.get_model(None, None)
         model['display'] = display['display']
         ctx.assets.models[f'minecraft:item/{entry}'] = beet.Model(model)
      if entry == 'shield':
         shield = model_resolver.item_model.special.SpecialModelShield(type='shield')
         display = vanilla.assets.models['minecraft:item/shield'].data
         model = shield.get_model(None, model_resolver.Item(id='shield', components={}))
         model['display'] = display['display']
         ctx.assets.models[f'minecraft:item/{entry}'] = beet.Model(model)
      if 'chest' in entry:
         tx = {'chest':'normal','trapped_chest':'trapped','ender_chest':'ender'}[entry]
         chest = model_resolver.item_model.special.SpecialModelChest(type='chest', texture=tx, openness=0)
         display = vanilla.assets.models['minecraft:item/chest'].data
         model = chest.get_model(None, None)
         model['display'] = display['display']
         ctx.assets.models[f'minecraft:item/{entry}'] = beet.Model(model)

   ctx.assets.textures['minecraft:block/grass_block_top'] = beet.Texture(colorize(vanilla.assets.textures['minecraft:block/grass_block_top'].image, rgba(0x7bbd6b)))
   banner_base = vanilla.assets.textures['minecraft:entity/banner_base'].image.convert('RGBA')
   banner_base2 = vanilla.assets.textures['minecraft:entity/banner/base'].image.convert('RGBA')
   for n,color in banner.COLOR_STRING_TO_ARGB.items():
      final = Image.new('RGBA', banner_base.size)
      final.paste(banner_base, (0, 0))
      colored = colorize(banner_base2, rgba(color))
      final.paste(colored, (0, 0), colored)
      ctx.assets.textures[f'render:banner_{n}'] = beet.Texture(final)
      
   mcbanners={}
   mcshields={}
   
   banner_patterns = ['base','border','bricks','circle','creeper','cross','curly_border','diagonal_left','diagonal_right','diagonal_up_left','diagonal_up_right','flower','globe','gradient','gradient_up','half_horizontal','half_horizontal_bottom','half_vertical','half_vertical_right','mojang','piglin','rhombus','skull','small_stripes','square_bottom_left','square_bottom_right','square_top_left','square_top_right','straight_cross','stripe_bottom','stripe_center','stripe_downleft','stripe_downright','stripe_left','stripe_middle','stripe_right','stripe_top','triangle_bottom','triangle_top','triangles_bottom','triangles_top']
   for pattern in banner_patterns:
      banner_texture = f'entity/banner/{pattern}'
      shield_texture = f'entity/shield/{pattern}'
      fake_banner = {"parent":"minecraft:item/template_banner","textures":{"0":banner_texture},"elements":[{"from":[8.66667, 2.66667, 1.33333],"to":[9.66667, 29.33333, 14.66667],"rotation":{"angle":-90,"axis":"y","origin":[8, 0, 8]},"faces":{"north":{"uv":[5.25, 0.25, 5.5, 10.25],"texture":"#0"},"east":{"uv":[0.25, 0.25, 5.25, 10.25],"texture":"#0"},"south":{"uv":[0, 0.25, 0.25, 10.25],"texture":"#0"},"west":{"uv":[5.5, 0.25, 10.5, 10.25],"texture":"#0"},"up":{"uv":[5.25, 0, 0.25, 0.25],"rotation":90,"texture":"#0"},"down":{"uv":[10.25, 0, 5.25, 0.25],"rotation":270,"texture":"#0"}}}]}
      fake_shield = {"parent":"minecraft:item/shield","textures":{"0":shield_texture},"elements":[{"from":[-6, -11, 1],"to":[6, 11, 2],"faces":{"south":{"uv":[0.25, 0.25, 3.25, 5.75],"texture":"#0"}}}]}
      ctx.assets.models[f'render:banner_{pattern}'] = beet.Model(fake_banner)
      ctx.assets.models[f'render:shield_{pattern}'] = beet.Model(fake_shield)
      
   renderer = model_resolver.Render(ctx=ctx)
   renderer.default_render_size = 64
   for entry in blocknames:         
      renderer.add_model_task(
         model=f'minecraft:item/{entry}',
         path_ctx=f'render:{entry}',
         animation_mode = 'one_file'
      )
   for pattern in banner_patterns:         
      renderer.add_model_task(
         model=f'render:banner_{pattern}',
         path_ctx=f'render:banner_{pattern}',
         animation_mode = 'one_file'
      )
      renderer.add_model_task(
         model=f'render:shield_{pattern}',
         path_ctx=f'render:shield_{pattern}',
         animation_mode = 'one_file'
      )
   renderer.run()
   del ctx.assets.textures['minecraft:block/grass_block_top']
   for n,color in banner.COLOR_STRING_TO_ARGB.items():
      del ctx.assets.textures[f'render:banner_{n}']
   
   mcblocks = {}
   for entry in blocknames:
      tx = ctx.assets.textures[f'render:{entry}'].image.convert('RGBA')
      color = {"acacia_leaves":0x48b518,"birch_leaves":0x80a755,"dark_oak_leaves":0x48b518,"fern":0x7bbd6b,"jungle_leaves":0x48b518,"large_fern":0x7bbd6b,"lily_pad":0x71c35c,"oak_leaves":0x48b518,"grass":0x7bbd6b,"spruce_leaves":0x619961,"tall_grass":0x7bbd6b,"vine":0x48b518}.get(entry)
      if color is not None:
         tx = colorize(tx, rgba(color))
      mcblocks[entry] = tx
      del ctx.assets.textures[f'render:{entry}']
      if f'minecraft:item/{entry}' in ctx.assets.models:
         del ctx.assets.models[f'minecraft:item/{entry}']
   for pattern in banner_patterns:
      if pattern != 'base':
         mcbanners[pattern] = ctx.assets.textures[f'render:banner_{pattern}'].image.convert('RGBA')
      mcshields[pattern] = ctx.assets.textures[f'render:shield_{pattern}'].image.convert('RGBA')
      del ctx.assets.textures[f'render:banner_{pattern}']
      del ctx.assets.textures[f'render:shield_{pattern}']
   
   for model in list(ctx.assets.models.keys()):
      del ctx.assets.models[model]
      
   blockitems=["acacia_sapling","activator_rail","allium","azure_bluet","birch_sapling","black_stained_glass_pane","blue_orchid","blue_stained_glass_pane","brain_coral","brain_coral_fan","brown_mushroom","brown_stained_glass_pane","bubble_coral","bubble_coral_fan","cobweb","cornflower","crimson_fungus","crimson_roots","cyan_stained_glass_pane","dandelion","dark_oak_sapling","dead_brain_coral","dead_brain_coral_fan","dead_bubble_coral","dead_bubble_coral_fan","dead_bush","dead_fire_coral","dead_fire_coral_fan","dead_horn_coral","dead_horn_coral_fan","dead_tube_coral","dead_tube_coral_fan","detector_rail","fern","fire_coral","fire_coral_fan","glass_pane","grass","gray_stained_glass_pane","green_stained_glass_pane","horn_coral","horn_coral_fan","iron_bars","jungle_sapling","ladder","large_fern","lever","light_blue_stained_glass_pane","light_gray_stained_glass_pane","lilac","lily_of_the_valley","lily_pad","lime_stained_glass_pane","magenta_stained_glass_pane","nether_sprouts","oak_sapling","orange_stained_glass_pane","orange_tulip","oxeye_daisy","peony","pink_stained_glass_pane","pink_tulip","poppy","powered_rail","purple_stained_glass_pane","rail","redstone_torch","red_mushroom","red_stained_glass_pane","red_tulip","rose_bush","soul_torch","spruce_sapling","sunflower","tall_grass","torch","tripwire_hook","tube_coral","tube_coral_fan","twisting_vines","vine","warped_fungus","warped_roots","weeping_vines","white_stained_glass_pane","white_tulip","wither_rose","yellow_stained_glass_pane","small_amethyst_bud","medium_amethyst_bud","large_amethyst_bud","amethyst_cluster","hanging_roots","glow_lichen"]
   for blockitem in blockitems:
      mcitems[blockitem]="block"

   mcitems=dict(sorted(mcitems.items()))
   mcblocks=dict(sorted(mcblocks.items()))
   mcbanners=dict(sorted(mcbanners.items()))
   mcshields=dict(sorted(mcshields.items()))

   mc_block_textures={}
   for k,v in mcblocks.items():
      mc_block_textures[k]=v
   for k,v in mcbanners.items():
      mc_block_textures[f"banner_pattern.{k}"]=v
   for k,v in mcshields.items():
      mc_block_textures[f"shield_pattern.{k}"]=v

   # create grids
   print("Creating image sheets...")
   blockgrid=create_grid(mc_block_textures)
   blocksheet=create_image(blockgrid, 64)
   ctx.assets.textures['tryashtar.shulker_preview:block_sheet'] = beet.Texture(blocksheet)

   # start creating font providers
   print("Generating font providers...")
   providers=[{"comment":"Many thanks to AmberW#4615 for this invaluable concept","type":"bitmap","file":"tryashtar.shulker_preview:pixel.png","ascent":-32768,"height":-3,"chars":["\uf801"]},{"type":"bitmap","file":"tryashtar.shulker_preview:pixel.png","ascent":-32768,"height":-4,"chars":["\uf802"]},{"type":"bitmap","file":"tryashtar.shulker_preview:pixel.png","ascent":-32768,"height":-5,"chars":["\uf803"]},{"type":"bitmap","file":"tryashtar.shulker_preview:pixel.png","ascent":-32768,"height":-6,"chars":["\uf804"]},{"type":"bitmap","file":"tryashtar.shulker_preview:pixel.png","ascent":-32768,"height":-7,"chars":["\uf805"]},{"type":"bitmap","file":"tryashtar.shulker_preview:pixel.png","ascent":-32768,"height":-8,"chars":["\uf806"]},{"type":"bitmap","file":"tryashtar.shulker_preview:pixel.png","ascent":-32768,"height":-9,"chars":["\uf807"]},{"type":"bitmap","file":"tryashtar.shulker_preview:pixel.png","ascent":-32768,"height":-10,"chars":["\uf808"]},{"type":"bitmap","file":"tryashtar.shulker_preview:pixel.png","ascent":-32768,"height":-18,"chars":["\uf809"]},{"type":"bitmap","file":"tryashtar.shulker_preview:pixel.png","ascent":-32768,"height":-34,"chars":["\uf80a"]},{"type":"bitmap","file":"tryashtar.shulker_preview:pixel.png","ascent":-32768,"height":-66,"chars":["\uf80b"]},{"type":"bitmap","file":"tryashtar.shulker_preview:pixel.png","ascent":-32768,"height":-130,"chars":["\uf80c"]},{"type":"bitmap","file":"tryashtar.shulker_preview:pixel.png","ascent":-32768,"height":-258,"chars":["\uf80d"]},{"type":"bitmap","file":"tryashtar.shulker_preview:pixel.png","ascent":-32768,"height":-514,"chars":["\uf80e"]},{"type":"bitmap","file":"tryashtar.shulker_preview:pixel.png","ascent":-32768,"height":-1026,"chars":["\uf80f"]},{"type":"bitmap","file":"tryashtar.shulker_preview:pixel.png","ascent":-32768,"height":0,"chars":["\uf821"]},{"type":"bitmap","file":"tryashtar.shulker_preview:pixel.png","ascent":-32768,"height":1,"chars":["\uf822"]},{"type":"bitmap","file":"tryashtar.shulker_preview:pixel.png","ascent":-32768,"height":2,"chars":["\uf823"]},{"type":"bitmap","file":"tryashtar.shulker_preview:pixel.png","ascent":-32768,"height":3,"chars":["\uf824"]},{"type":"bitmap","file":"tryashtar.shulker_preview:pixel.png","ascent":-32768,"height":4,"chars":["\uf825"]},{"type":"bitmap","file":"tryashtar.shulker_preview:pixel.png","ascent":-32768,"height":5,"chars":["\uf826"]},{"type":"bitmap","file":"tryashtar.shulker_preview:pixel.png","ascent":-32768,"height":6,"chars":["\uf827"]},{"type":"bitmap","file":"tryashtar.shulker_preview:pixel.png","ascent":-32768,"height":7,"chars":["\uf828"]},{"type":"bitmap","file":"tryashtar.shulker_preview:pixel.png","ascent":-32768,"height":15,"chars":["\uf829"]},{"type":"bitmap","file":"tryashtar.shulker_preview:pixel.png","ascent":-32768,"height":31,"chars":["\uf82a"]},{"type":"bitmap","file":"tryashtar.shulker_preview:pixel.png","ascent":-32768,"height":63,"chars":["\uf82b"]},{"type":"bitmap","file":"tryashtar.shulker_preview:pixel.png","ascent":-32768,"height":127,"chars":["\uf82c"]},{"type":"bitmap","file":"tryashtar.shulker_preview:pixel.png","ascent":-32768,"height":255,"chars":["\uf82d"]},{"type":"bitmap","file":"tryashtar.shulker_preview:pixel.png","ascent":-32768,"height":511,"chars":["\uf82e"]},{"type":"bitmap","file":"tryashtar.shulker_preview:pixel.png","ascent":-32768,"height":1023,"chars":["\uf82f"]},{"type":"bitmap","file":"tryashtar.shulker_preview:pixel.png","ascent":-32770,"height":-32770,"chars":["\uf800"]},{"type":"bitmap","file":"tryashtar.shulker_preview:pixel.png","ascent":-32768,"height":32767,"chars":["\uf820"]}]
   providers.append(register_single("tryashtar.shulker_preview:shulker_tooltip.png","shulker_tooltip", 23, 78, (get_spacing(-4),get_spacing(-169))))
   providers.append(register_single("tryashtar.shulker_preview:shulker_tooltip_header.png","shulker_tooltip_header", 23, 78, (get_spacing(-4),get_spacing(-169))))
   providers.append(register_single("tryashtar.shulker_preview:ender_tooltip.png","ender_tooltip", 23, 78, (get_spacing(-4),get_spacing(-169))))

   providers.extend(register_items(mcitems, 0, -32768, 16, False))
   # per-row icons
   for row in range(0, 3):
      height=-18*row
      # numbers 0-9
      numbers=[f"number.{i}.{row}" for i in range(0,10)]
      providers.append(register_grid("tryashtar.shulker_preview:numbers.png", [numbers], height-4, 8, lambda x:(get_spacing(-7),get_spacing(0))))
      # numbers 10-64 (built out of two digits)
      for n in range(10, 65):
         digit1=str(n)[0]
         digit2=str(n)[1]
         translations[f"tryashtar.shulker_preview.number.{n}.{row}"]=get_spacing(-13)+charmap[f"number.{digit1}.{row}"]+get_spacing(-1)+charmap[f"number.{digit2}.{row}"]+get_spacing(0)
      dur1=[f"durability.{i}.{row}" for i in range(1,6)]
      dur2=[f"durability.{i}.{row}" for i in range(6,11)]
      dur3=[f"durability.{i}.{row}" for i in range(11,15)]+[None]
      providers.append(register_grid("tryashtar.shulker_preview:durability.png", [dur1,dur2,dur3], height-8, 2, lambda x:(get_spacing(-16),get_spacing(2))))

      # grids
      providers.append(register_grid("tryashtar.shulker_preview:block_sheet.png", apply_to_all(grid_keys(blockgrid), lambda x: block_translation(x,row)), height+5, 16, lambda x: block_spacing(x)))
      providers.extend(register_items(mcitems, row, height+5, 16, True))


   # write translations and providers
   print("Writing JSONs...")
   ctx.assets.languages['tryashtar.shulker_preview:en_us'] = beet.Language(translations)
   ctx.assets.fonts['tryashtar.shulker_preview:preview'] = beet.Font({"providers":providers})

   # create dictionary of item lengths
   print("Creating functions...")
   all_items={i:"item" for i in mcitems.keys()}
   all_items.update({i:"block" for i in mcblocks.keys()})
   for texture in specials:
      del all_items[texture]
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
      "execute store result score #length shulker_preview run data get storage tryashtar.shulker_preview:data item.id"
      ]
      lengths=list(length_dict.keys())
      lengths.sort()
      for length in lengths:
         fpath=f"tryashtar.shulker_preview:row_{row}/process_item/length_{length}"
         lines.append(f"execute if score #length shulker_preview matches {length} run function tryashtar.shulker_preview:row_{row}/process_item/length_{length}")
         sublines=process_item_lines(length_dict[length], row)
         ctx.data.functions[fpath] = beet.Function(sublines)

      lines.extend([
         "",
         "# placeholder if item was not found",
         f'execute unless entity @e[type=marker,tag=tryashtar.shulker_preview,distance=..0.0001] run summon marker ~ ~ ~ {{Tags:["tryashtar.shulker_preview"],CustomName:\'{{"translate":"tryashtar.shulker_preview.item.missingno.{row}"}}\'}}',
         "",
         "# summon in count entity",
         "execute store result score #count shulker_preview run data get storage tryashtar.shulker_preview:data item.Count",
         f"execute if score #count shulker_preview matches 2.. run function tryashtar.shulker_preview:row_{row}/overlay/count"
         ])
      ctx.data.functions[f"tryashtar.shulker_preview:row_{row}/process_item"] = beet.Function(lines)

      # item count overlay
      lines=["# create an entity that draws item counts"]
      for i in range(2, 65):
         n = str(i) if i < 64 else f"{i}.."
         lines.append(f'execute if score #count shulker_preview matches {n} run summon marker ~ ~0.9 ~ {{Tags:["tryashtar.shulker_preview"],CustomName:\'{{"translate":"tryashtar.shulker_preview.number.{i}.{row}"}}\'}}')
      ctx.data.functions[f'tryashtar.shulker_preview:row_{row}/overlay/count'] = beet.Function(lines)

      # overlay/durability
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
         text += f' run summon marker ~ ~0.8 ~ {{Tags:["tryashtar.shulker_preview"],CustomName:\'{{"translate":"tryashtar.shulker_preview.durability.{i}.{row}"}}\'}}'
         lines.append(text)
      ctx.data.functions[f'tryashtar.shulker_preview:row_{row}/overlay/durability'] = beet.Function(lines)

      # potion and arrow overlays
      potion_lines=["# create an entity that draws the proper potion overlay color"]
      arrow_lines=["# create an entity that draws the proper tipped arrow overlay color"]
      for potionname, color in potion_dict.items():
         if_item=f'execute if data storage tryashtar.shulker_preview:data item{{tag:{{Potion:"minecraft:{potionname}"}}}}'
         potion_lines.append(f'{if_item} run summon marker ~ ~0.1 ~ {{Tags:["tryashtar.shulker_preview"],CustomName:\'{{"translate":"tryashtar.shulker_preview.overlay.potion_overlay.{row}","color":"{color_hex(color)}"}}\'}}')
         arrow_lines.append(f'{if_item} run summon marker ~ ~0.3 ~ {{Tags:["tryashtar.shulker_preview"],CustomName:\'{{"translate":"tryashtar.shulker_preview.overlay.tipped_arrow_head.{row}","color":"{color_hex(color)}"}}\'}}')

      custom_potion_lines=[
         f'# create an entity that draws approximately the correct overlay color',
         f'execute store result score #color shulker_preview run data get storage tryashtar.shulker_preview:data item.tag.CustomPotionColor',
         f'function tryashtar.shulker_preview:row_{row}/analyze_color'
      ]
      custom_arrow_lines=custom_potion_lines.copy()

      # banner patterns
      banner_lines=[
         f'# recursively draw all banner patterns',
         f'function tryashtar.shulker_preview:row_{row}/overlay/banner_pattern',
         f'data remove storage tryashtar.shulker_preview:data item.tag.BlockEntityTag.Patterns[0]',
         f'execute if data storage tryashtar.shulker_preview:data item.tag.BlockEntityTag.Patterns[0] positioned ~ ~0.01 ~ run function tryashtar.shulker_preview:row_{row}/overlay/banner',
      ]
      shield_base=[
         f'# draw shield base and patterns'
      ]
      shield_lines=[
         f'# recursively draw all banner patterns',
         f'function tryashtar.shulker_preview:row_{row}/overlay/shield_pattern',
         f'data remove storage tryashtar.shulker_preview:data item.tag.BlockEntityTag.Patterns[0]',
         f'execute if data storage tryashtar.shulker_preview:data item.tag.BlockEntityTag.Patterns[0] positioned ~ ~0.01 ~ run function tryashtar.shulker_preview:row_{row}/overlay/shield',
      ]
      banner_pattern_lines=[
         f'# create an entity that draws a banner pattern overlay',
         f'data modify storage tryashtar.shulker_preview:data pattern set from storage tryashtar.shulker_preview:data item.tag.BlockEntityTag.Patterns[0]'
      ]
      shield_pattern_lines=banner_pattern_lines.copy()
      for cid,cname in int_colors.items():
         chex=dye_colors[cname]
         shield_base.append(f'execute if data storage tryashtar.shulker_preview:data item.tag.BlockEntityTag{{Base:{cid}}} run summon marker ~ ~0.01 ~ {{Tags:["tryashtar.shulker_preview"],CustomName:\'{{"translate":"tryashtar.shulker_preview.shield_pattern.base.{row}","color":"#{chex}"}}\'}}')
         banner_pattern_lines.append(f'execute if data storage tryashtar.shulker_preview:data pattern{{Color:{cid}}} run function tryashtar.shulker_preview:row_{row}/overlay/banner/{cname}')
         shield_pattern_lines.append(f'execute if data storage tryashtar.shulker_preview:data pattern{{Color:{cid}}} run function tryashtar.shulker_preview:row_{row}/overlay/shield/{cname}')
         single_b_pattern_lines=[]
         single_s_pattern_lines=[]
         for i,(pid,pname) in enumerate(banner_pattern_ids.items()):
            line=f'execute if data storage tryashtar.shulker_preview:data pattern{{Pattern:"{pid}"}} run summon marker ~ ~{round((i+1)*0.0001,4)} ~ {{Tags:["tryashtar.shulker_preview"],CustomName:\'{{"translate":"tryashtar.shulker_preview.banner_pattern.{pname}.{row}","color":"#{chex}"}}\'}}'
            single_b_pattern_lines.append(line)
            single_s_pattern_lines.append(line.replace("banner_pattern","shield_pattern"))
         ctx.data.functions[f"tryashtar.shulker_preview:row_{row}/overlay/banner/{cname}"] = beet.Function(single_b_pattern_lines)
         ctx.data.functions[f"tryashtar.shulker_preview:row_{row}/overlay/shield/{cname}"] = beet.Function(single_s_pattern_lines)
      shield_base.append(f'execute positioned ~ ~0.02 ~ run function tryashtar.shulker_preview:row_{row}/overlay/shield')
      ctx.data.functions[f"tryashtar.shulker_preview:row_{row}/overlay/shield_base"] = beet.Function(shield_base)

      # dyed armor
      default_armor_lines=[
         f'# create an entity that draws approximately colored armor',
         f'execute store result score #color shulker_preview run data get storage tryashtar.shulker_preview:data item.tag.display.color',
         f'function tryashtar.shulker_preview:row_{row}/analyze_color',
      ]
      armor_lines={
         "leather_helmet": default_armor_lines.copy(),
         "leather_chestplate": default_armor_lines.copy(),
         "leather_leggings": default_armor_lines.copy(),
         "leather_boots": default_armor_lines.copy(),
         "leather_horse_armor": default_armor_lines.copy()
      }

      # map markings
      map_lines=[
         f'# create an entity that draws the proper map overlay color',
         f'execute store result score #color shulker_preview run data get storage tryashtar.shulker_preview:data item.tag.display.MapColor'
      ]
      map_unless='execute '
      for color in [3830373, 5393476]:
         map_lines.append(f'execute if score #color shulker_preview matches {color} run summon marker ~ ~0.5 ~ {{Tags:["tryashtar.shulker_preview"],CustomName:\'{{"translate":"tryashtar.shulker_preview.overlay.filled_map_markings.{row}","color":"{color_hex(color)}"}}\'}}')
         map_unless+=f'unless score #color shulker_preview matches {color} '
      map_unless+=f'run function tryashtar.shulker_preview:row_{row}/overlay/custom_map'
      map_lines.append(map_unless)

      custom_map_lines=[
         f'# create an entity that draws approximately the correct overlay color',
         f'function tryashtar.shulker_preview:row_{row}/analyze_color',
      ]

      # color analysis
      lines=[
         "# pick the closest of the 16 dye colors",
         "scoreboard players operation #red shulker_preview = #color shulker_preview",
         "scoreboard players operation #red shulker_preview /= #256 shulker_preview",
         "scoreboard players operation #red shulker_preview /= #256 shulker_preview",
         "scoreboard players operation #red shulker_preview %= #256 shulker_preview",
         "scoreboard players operation #green shulker_preview = #color shulker_preview",
         "scoreboard players operation #green shulker_preview /= #256 shulker_preview",
         "scoreboard players operation #green shulker_preview %= #256 shulker_preview",
         "scoreboard players operation #blue shulker_preview = #color shulker_preview",
         "scoreboard players operation #blue shulker_preview %= #256 shulker_preview",
         "scoreboard players set #nearest shulker_preview 2147483647",
         ""
      ]
      color_assigns=[]
      for i,(color,chex) in enumerate(dye_colors.items()):
         rgb=tuple(int(chex[i:i+2], 16) for i in (0, 2, 4))
         r,g,b=rgb
         rgbint=(r<<16) + (g<<8) + b
         color_assigns.append(f"execute if score #diff{i} shulker_preview = #nearest shulker_preview run scoreboard players set #near_color shulker_preview {rgbint}")
         lines.append(f"# {color}")
         lines.append(f"scoreboard players operation #mean shulker_preview = #red shulker_preview")
         lines.append(f"scoreboard players add #mean shulker_preview {r}")
         lines.append(f"scoreboard players operation #mean shulker_preview /= #2 shulker_preview")
         lines.append(f"scoreboard players set #mean2 shulker_preview 767")
         lines.append(f"scoreboard players operation #mean2 shulker_preview -= #mean shulker_preview")
         lines.append(f"scoreboard players operation #red_diff shulker_preview = #red shulker_preview")
         lines.append(f"scoreboard players remove #red_diff shulker_preview {r}")
         lines.append(f"scoreboard players operation #red_diff shulker_preview *= #red_diff shulker_preview")
         lines.append(f"scoreboard players operation #green_diff shulker_preview = #green shulker_preview")
         lines.append(f"scoreboard players remove #green_diff shulker_preview {g}")
         lines.append(f"scoreboard players operation #green_diff shulker_preview *= #green_diff shulker_preview")
         lines.append(f"scoreboard players operation #blue_diff shulker_preview = #blue shulker_preview")
         lines.append(f"scoreboard players remove #blue_diff shulker_preview {b}")
         lines.append(f"scoreboard players operation #blue_diff shulker_preview *= #blue_diff shulker_preview")
         lines.append(f"scoreboard players add #mean shulker_preview 512")
         lines.append(f"scoreboard players operation #red_diff shulker_preview *= #mean shulker_preview")
         lines.append(f"scoreboard players operation #red_diff shulker_preview /= #256 shulker_preview")
         lines.append(f"scoreboard players operation #green_diff shulker_preview *= #4 shulker_preview")
         lines.append(f"scoreboard players operation #blue_diff shulker_preview *= #mean2 shulker_preview")
         lines.append(f"scoreboard players operation #blue_diff shulker_preview /= #256 shulker_preview")
         lines.append(f"scoreboard players operation #diff{i} shulker_preview = #red_diff shulker_preview")
         lines.append(f"scoreboard players operation #diff{i} shulker_preview += #green_diff shulker_preview")
         lines.append(f"scoreboard players operation #diff{i} shulker_preview += #blue_diff shulker_preview")
         lines.append(f"scoreboard players operation #nearest shulker_preview < #diff{i} shulker_preview")
         lines.append("")
         custom_potion_lines.append(f'execute if score #near_color shulker_preview matches {rgbint} run summon marker ~ ~0.2 ~ {{Tags:["tryashtar.shulker_preview"],CustomName:\'{{"translate":"tryashtar.shulker_preview.overlay.potion_overlay.{row}","color":"#{chex}"}}\'}}')
         custom_arrow_lines.append(f'execute if score #near_color shulker_preview matches {rgbint} run summon marker ~ ~0.4 ~ {{Tags:["tryashtar.shulker_preview"],CustomName:\'{{"translate":"tryashtar.shulker_preview.overlay.tipped_arrow_head.{row}","color":"#{chex}"}}\'}}')
         custom_map_lines.append(f'execute if score #near_color shulker_preview matches {rgbint} run summon marker ~ ~0.6 ~ {{Tags:["tryashtar.shulker_preview"],CustomName:\'{{"translate":"tryashtar.shulker_preview.overlay.filled_map_markings.{row}","color":"#{chex}"}}\'}}')
         for armor,armorlines in armor_lines.items():
            armorlines.append(f'execute if score #near_color shulker_preview matches {rgbint} run summon marker ~ ~ ~ {{Tags:["tryashtar.shulker_preview"],CustomName:\'{{"translate":"tryashtar.shulker_preview.item.{armor}.{row}","color":"#{chex}"}}\'}}')

      lines.extend(color_assigns)
      ctx.data.functions[f"tryashtar.shulker_preview:row_{row}/analyze_color"] = beet.Function(lines)

      ctx.data.functions[f"tryashtar.shulker_preview:row_{row}/overlay/potion"] = beet.Function(potion_lines)
      ctx.data.functions[f"tryashtar.shulker_preview:row_{row}/overlay/custom_potion"] = beet.Function(custom_potion_lines)
      ctx.data.functions[f"tryashtar.shulker_preview:row_{row}/overlay/arrow"] = beet.Function(arrow_lines)
      ctx.data.functions[f"tryashtar.shulker_preview:row_{row}/overlay/custom_arrow"] = beet.Function(custom_arrow_lines)
      ctx.data.functions[f"tryashtar.shulker_preview:row_{row}/overlay/map"] = beet.Function(map_lines)
      ctx.data.functions[f"tryashtar.shulker_preview:row_{row}/overlay/custom_map"] = beet.Function(custom_map_lines)
      ctx.data.functions[f"tryashtar.shulker_preview:row_{row}/overlay/banner"] = beet.Function(banner_lines)
      ctx.data.functions[f"tryashtar.shulker_preview:row_{row}/overlay/shield"] = beet.Function(shield_lines)
      ctx.data.functions[f"tryashtar.shulker_preview:row_{row}/overlay/banner_pattern"] = beet.Function(banner_pattern_lines)
      ctx.data.functions[f"tryashtar.shulker_preview:row_{row}/overlay/shield_pattern"] = beet.Function(shield_pattern_lines)
      for armor,lines in armor_lines.items():
         dye_armor=armor.replace("leather_","").replace("_armor","")
         ctx.data.functions[f"tryashtar.shulker_preview:row_{row}/dye_armor/{dye_armor}"] = beet.Function(lines)


   # generate all items for testing
   index = 0
   chest_items=list(all_items.keys())
   while index < len(chest_items):
      boxes = 0
      boxslot = 0
      command = "setblock ~ ~1 ~ chest{Items:["
      while index < len(chest_items) and len(command) < 32000:
         item = chest_items[index]
         if boxslot == 0:
            command += f'{{id:shulker_box,Count:1b,Slot:{boxes}b,tag:{{BlockEntityTag:{{Items:['
            boxes += 1
         command += f'{{id:"minecraft:{item}",Count:1b,Slot:{boxslot}b}},'
         index += 1
         boxslot +=1
         if boxslot >= 27:
            boxslot = 0
         if boxslot == 0:
            command += "]}}},"
            if boxes >= 27:
               break
      if boxslot != 0:
         command += "]}}},"
      command += "]}"
      print(command)

   icon = beet.PngFile(Image.open('in/pack.png'))
   ctx.assets.icon = icon
   ctx.data.icon = icon
   ctx.assets.pack_format = 7
   ctx.assets.description = {'text':'Shulker Box tooltip preview: resource pack','color':'#8fdff7'}
   ctx.assets.save(path='out/resourcepack', overwrite=True)
   ctx.assets.save(path=f'out/Shulker Preview Resource Pack ({minecraft_version}).zip', zipped=True, overwrite=True)
   ctx.data.pack_format = 7
   ctx.data.description = {'text':'Shulker Box tooltip preview: data pack','color':'#8fdff7'}
   ctx.data.save(path='out/datapack', overwrite=True)
   ctx.data.save(path=f'out/Shulker Preview Data Pack ({minecraft_version}).zip', zipped=True, overwrite=True)
   dark_theme = beet.ResourcePack(path='in/resourcepack_dark')
   dark_theme.pack_format = ctx.assets.pack_format
   dark_theme.description = '(apply this pack above the normal resource pack)'
   dark_theme.save(path='out/dark_theme', overwrite=True)
   dark_theme.save(path=f'out/Shulker Preview Dark Theme ({minecraft_version}).zip', zipped=True, overwrite=True)

def get_items(ctx: beet.Context, vanilla: beet.contrib.vanilla.Vanilla, version: str):
   release = vanilla.releases[version]
   jar = release.cache.download(
      release.info.data["downloads"]["server"]["url"]
   )
   cache = ctx.cache["shulker_preview"]
   path = cache.get_path("minecraft_reports")
   if not path.is_dir():
      os.makedirs(path, exist_ok=True)
      subprocess.run(["java","-cp",jar,"net.minecraft.data.Main","--reports",],
         cwd=path,
         check=True,
      )
   with open(path / "generated" / "reports" / "registries.json") as file:
      items = json.load(file)["minecraft:item"]["entries"]
   return items

def colorize(image, color):
   return ImageChops.multiply(image, Image.new('RGBA', image.size, color))

def rgba(color):
   r = color // 256 // 256 % 256
   g = color // 256 % 256
   b = color % 256
   return (r, g, b, 255)


def unicode_escape(character):
   return "\\u"+str(character.encode("unicode-escape"))[5:9].upper()

def grid_keys(tuple_grid):
   return apply_to_all(tuple_grid, lambda x: x[0])

def apply_to_all(tuple_grid, lamb):
   return [[(None if j is None else lamb(j)) for j in i] for i in tuple_grid]

def block_translation(key, row):
   if not "." in key:
      key="block."+key
   return f"{key}.{row}"

def block_spacing(key):
   if "_pattern." in key:
      return (get_spacing(-18),get_spacing(1))
   return (get_spacing(0),get_spacing(1))

# fewest positive/negative spaces required to move this many pixels
positive_spaces=OrderedDict([(1024,'\uF82F'),(512,'\uF82E'),(256,'\uF82D'),(128,'\uF82C'),(64,'\uF82B'),(32,'\uF82A'),(16,'\uF829'),(8,'\uF828'),(7,'\uF827'),(6,'\uF826'),(5,'\uF825'),(4,'\uF824'),(3,'\uF823'),(2,'\uF822'),(1,'\uF821')])
negative_spaces=OrderedDict([(-1024,'\uF80F'),(-512,'\uF80E'),(-256,'\uF80D'),(-128,'\uF80C'),(-64,'\uF80B'),(-32,'\uF80A'),(-16,'\uF809'),(-8,'\uF808'),(-7,'\uF807'),(-6,'\uF806'),(-5,'\uF805'),(-4,'\uF804'),(-3,'\uF803'),(-2,'\uF802'),(-1,'\uF801')])
# numbers are in pixels, alternativey "max" or "-max" in sequence applies respective size space
def get_spacing(pixels):
   result=""
   if pixels=="max":
      result+='\uF820'
   elif pixels=="-max":
      result+='\uF800'
   elif pixels>=0:
      for space in positive_spaces:
         while pixels>=space:
            pixels-=space
            result+=positive_spaces[space]
   else:
      for space in negative_spaces:
         while pixels<=space:
            pixels-=space
            result+=negative_spaces[space]
   return result

currentchar='\u0900'
charmap={}
translations={"%1$s%418634357$s":"%2$s","tryashtar.shulker_preview.empty_slot":get_spacing(18),"tryashtar.shulker_preview.row_end":get_spacing(-162)}
# create a provider from file name, grid of icon names, and ascent/height
# returns provider and also modifies charmap, a global [icon->character code] dictionary, and translations, which is charmap but with prefixed keys, and values padded with positive/negative spaces as specified in spacing
def register_grid(fileid, icongrid, ascent, height, spacing_lambda):
   global currentchar
   base={"type":"bitmap","file":fileid,"ascent":ascent,"height":height}
   chars=[]
   for row in icongrid:
      string=""
      for entry in row:
         if entry is None:
            string+='\u0000'
            continue
         charmap[entry]=currentchar
         spacing=spacing_lambda(entry)
         if spacing is not None:
            translations[f"tryashtar.shulker_preview.{entry}"]=spacing[0]+currentchar+spacing[1]
         string+=currentchar
         currentchar=next_legal_character(currentchar)
      chars.append(string)
   base["chars"]=chars
   return base

def next_legal_character(currentchar):
   i=ord(currentchar)
   i+=1
   if i>=0x600 and i<=0x6ff:
      i=0x700
   return chr(i)

def register_items(items, row, ascent, height, real_version):
   global currentchar
   results=[]
   itemlist=list(items.items())
   itemlist.append(("missingno","item"))
   for item,v in itemlist:
      if "_spawn_egg" in item or item in reused_textures:
         continue
      location=item.replace("glass_pane","glass")
      location={"large_fern":"large_fern_top","lilac":"lilac_top","peony":"peony_top","rose_bush":"rose_bush_top","sunflower":"sunflower_front","clock":"clock_00","compass":"compass_16","crossbow":"crossbow_standby","tall_grass":"tall_grass_top","tipped_arrow":"tipped_arrow_base","twisting_vines":"twisting_vines_plant","weeping_vines":"weeping_vines_plant"}.get(location,location)
      itype="block" if v=="block" else "item"
      thingtype="item"
      if item in ["tipped_arrow_head","spawn_egg_overlay","potion_overlay","leather_boots_overlay","leather_chestplate_overlay","leather_helmet_overlay","leather_leggings_overlay","firework_star_overlay","filled_map_markings"]:
         thingtype="overlay"
      resource_location=f"minecraft:{itype}/{location}.png"
      if item=="missingno":
         resource_location="tryashtar.shulker_preview:missingno.png"
      if real_version:
         negative=charmap[f"negative.{thingtype}.{item}"]
         firstspace=""
         if thingtype=="overlay":
            firstspace=get_spacing(-18)
         results.append(register_single(resource_location, f"{thingtype}.{item}.{row}", ascent, height, (firstspace,negative+get_spacing(15))))         
      else:
         results.append(register_single(resource_location, f"negative.{thingtype}.{item}", -32768, -height, None))
   return results

# shortcut to create provider from one image
def register_single(fileid, iconname, ascent, height, spacing):
   return register_grid(fileid, [[iconname]], ascent, height, lambda x: spacing)

# take [item name->path] dictionary and form it into an ordered square 2D array of tuples (missing spaces are filled in with None)
def create_grid(icondict):
   size=get_dimensions(len(icondict))
   ordered=list(icondict.items())
   ordered.extend([None]*(size[0]*size[1]-len(ordered)))
   result=numpy.empty(len(ordered), dtype=object)
   result[:]=ordered
   return numpy.reshape(result, size)

# returns an integer square that fits this area
# might remove bottom row if it would be empty
def get_dimensions(area):
   width=math.ceil(math.sqrt(area))
   height=width
   if width*(height-1)>=area:
      height-=1
   return (height,width)

# take square 2D array of (item name, path) tuples and add images to a large image grid
def create_image(grid, icon_size):
   dim=grid.shape
   sheet=Image.new("RGBA", (dim[1]*icon_size,dim[0]*icon_size))
   for pos, icon in numpy.ndenumerate(grid):
      if icon is None:
         continue
      x=pos[1]*icon_size
      y=pos[0]*icon_size
      sprite=icon[1]
      pixels = sprite.load()
      for corner in (0,icon_size-1):
         r,g,b,a = pixels[corner,corner]
         if a==0:
            r,g,b=(139,139,139)
         pixels[corner,corner] = (r,g,b,max(a,18))
      sheet.paste(sprite, (x, y, x+icon_size, y+icon_size))
   return sheet

def rename_key(dictionary, oldname, newname):
   dictionary[newname]=dictionary.pop(oldname)

def delete_entries_regex(dictionary, regex):
   for k in list(dictionary):
      if re.search(regex,k):
         del dictionary[k] 

def delete_entries(dictionary, keys):
   for k in keys:
      if k in dictionary:
         del dictionary[k]

# create [item name->path] dictionary from reading PNG files in one or more folders
def load_items(*args):
   result={}
   for folder in args:
      for file in os.listdir(folder):
         ext=os.path.splitext(file)[1]
         if ext==".png":
            name=os.path.splitext(file)[0]
            location=os.path.join(folder,file)
            result[name]=location
   return result

# item information
durability_dict={"leather_helmet":55,"leather_chestplate":80,"leather_leggings":75,"leather_boots":65,"golden_helmet":77,"golden_chestplate":112,"golden_leggings":105,"golden_boots":91,"chainmail_helmet":165,"chainmail_chestplate":240,"chainmail_leggings":225,"chainmail_boots":195,"iron_helmet":165,"iron_chestplate":240,"iron_leggings":225,"iron_boots":195,"diamond_helmet":363,"diamond_chestplate":528,"diamond_leggings":495,"diamond_boots":429,"golden_axe":32,"golden_pickaxe":32,"golden_shovel":32,"golden_hoe":32,"golden_sword":32,"wooden_axe":59,"wooden_pickaxe":59,"wooden_shovel":59,"wooden_hoe":59,"wooden_sword":59,"stone_axe":131,"stone_pickaxe":131,"stone_shovel":131,"stone_hoe":131,"stone_sword":131,"iron_axe":250,"iron_pickaxe":250,"iron_shovel":250,"iron_hoe":250,"iron_sword":250,"diamond_axe":1561,"diamond_pickaxe":1561,"diamond_shovel":1561,"diamond_hoe":1561,"diamond_sword":1561,"fishing_rod":64,"flint_and_steel":64,"carrot_on_a_stick":25,"shears":238,"shield":336,"bow":384,"trident":250,"elytra":432,"crossbow":326,"warped_fungus_on_a_stick":100,"netherite_axe":2031,"netherite_sword":2031,"netherite_pickaxe":2031,"netherite_shovel":2031,"netherite_hoe":2031,"netherite_helmet":407,"netherite_chestplate":592,"netherite_leggings":555,"netherite_boots":481}
potion_dict={"night_vision":2039713,"long_night_vision":2039713,"invisibility":8356754,"long_invisibility":8356754,"leaping":2293580,"strong_leaping":2293580,"long_leaping":2293580,"fire_resistance":14981690,"long_fire_resistance":14981690,"swiftness":8171462,"strong_swiftness":8171462,"long_swiftness":8171462,"water_breathing":3035801,"long_water_breathing":3035801,"healing":16262179,"strong_healing":16262179,"harming":4393481,"strong_harming":4393481,"poison":5149489,"strong_poison":5149489,"long_poison":5149489,"regeneration":13458603,"strong_regeneration":13458603,"long_regeneration":13458603,"strength":9643043,"strong_strength":9643043,"long_strength":9643043,"weakness":4738376,"long_weakness":4738376,"luck":3381504,"turtle_master":0x755b62,"strong_turtle_master":0x735c64,"long_turtle_master":0x755b62,"slow_falling":16773073,"long_slow_falling":16773073,"slowness":5926017,"long_slowness":5926017,"strong_slowness":5926017,"water":3694022,"thick":3694022,"mundane":3694022,"awkward":3694022}
potion_dict=dict(sorted(potion_dict.items()))

int_colors={
   0:"white",
   1:"orange",
   2:"magenta",
   3:"light_blue",
   4:"yellow",
   5:"lime",
   6:"pink",
   7:"gray",
   8:"light_gray",
   9:"cyan",
   10:"purple",
   11:"blue",
   12:"brown",
   13:"green",
   14:"red",
   15:"black"
}

dye_colors={
   "white": "f9fffe",
   "orange": "f9801d",
   "magenta": "c74ebd",
   "light_blue": "3ab3da",
   "yellow": "fed83d",
   "lime": "80c71f",
   "pink": "f38baa",
   "gray": "474f52",
   "light_gray": "9d9d97",
   "cyan": "169c9c",
   "purple": "8932b8",
   "blue": "3c44aa",
   "brown": "835432",
   "green": "5e7c16",
   "red": "b02e26",
   "black": "1d1d21"
}

banner_pattern_ids={
   "bs":"stripe_bottom",
   "ts":"stripe_top",
   "ls":"stripe_left",
   "rs":"stripe_right",
   "cs":"stripe_center",
   "ms":"stripe_middle",
   "drs":"stripe_downright",
   "dls":"stripe_downleft",
   "ss":"small_stripes",
   "cr":"cross",
   "sc":"straight_cross",
   "ld":"diagonal_left",
   "rud":"diagonal_right",
   "lud":"diagonal_up_left",
   "rd":"diagonal_up_right",
   "vh":"half_vertical",
   "vhr":"half_vertical_right",
   "hh":"half_horizontal",
   "hhb":"half_horizontal_bottom",
   "bl":"square_bottom_left",
   "br":"square_bottom_right",
   "tl":"square_top_left",
   "tr":"square_top_right",
   "bt":"triangle_bottom",
   "tt":"triangle_top",
   "bts":"triangles_bottom",
   "tts":"triangles_top",
   "mc":"circle",
   "mr":"rhombus",
   "bo":"border",
   "cbo":"curly_border",
   "bri":"bricks",
   "gra":"gradient",
   "gru":"gradient_up",
   "cre":"creeper",
   "sku":"skull",
   "flo":"flower",
   "moj":"mojang",
   "glb":"globe",
   "pig":"piglin"
}

spawn_egg_colors={
   "axolotl_spawn_egg": (16499171, 10890612),
   "bat_spawn_egg": (4996656, 986895),
   "bee_spawn_egg": (15582019, 4400155),
   "blaze_spawn_egg": (16167425, 16775294),
   "cat_spawn_egg": (15714446, 9794134),
   "cave_spider_spawn_egg": (803406, 11013646),
   "chicken_spawn_egg": (10592673, 16711680),
   "cod_spawn_egg": (12691306, 15058059),
   "cow_spawn_egg": (4470310, 10592673),
   "creeper_spawn_egg": (894731, 0),
   "dolphin_spawn_egg": (2243405, 16382457),
   "donkey_spawn_egg": (5457209, 8811878),
   "drowned_spawn_egg": (9433559, 7969893),
   "elder_guardian_spawn_egg": (13552826, 7632531),
   "enderman_spawn_egg": (1447446, 0),
   "endermite_spawn_egg": (1447446, 7237230),
   "evoker_spawn_egg": (9804699, 1973274),
   "fox_spawn_egg": (14005919, 13396256),
   "ghast_spawn_egg": (16382457, 12369084),
   "glow_squid_spawn_egg": (611926, 8778172),
   "goat_spawn_egg": (10851452, 5589310),
   "guardian_spawn_egg": (5931634, 15826224),
   "hoglin_spawn_egg": (13004373, 6251620),
   "horse_spawn_egg": (12623485, 15656192),
   "husk_spawn_egg": (7958625, 15125652),
   "llama_spawn_egg": (12623485, 10051392),
   "magma_cube_spawn_egg": (3407872, 16579584),
   "mooshroom_spawn_egg": (10489616, 12040119),
   "mule_spawn_egg": (1769984, 5321501),
   "ocelot_spawn_egg": (15720061, 5653556),
   "panda_spawn_egg": (15198183, 1776418),
   "parrot_spawn_egg": (894731, 16711680),
   "phantom_spawn_egg": (4411786, 8978176),
   "pig_spawn_egg": (15771042, 14377823),
   "piglin_spawn_egg": (10051392, 16380836),
   "piglin_brute_spawn_egg": (5843472, 16380836),
   "pillager_spawn_egg": (5451574, 9804699),
   "polar_bear_spawn_egg": (15921906, 9803152),
   "pufferfish_spawn_egg": (16167425, 3654642),
   "rabbit_spawn_egg": (10051392, 7555121),
   "ravager_spawn_egg": (7697520, 5984329),
   "salmon_spawn_egg": (10489616, 951412),
   "sheep_spawn_egg": (15198183, 16758197),
   "shulker_spawn_egg": (9725844, 5060690),
   "silverfish_spawn_egg": (7237230, 3158064),
   "skeleton_spawn_egg": (12698049, 4802889),
   "skeleton_horse_spawn_egg": (6842447, 15066584),
   "slime_spawn_egg": (5349438, 8306542),
   "spider_spawn_egg": (3419431, 11013646),
   "squid_spawn_egg": (2243405, 7375001),
   "stray_spawn_egg": (6387319, 14543594),
   "strider_spawn_egg": (10236982, 5065037),
   "trader_llama_spawn_egg": (15377456, 4547222),
   "tropical_fish_spawn_egg": (15690005, 16775663),
   "turtle_spawn_egg": (15198183, 44975),
   "vex_spawn_egg": (8032420, 15265265),
   "villager_spawn_egg": (5651507, 12422002),
   "vindicator_spawn_egg": (9804699, 2580065),
   "wandering_trader_spawn_egg": (4547222, 15377456),
   "witch_spawn_egg": (3407872, 5349438),
   "wither_skeleton_spawn_egg": (1315860, 4672845),
   "wolf_spawn_egg": (14144467, 13545366),
   "zoglin_spawn_egg": (13004373, 15132390),
   "zombie_spawn_egg": (44975, 7969893),
   "zombie_horse_spawn_egg": (3232308, 9945732),
   "zombified_piglin_spawn_egg": (15373203, 5009705),
   "zombie_villager_spawn_egg": (5651507, 7969893),
}
reused_textures={"debug_stick":"stick","enchanted_golden_apple":"golden_apple"}
grass_colors={"vine":"#48b518","lily_pad":"#71c35c","grass":"#7bbd6b","fern":"#7bbd6b","tall_grass":"#7bbd6b","large_fern":"#7bbd6b"}

def color_hex(int_color):
   return "#"+format(int_color,'06x')

# generates a very specific function
def process_item_lines(items, row):
   lines=[]
   potion=False
   durability=False
   arrow=False
   filledmap=False
   banner=False
   shield=False
   for item, itemtype in sorted(items, key=lambda x: x[0]):
      name="minecraft:"+item
      if_item=f'execute if data storage tryashtar.shulker_preview:data item{{id:"{name}"}}'
      reused=reused_textures.get(item)
      grass=grass_colors.get(item)
      if reused is not None:
         lines.append(f'{if_item} run summon marker ~ ~ ~ {{Tags:["tryashtar.shulker_preview"],CustomName:\'{{"translate":"tryashtar.shulker_preview.{itemtype}.{reused}.{row}"}}\'}}')
      elif grass is not None:
         lines.append(f'{if_item} run summon marker ~ ~ ~ {{Tags:["tryashtar.shulker_preview"],CustomName:\'{{"translate":"tryashtar.shulker_preview.{itemtype}.{item}.{row}","color":"{grass}"}}\'}}')
      elif "spawn_egg" in item:
         color=spawn_egg_colors[item]
         lines.append(f'{if_item} run summon marker ~ ~ ~ {{Tags:["tryashtar.shulker_preview"],CustomName:\'[{{"translate":"tryashtar.shulker_preview.item.spawn_egg.{row}","color":"{color_hex(color[0])}"}},{{"translate":"tryashtar.shulker_preview.overlay.spawn_egg_overlay.{row}","color":"{color_hex(color[1])}"}}]\'}}')
      elif item == "elytra":
         lines.extend([
            f'execute if data storage tryashtar.shulker_preview:data item{{id:"minecraft:elytra",tag:{{Damage:431}}}} run summon marker ~ ~ ~ {{Tags:["tryashtar.shulker_preview"],CustomName:\'{{"translate":"tryashtar.shulker_preview.item.broken_elytra.{row}"}}\'}}',
            f'{if_item} unless data storage tryashtar.shulker_preview:data item{{tag:{{Damage:431}}}} run summon marker ~ ~ ~ {{Tags:["tryashtar.shulker_preview"],CustomName:\'{{"translate":"tryashtar.shulker_preview.item.elytra.{row}"}}\'}}'
            ])
      elif item == "bundle":
         lines.extend([
            f'execute if data storage tryashtar.shulker_preview:data item{{id:"minecraft:bundle",tag:{{Items:[{{}}]}}}} run summon marker ~ ~ ~ {{Tags:["tryashtar.shulker_preview"],CustomName:\'{{"translate":"tryashtar.shulker_preview.item.bundle_filled.{row}"}}\'}}',
            f'{if_item} unless data storage tryashtar.shulker_preview:data item.tag.Items[{{}}] run summon marker ~ ~ ~ {{Tags:["tryashtar.shulker_preview"],CustomName:\'{{"translate":"tryashtar.shulker_preview.item.bundle.{row}"}}\'}}'
            ])
      elif item == "crossbow":
         lines.extend([
            f'execute if data storage tryashtar.shulker_preview:data item{{id:"minecraft:crossbow",tag:{{ChargedProjectiles:[{{id:"minecraft:arrow"}}]}}}} run summon marker ~ ~ ~ {{Tags:["tryashtar.shulker_preview"],CustomName:\'{{"translate":"tryashtar.shulker_preview.item.crossbow_arrow.{row}"}}\'}}',
            f'execute if data storage tryashtar.shulker_preview:data item{{id:"minecraft:crossbow",tag:{{ChargedProjectiles:[{{id:"minecraft:firework_rocket"}}]}}}} run summon marker ~ ~ ~ {{Tags:["tryashtar.shulker_preview"],CustomName:\'{{"translate":"tryashtar.shulker_preview.item.crossbow_firework.{row}"}}\'}}',
            f'{if_item} unless data storage tryashtar.shulker_preview:data item.tag.ChargedProjectiles[{{}}] run summon marker ~ ~ ~ {{Tags:["tryashtar.shulker_preview"],CustomName:\'{{"translate":"tryashtar.shulker_preview.item.crossbow.{row}"}}\'}}'
            ])
      elif item == "light":
         for light_level in range(0,16):
            lines.append(f'execute if data storage tryashtar.shulker_preview:data item{{id:"minecraft:light",tag:{{BlockStateTag:{{level:"{light_level}"}}}}}} run summon marker ~ ~ ~ {{Tags:["tryashtar.shulker_preview"],CustomName:\'{{"translate":"tryashtar.shulker_preview.item.light_{str(light_level).zfill(2)}.{row}"}}\'}}')
         lines.append(f'{if_item} unless data storage tryashtar.shulker_preview:data item.tag.BlockStateTag.level run summon marker ~ ~ ~ {{Tags:["tryashtar.shulker_preview"],CustomName:\'{{"translate":"tryashtar.shulker_preview.item.light_15.{row}"}}\'}}')
      elif item in ["leather_helmet","leather_chestplate","leather_leggings","leather_boots","leather_horse_armor"]:
         dye_armor=item.replace("leather_","").replace("_armor","")
         lines.append(f'{if_item} unless data storage tryashtar.shulker_preview:data item.tag.display.color run summon marker ~ ~ ~ {{Tags:["tryashtar.shulker_preview"],CustomName:\'{{"translate":"tryashtar.shulker_preview.item.{item}.{row}","color":"{color_hex(10511680)}"}}\'}}')
         lines.append(f'{if_item} if data storage tryashtar.shulker_preview:data item.tag.display.color run function tryashtar.shulker_preview:row_{row}/dye_armor/{dye_armor}')
         if item not in ("leather_chestplate","leather_horse_armor"):
            lines.append(f'{if_item} run summon marker ~ ~0.02 ~ {{Tags:["tryashtar.shulker_preview"],CustomName:\'{{"translate":"tryashtar.shulker_preview.overlay.{item}_overlay.{row}"}}\'}}')
      elif item in ("potion","splash_potion","lingering_potion"):
         lines.append(f'{if_item} run summon marker ~ ~ ~ {{Tags:["tryashtar.shulker_preview"],CustomName:\'[{{"translate":"tryashtar.shulker_preview.item.{item}.{row}"}},{{"translate":"tryashtar.shulker_preview.overlay.potion_overlay.{row}","color":"{color_hex(16253176)}"}}]\'}}')
         potion=True
      elif item=="firework_star":
         lines.append(f'{if_item} run summon marker ~ ~ ~ {{Tags:["tryashtar.shulker_preview"],CustomName:\'[{{"translate":"tryashtar.shulker_preview.item.{item}.{row}"}},{{"translate":"tryashtar.shulker_preview.overlay.firework_star_overlay.{row}","color":"{color_hex(9079434)}"}}]\'}}')
      elif item=="filled_map":
         lines.append(f'{if_item} run summon marker ~ ~ ~ {{Tags:["tryashtar.shulker_preview"],CustomName:\'{{"translate":"tryashtar.shulker_preview.item.{item}.{row}"}}\'}}')
         lines.append(f'{if_item} unless data storage tryashtar.shulker_preview:data item.tag.display.MapColor run summon marker ~ ~0.01 ~ {{Tags:["tryashtar.shulker_preview"],CustomName:\'{{"translate":"tryashtar.shulker_preview.overlay.filled_map_markings.{row}","color":"#46402d"}}\'}}')
         filledmap=True
      elif item=="tipped_arrow":
         lines.append(f'{if_item} run summon marker ~ ~ ~ {{Tags:["tryashtar.shulker_preview"],CustomName:\'[{{"translate":"tryashtar.shulker_preview.item.{item}.{row}"}},{{"translate":"tryashtar.shulker_preview.overlay.tipped_arrow_head.{row}","color":"{color_hex(16253176)}"}}]\'}}')
         arrow=True
      else:
         lines.append(f'{if_item} run summon marker ~ ~ ~ {{Tags:["tryashtar.shulker_preview"],CustomName:\'{{"translate":"tryashtar.shulker_preview.{itemtype}.{item}.{row}"}}\'}}')
      if "banner" in item and "pattern" not in item:
         banner=True
      if item=="shield":
         shield=True
      if item in durability_dict:
         lines.append(f'{if_item} run scoreboard players set #max shulker_preview {durability_dict[item]}')
         durability=True
   if potion:
      lines.append(f'execute if data storage tryashtar.shulker_preview:data item.tag.Potion run function tryashtar.shulker_preview:row_{row}/overlay/potion')
      lines.append(f'execute if data storage tryashtar.shulker_preview:data item.tag.CustomPotionColor run function tryashtar.shulker_preview:row_{row}/overlay/custom_potion')
   if arrow:
      lines.append(f'execute if data storage tryashtar.shulker_preview:data item.tag.Potion run function tryashtar.shulker_preview:row_{row}/overlay/arrow')
      lines.append(f'execute if data storage tryashtar.shulker_preview:data item.tag.CustomPotionColor run function tryashtar.shulker_preview:row_{row}/overlay/custom_arrow')
   if filledmap:
      lines.append(f'execute if data storage tryashtar.shulker_preview:data item.tag.display.MapColor run function tryashtar.shulker_preview:row_{row}/overlay/map')
   if banner:
      lines.append(f'execute if data storage tryashtar.shulker_preview:data item.tag.BlockEntityTag.Patterns[0] positioned ~ ~0.7 ~ run function tryashtar.shulker_preview:row_{row}/overlay/banner')
   if shield:
      lines.append(f'execute if data storage tryashtar.shulker_preview:data item.tag.BlockEntityTag.Base positioned ~ ~0.7 ~ run function tryashtar.shulker_preview:row_{row}/overlay/shield_base')
   if durability:
      lines.extend([
         f'execute store result score #durability shulker_preview run data get storage tryashtar.shulker_preview:data item.tag.Damage',
         f'execute if data storage tryashtar.shulker_preview:data item.tag.Damage run function tryashtar.shulker_preview:row_{row}/overlay/durability'
         ])
   return lines
