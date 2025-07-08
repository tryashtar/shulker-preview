import copy
import os
import re
import math
import model_resolver.item_model
import model_resolver.item_model.special
import numpy
from PIL import Image, ImageChops
from collections import OrderedDict
import beet.contrib.vanilla
import model_resolver

def main(ctx: beet.Context):
   # load item textures from two sources
   print("Loading icons...")
   
   vanilla = beet.contrib.vanilla.Vanilla(ctx)
   blocknames = ['acacia_button','acacia_fence','acacia_fence_gate','acacia_leaves','acacia_log','acacia_planks','acacia_pressure_plate','acacia_slab','acacia_stairs','acacia_trapdoor','acacia_wood','andesite','andesite_slab','andesite_stairs','andesite_wall','anvil','barrel','beacon','bedrock','birch_button','birch_fence','birch_fence_gate','birch_leaves','birch_log','birch_planks','birch_pressure_plate','birch_slab','birch_stairs','birch_trapdoor','birch_wood','black_banner','black_bed','black_carpet','black_concrete','black_concrete_powder','black_glazed_terracotta','black_shulker_box','black_stained_glass','black_terracotta','black_wool','blast_furnace','blue_banner','blue_bed','blue_carpet','blue_concrete','blue_concrete_powder','blue_glazed_terracotta','blue_ice','blue_shulker_box','blue_stained_glass','blue_terracotta','blue_wool','bone_block','bookshelf','brain_coral_block','brick_slab','brick_stairs','brick_wall','bricks','brown_banner','brown_bed','brown_carpet','brown_concrete','brown_concrete_powder','brown_glazed_terracotta','brown_mushroom_block','brown_shulker_box','brown_stained_glass','brown_terracotta','brown_wool','bubble_coral_block','cactus','cartography_table','carved_pumpkin','chain_command_block','chest','chipped_anvil','chiseled_quartz_block','chiseled_red_sandstone','chiseled_sandstone','chiseled_stone_bricks','chorus_flower','chorus_plant','clay','coal_block','coal_ore','coarse_dirt','cobblestone','cobblestone_slab','cobblestone_stairs','cobblestone_wall','command_block','composter','conduit','cracked_stone_bricks','crafting_table','creeper_head','cut_red_sandstone','cut_red_sandstone_slab','cut_sandstone','cut_sandstone_slab','cyan_banner','cyan_bed','cyan_carpet','cyan_concrete','cyan_concrete_powder','cyan_glazed_terracotta','cyan_shulker_box','cyan_stained_glass','cyan_terracotta','cyan_wool','damaged_anvil','dark_oak_button','dark_oak_fence','dark_oak_fence_gate','dark_oak_leaves','dark_oak_log','dark_oak_planks','dark_oak_pressure_plate','dark_oak_slab','dark_oak_stairs','dark_oak_trapdoor','dark_oak_wood','dark_prismarine','dark_prismarine_slab','dark_prismarine_stairs','daylight_detector','dead_brain_coral_block','dead_bubble_coral_block','dead_fire_coral_block','dead_horn_coral_block','dead_tube_coral_block','diamond_block','diamond_ore','diorite','diorite_slab','diorite_stairs','diorite_wall','dirt','dispenser','dragon_egg','dragon_head','dried_kelp_block','dropper','emerald_block','emerald_ore','enchanting_table','end_portal_frame','end_rod','end_stone','end_stone_brick_slab','end_stone_brick_stairs','end_stone_brick_wall','end_stone_bricks','ender_chest','farmland','fire_coral_block','fletching_table','furnace','glass','glowstone','gold_block','gold_ore','granite','granite_slab','granite_stairs','granite_wall','grass_block','grass_path','gravel','gray_banner','gray_bed','gray_carpet','gray_concrete','gray_concrete_powder','gray_glazed_terracotta','gray_shulker_box','gray_stained_glass','gray_terracotta','gray_wool','green_banner','green_bed','green_carpet','green_concrete','green_concrete_powder','green_glazed_terracotta','green_shulker_box','green_stained_glass','green_terracotta','green_wool','grindstone','hay_block','heavy_weighted_pressure_plate','horn_coral_block','ice','infested_chiseled_stone_bricks','infested_cobblestone','infested_cracked_stone_bricks','infested_mossy_stone_bricks','infested_stone','infested_stone_bricks','iron_block','iron_ore','iron_trapdoor','jack_o_lantern','jigsaw','jukebox','jungle_button','jungle_fence','jungle_fence_gate','jungle_leaves','jungle_log','jungle_planks','jungle_pressure_plate','jungle_slab','jungle_stairs','jungle_trapdoor','jungle_wood','lapis_block','lapis_ore','lectern','light_blue_banner','light_blue_bed','light_blue_carpet','light_blue_concrete','light_blue_concrete_powder','light_blue_glazed_terracotta','light_blue_shulker_box','light_blue_stained_glass','light_blue_terracotta','light_blue_wool','light_gray_banner','light_gray_bed','light_gray_carpet','light_gray_concrete','light_gray_concrete_powder','light_gray_glazed_terracotta','light_gray_shulker_box','light_gray_stained_glass','light_gray_terracotta','light_gray_wool','light_weighted_pressure_plate','lime_banner','lime_bed','lime_carpet','lime_concrete','lime_concrete_powder','lime_glazed_terracotta','lime_shulker_box','lime_stained_glass','lime_terracotta','lime_wool','loom','magenta_banner','magenta_bed','magenta_carpet','magenta_concrete','magenta_concrete_powder','magenta_glazed_terracotta','magenta_shulker_box','magenta_stained_glass','magenta_terracotta','magenta_wool','magma_block','melon','mossy_cobblestone','mossy_cobblestone_slab','mossy_cobblestone_stairs','mossy_cobblestone_wall','mossy_stone_brick_slab','mossy_stone_brick_stairs','mossy_stone_brick_wall','mossy_stone_bricks','mushroom_stem','mycelium','nether_brick_fence','nether_brick_slab','nether_brick_stairs','nether_brick_wall','nether_bricks','nether_quartz_ore','nether_wart_block','netherrack','note_block','oak_button','oak_fence','oak_fence_gate','oak_leaves','oak_log','oak_planks','oak_pressure_plate','oak_slab','oak_stairs','oak_trapdoor','oak_wood','observer','obsidian','orange_banner','orange_bed','orange_carpet','orange_concrete','orange_concrete_powder','orange_glazed_terracotta','orange_shulker_box','orange_stained_glass','orange_terracotta','orange_wool','packed_ice','petrified_oak_slab','pink_banner','pink_bed','pink_carpet','pink_concrete','pink_concrete_powder','pink_glazed_terracotta','pink_shulker_box','pink_stained_glass','pink_terracotta','pink_wool','piston','player_head','podzol','polished_andesite','polished_andesite_slab','polished_andesite_stairs','polished_diorite','polished_diorite_slab','polished_diorite_stairs','polished_granite','polished_granite_slab','polished_granite_stairs','prismarine','prismarine_brick_slab','prismarine_brick_stairs','prismarine_bricks','prismarine_slab','prismarine_stairs','prismarine_wall','pumpkin','purple_banner','purple_bed','purple_carpet','purple_concrete','purple_concrete_powder','purple_glazed_terracotta','purple_shulker_box','purple_stained_glass','purple_terracotta','purple_wool','purpur_block','purpur_pillar','purpur_slab','purpur_stairs','quartz_block','quartz_pillar','quartz_slab','quartz_stairs','red_banner','red_bed','red_carpet','red_concrete','red_concrete_powder','red_glazed_terracotta','red_mushroom_block','red_nether_brick_slab','red_nether_brick_stairs','red_nether_brick_wall','red_nether_bricks','red_sand','red_sandstone','red_sandstone_slab','red_sandstone_stairs','red_sandstone_wall','red_shulker_box','red_stained_glass','red_terracotta','red_wool','redstone_block','redstone_lamp','redstone_ore','repeating_command_block','sand','sandstone','sandstone_slab','sandstone_stairs','sandstone_wall','scaffolding','sea_lantern','shield','shulker_box','skeleton_skull','slime_block','smithing_table','smoker','smooth_quartz','smooth_quartz_slab','smooth_quartz_stairs','smooth_red_sandstone','smooth_red_sandstone_slab','smooth_red_sandstone_stairs','smooth_sandstone','smooth_sandstone_slab','smooth_sandstone_stairs','smooth_stone','smooth_stone_slab','snow','snow_block','soul_sand','spawner','sponge','spruce_button','spruce_fence','spruce_fence_gate','spruce_leaves','spruce_log','spruce_planks','spruce_pressure_plate','spruce_slab','spruce_stairs','spruce_trapdoor','spruce_wood','sticky_piston','stone','stone_brick_slab','stone_brick_stairs','stone_brick_wall','stone_bricks','stone_button','stone_pressure_plate','stone_slab','stone_stairs','stonecutter','stripped_acacia_log','stripped_acacia_wood','stripped_birch_log','stripped_birch_wood','stripped_dark_oak_log','stripped_dark_oak_wood','stripped_jungle_log','stripped_jungle_wood','stripped_oak_log','stripped_oak_wood','stripped_spruce_log','stripped_spruce_wood','structure_block','terracotta','tnt','trapped_chest','tube_coral_block','wet_sponge','white_banner','white_bed','white_carpet','white_concrete','white_concrete_powder','white_glazed_terracotta','white_shulker_box','white_stained_glass','white_terracotta','white_wool','wither_skeleton_skull','yellow_banner','yellow_bed','yellow_carpet','yellow_concrete','yellow_concrete_powder','yellow_glazed_terracotta','yellow_shulker_box','yellow_stained_glass','yellow_terracotta','yellow_wool','zombie_head']
   
   itemnames = ['acacia_boat','acacia_door','acacia_sapling','acacia_sign','activator_rail','allium','apple','armor_stand','arrow','azure_bluet','baked_potato','bamboo','barrier','bat_spawn_egg','beef','beetroot','beetroot_seeds','beetroot_soup','bell','birch_boat','birch_door','birch_sapling','birch_sign','black_dye','black_stained_glass_pane','blaze_powder','blaze_rod','blaze_spawn_egg','blue_dye','blue_orchid','blue_stained_glass_pane','bone','bone_meal','book','bow','bowl','brain_coral','brain_coral_fan','bread','brewing_stand','brick','broken_elytra','brown_dye','brown_mushroom','brown_stained_glass_pane','bubble_coral','bubble_coral_fan','bucket','cake','campfire','carrot','carrot_on_a_stick','cat_spawn_egg','cauldron','cave_spider_spawn_egg','chainmail_boots','chainmail_chestplate','chainmail_helmet','chainmail_leggings','charcoal','chest_minecart','chicken','chicken_spawn_egg','chorus_fruit','clay_ball','clock','coal','cobweb','cocoa_beans','cod','cod_bucket','cod_spawn_egg','command_block_minecart','comparator','compass','cooked_beef','cooked_chicken','cooked_cod','cooked_mutton','cooked_porkchop','cooked_rabbit','cooked_salmon','cookie','cornflower','cow_spawn_egg','creeper_banner_pattern','creeper_spawn_egg','crossbow','crossbow_arrow','crossbow_firework','cyan_dye','cyan_stained_glass_pane','dandelion','dark_oak_boat','dark_oak_door','dark_oak_sapling','dark_oak_sign','dead_brain_coral','dead_brain_coral_fan','dead_bubble_coral','dead_bubble_coral_fan','dead_bush','dead_fire_coral','dead_fire_coral_fan','dead_horn_coral','dead_horn_coral_fan','dead_tube_coral','dead_tube_coral_fan','debug_stick','detector_rail','diamond','diamond_axe','diamond_boots','diamond_chestplate','diamond_helmet','diamond_hoe','diamond_horse_armor','diamond_leggings','diamond_pickaxe','diamond_shovel','diamond_sword','dolphin_spawn_egg','donkey_spawn_egg','dragon_breath','dried_kelp','drowned_spawn_egg','egg','elder_guardian_spawn_egg','elytra','emerald','enchanted_book','enchanted_golden_apple','end_crystal','ender_eye','ender_pearl','enderman_spawn_egg','endermite_spawn_egg','evoker_spawn_egg','experience_bottle','feather','fermented_spider_eye','fern','filled_map','fire_charge','fire_coral','fire_coral_fan','firework_rocket','firework_star','fishing_rod','flint','flint_and_steel','flower_banner_pattern','flower_pot','fox_spawn_egg','furnace_minecart','ghast_spawn_egg','ghast_tear','glass_bottle','glass_pane','glistering_melon_slice','globe_banner_pattern','glowstone_dust','gold_ingot','gold_nugget','golden_apple','golden_axe','golden_boots','golden_carrot','golden_chestplate','golden_helmet','golden_hoe','golden_horse_armor','golden_leggings','golden_pickaxe','golden_shovel','golden_sword','grass','gray_dye','gray_stained_glass_pane','green_dye','green_stained_glass_pane','guardian_spawn_egg','gunpowder','heart_of_the_sea','hopper','hopper_minecart','horn_coral','horn_coral_fan','horse_spawn_egg','husk_spawn_egg','ink_sac','iron_axe','iron_bars','iron_boots','iron_chestplate','iron_door','iron_helmet','iron_hoe','iron_horse_armor','iron_ingot','iron_leggings','iron_nugget','iron_pickaxe','iron_shovel','iron_sword','item_frame','jungle_boat','jungle_door','jungle_sapling','jungle_sign','kelp','knowledge_book','ladder','lantern','lapis_lazuli','large_fern','lava_bucket','lead','leather','leather_boots','leather_chestplate','leather_helmet','leather_horse_armor','leather_leggings','lever','light_blue_dye','light_blue_stained_glass_pane','light_gray_dye','light_gray_stained_glass_pane','lilac','lily_of_the_valley','lily_pad','lime_dye','lime_stained_glass_pane','lingering_potion','llama_spawn_egg','magenta_dye','magenta_stained_glass_pane','magma_cream','magma_cube_spawn_egg','map','melon_seeds','melon_slice','milk_bucket','minecart','mojang_banner_pattern','mooshroom_spawn_egg','mule_spawn_egg','mushroom_stew','music_disc_11','music_disc_13','music_disc_blocks','music_disc_cat','music_disc_chirp','music_disc_far','music_disc_mall','music_disc_mellohi','music_disc_stal','music_disc_strad','music_disc_wait','music_disc_ward','mutton','name_tag','nautilus_shell','nether_brick','nether_star','nether_wart','oak_boat','oak_door','oak_sapling','oak_sign','ocelot_spawn_egg','orange_dye','orange_stained_glass_pane','orange_tulip','oxeye_daisy','painting','panda_spawn_egg','paper','parrot_spawn_egg','peony','phantom_membrane','phantom_spawn_egg','pig_spawn_egg','pillager_spawn_egg','pink_dye','pink_stained_glass_pane','pink_tulip','poisonous_potato','polar_bear_spawn_egg','popped_chorus_fruit','poppy','porkchop','potato','potion','powered_rail','prismarine_crystals','prismarine_shard','pufferfish','pufferfish_bucket','pufferfish_spawn_egg','pumpkin_pie','pumpkin_seeds','purple_dye','purple_stained_glass_pane','quartz','rabbit','rabbit_foot','rabbit_hide','rabbit_spawn_egg','rabbit_stew','rail','ravager_spawn_egg','red_dye','red_mushroom','red_stained_glass_pane','red_tulip','redstone','redstone_torch','repeater','rose_bush','rotten_flesh','saddle','salmon','salmon_bucket','salmon_spawn_egg','scute','sea_pickle','seagrass','shears','sheep_spawn_egg','shulker_shell','shulker_spawn_egg','silverfish_spawn_egg','skeleton_horse_spawn_egg','skeleton_spawn_egg','skull_banner_pattern','slime_ball','slime_spawn_egg','snowball','spectral_arrow','spider_eye','spider_spawn_egg','splash_potion','spruce_boat','spruce_door','spruce_sapling','spruce_sign','squid_spawn_egg','stick','stone_axe','stone_hoe','stone_pickaxe','stone_shovel','stone_sword','stray_spawn_egg','string','structure_void','sugar','sugar_cane','sunflower','suspicious_stew','sweet_berries','tall_grass','tipped_arrow','tnt_minecart','torch','totem_of_undying','trader_llama_spawn_egg','trident','tripwire_hook','tropical_fish','tropical_fish_bucket','tropical_fish_spawn_egg','tube_coral','tube_coral_fan','turtle_egg','turtle_helmet','turtle_spawn_egg','vex_spawn_egg','villager_spawn_egg','vindicator_spawn_egg','vine','wandering_trader_spawn_egg','water_bucket','wheat','wheat_seeds','white_dye','white_stained_glass_pane','white_tulip','witch_spawn_egg','wither_rose','wither_skeleton_spawn_egg','wolf_spawn_egg','wooden_axe','wooden_hoe','wooden_pickaxe','wooden_shovel','wooden_sword','writable_book','written_book','yellow_dye','yellow_stained_glass_pane','zombie_horse_spawn_egg','zombie_pigman_spawn_egg','zombie_spawn_egg','zombie_villager_spawn_egg']
   
   spawn_egg_colors={
      "bat_spawn_egg": (4996656, 986895),
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
      "guardian_spawn_egg": (5931634, 15826224),
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
      "zombie_spawn_egg": (44975, 7969893),
      "zombie_horse_spawn_egg": (3232308, 9945732),
      "zombie_pigman_spawn_egg": (15373203, 5009705),
      "zombie_villager_spawn_egg": (5651507, 7969893),
   }
   
   egg_base = vanilla.assets.textures['minecraft:item/spawn_egg'].image.convert('RGBA')
   egg_overlay = vanilla.assets.textures['minecraft:item/spawn_egg_overlay'].image.convert('RGBA')
   arrow_base = vanilla.assets.textures['minecraft:item/tipped_arrow_base'].image.convert('RGBA')
   arrow_overlay = vanilla.assets.textures['minecraft:item/tipped_arrow_head'].image.convert('RGBA')
   
   mcitems = {}
   for entry in itemnames:
      if entry.endswith('_spawn_egg'):
         image = Image.new('RGBA', egg_base.size)
         c1, c2 = spawn_egg_colors[entry]
         image.paste(colorize(egg_base, rgba(c1)), (0, 0, 16,16), egg_base)
         image.paste(colorize(egg_overlay, rgba(c2)), (0, 0, 16,16), egg_overlay)
      elif entry == 'tipped_arrow':
         image = Image.new('RGBA', arrow_base.size)
         image.paste(arrow_base, (0, 0, 16,16), arrow_base)
         image.paste(colorize(arrow_overlay, rgba(0x385dc6)), (0, 0, 16,16), arrow_overlay)
      else:
         lookup = {'crossbow':'crossbow_standby','clock':'clock_00','compass':'compass_00','debug_stick':'stick','enchanted_golden_apple':'golden_apple','large_fern':'large_fern_top','lilac':'lilac_top','peony':'peony_top','rose_bush':'rose_bush_top','sunflower':'sunflower_front','tall_grass':'tall_grass_top'}.get(entry, entry)
         lookup = lookup.replace('glass_pane', 'glass')
         texture = vanilla.assets.textures.get(f'minecraft:item/{lookup}')
         if texture is None:
            texture = vanilla.assets.textures.get(f'minecraft:block/{lookup}')
         if texture is None:
            print(entry)
            image = None
         else:
            image = texture.image.convert('RGBA')
      grassmap = {"vine":0x48b518,"lily_pad":0x71c35c,"grass":0x7bbd6b,"fern":0x7bbd6b,"tall_grass":0x7bbd6b,"large_fern":0x7bbd6b}
      if entry in grassmap:
         image = colorize(image, rgba(grassmap[entry]))
      if entry in ['leather_helmet', 'leather_chestplate', 'leather_leggings', 'leather_boots', 'leather_horse_armor']:
         img_new = Image.new('RGBA', image.size)
         img_new.paste(colorize(image, rgba(0xA06540)), (0, 0, 16, 16), image)
         overlay = vanilla.assets.textures.get(f'minecraft:item/{entry}_overlay')
         if overlay is not None:
            img_new.paste(overlay.image, (0, 0, 16, 16), overlay.image)
         image = img_new
      if entry == 'firework_star':
         overlay = vanilla.assets.textures.get(f'minecraft:item/firework_star_overlay')
         image.paste(colorize(overlay.image, rgba(0x8A8A8A)), (0, 0, 16, 16), overlay.image)
      if entry == 'filled_map':
         overlay = vanilla.assets.textures.get(f'minecraft:item/filled_map_markings')
         image.paste(colorize(overlay.image, rgba(0x46402E)), (0, 0, 16, 16), overlay.image)
      if entry in ['potion', 'lingering_potion', 'splash_potion']:
         overlay = vanilla.assets.textures.get(f'minecraft:item/potion_overlay')
         image.paste(colorize(overlay.image, rgba(0x385dc6)), (0, 0, 16, 16), overlay.image)
      if image is not None:
         mcitems[entry] = image
   tipped_arrow = vanilla.assets.textures['minecraft:item/tipped_arrow_head'].image.convert('RGBA')
   potion = vanilla.assets.textures['minecraft:item/potion_overlay'].image.convert('RGBA')
   mcoverlays = {
   "arrow_dust.fire_resistance": colorize(tipped_arrow, rgba(14981690)),
   "arrow_dust.harming": colorize(tipped_arrow, rgba(4393481)),
   "arrow_dust.healing": colorize(tipped_arrow, rgba(16262179)),
   "arrow_dust.invisibility": colorize(tipped_arrow, rgba(8356754)),
   "arrow_dust.leaping": colorize(tipped_arrow, rgba(2293580)),
   "arrow_dust.luck": colorize(tipped_arrow, rgba(0x339900)),
   "arrow_dust.night_vision": colorize(tipped_arrow, rgba(0x1F1FA1)),
   "arrow_dust.poison": colorize(tipped_arrow, rgba(5149489)),
   "arrow_dust.regeneration": colorize(tipped_arrow, rgba(13458603)),
   "arrow_dust.slow_falling": colorize(tipped_arrow, rgba(16773073)),
   "arrow_dust.slowness": colorize(tipped_arrow, rgba(5926017)),
   "arrow_dust.strength": colorize(tipped_arrow, rgba(9643043)),
   "arrow_dust.swiftness": colorize(tipped_arrow, rgba(8171462)),
   "arrow_dust.turtle_master": colorize(tipped_arrow, rgba(0x755b62)),
   "arrow_dust.water_breathing": colorize(tipped_arrow, rgba(3035801)),
   "arrow_dust.weakness": colorize(tipped_arrow, rgba(0x484D48)),
   "potion_liquid.fire_resistance": colorize(potion, rgba(14981690)),
   "potion_liquid.harming": colorize(potion, rgba(4393481)),
   "potion_liquid.healing": colorize(potion, rgba(16262179)),
   "potion_liquid.invisibility": colorize(potion, rgba(8356754)),
   "potion_liquid.leaping": colorize(potion, rgba(2293580)),
   "potion_liquid.luck": colorize(potion, rgba(0x339900)),
   "potion_liquid.night_vision": colorize(potion, rgba(0x1F1FA1)),
   "potion_liquid.poison": colorize(potion, rgba(5149489)),
   "potion_liquid.regeneration": colorize(potion, rgba(13458603)),
   "potion_liquid.slow_falling": colorize(potion, rgba(16773073)),
   "potion_liquid.slowness": colorize(potion, rgba(5926017)),
   "potion_liquid.strength": colorize(potion, rgba(9643043)),
   "potion_liquid.swiftness": colorize(potion, rgba(8171462)),
   "potion_liquid.turtle_master": colorize(potion, rgba(0x755b62)),
   "potion_liquid.water_breathing": colorize(potion, rgba(3035801)),
   "potion_liquid.weakness": colorize(potion, rgba(0x484D48)),
   }
   
   for entry in blocknames:
      if 'shulker_box' in entry:
         tx = ('shulker_' + entry.removesuffix('shulker_box')).removesuffix('_')
         sbox = model_resolver.item_model.special.SpecialModelShulkerBox(type='shulker_box', texture=tx)
         model = sbox.get_model(None, None)
         ctx.assets.models[f'minecraft:item/{entry}'] = beet.Model(model)
      if 'banner' in entry:
         color = '_'.join(entry.split('_')[:-1])
         banner = model_resolver.item_model.special.SpecialModelBanner(type='banner', color=color)
         display = vanilla.assets.models['minecraft:item/template_banner'].data
         model = banner.get_model(None, None)
         model['display'] = display['display']
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
         display = copy.deepcopy(vanilla.assets.models['minecraft:item/template_skull'].data)
         model['display'] = display['display']
         if entry == 'dragon_head':
            model['display']['gui']['scale'] = [0.5, 0.5, 0.5]
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
         display = vanilla.assets.models['minecraft:item/chest'].data
         chest = model_resolver.item_model.special.SpecialModelChest(type='chest', texture=tx)
         model = {"textures":{"0":f"entity/chest/{tx}"},"elements":[{"from":[1, 0, 1],"to":[15, 10, 15],"faces":{"north":{"uv":[14, 10.75, 10.5, 8.25],"rotation":180,"texture":"#0"},"east":{"uv":[3.5, 10.75, 0, 8.25],"rotation":180,"texture":"#0"},"south":{"uv":[7, 10.75, 3.5, 8.25],"rotation":180,"texture":"#0"},"west":{"uv":[10.5, 10.75, 7, 8.25],"rotation":180,"texture":"#0"},"up":{"uv":[3.5, 4.75, 7, 8.25],"rotation":180,"texture":"#0"},"down":{"uv":[7, 4.75, 10.5, 8.25],"rotation":180,"texture":"#0"}}},{"from":[1, 9, 1],"to":[15, 14, 15],"rotation":{"angle":0,"axis":"x","origin":[8, 10, 1]},"faces":{"north":{"uv":[14, 4.75, 10.5, 3.5],"rotation":180,"texture":"#0"},"east":{"uv":[3.5, 4.75, 0, 3.5],"rotation":180,"texture":"#0"},"south":{"uv":[7, 4.75, 3.5, 3.5],"rotation":180,"texture":"#0"},"west":{"uv":[10.5, 4.75, 7, 3.5],"rotation":180,"texture":"#0"},"up":{"uv":[7, 3.5, 3.5, 0],"rotation":180,"texture":"#0"},"down":{"uv":[7, 0, 10.5, 3.5],"rotation":180,"texture":"#0"}}},{"from":[7, 7, 14],"to":[9, 11, 16],"rotation":{"angle":0,"axis":"x","origin":[8, 10, 1]},"faces":{"north":{"uv":[0.75, 1.25, 0.25, 0.25],"rotation":180,"texture":"#0"},"east":{"uv":[1, 1.25, 0.75, 0.25],"rotation":180,"texture":"#0"},"south":{"uv":[1.5, 1.25, 1, 0.25],"rotation":180,"texture":"#0"},"west":{"uv":[0.25, 1.25, 0, 0.25],"rotation":180,"texture":"#0"},"up":{"uv":[0.25, 0, 0.75, 0.25],"texture":"#0"},"down":{"uv":[0.75, 0, 1.25, 0.25],"texture":"#0"}}}]}
         model['display'] = display['display']
         ctx.assets.models[f'minecraft:item/{entry}'] = beet.Model(model)

   renderer = model_resolver.Render(ctx=ctx)
   renderer.default_render_size = 64
   for entry in blocknames:         
      renderer.add_model_task(
         model=f'minecraft:item/{entry}',
         path_ctx=f'render:{entry}',
         animation_mode = 'one_file'
      )
   renderer.run()
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

   # create grids
   print("Creating image sheets...")
   itemgrid=create_grid(mcitems)
   itemsheet=create_image(itemgrid, 16)
   ctx.assets.textures['tryashtar.shulker_preview:item_sheet'] = beet.Texture(itemsheet)
   blockgrid=create_grid(mcblocks)
   blocksheet=create_image(blockgrid, 64)
   ctx.assets.textures['tryashtar.shulker_preview:block_sheet'] = beet.Texture(blocksheet)
   overlaygrid=create_grid(mcoverlays)
   overlaysheet=create_image(overlaygrid, 16)
   ctx.assets.textures['tryashtar.shulker_preview:overlay_sheet'] = beet.Texture(overlaysheet)

   # start creating font providers
   print("Generating font providers...")
   providers=[{"comment":"Many thanks to AmberW#4615 for this invaluable concept","type":"bitmap","file":"tryashtar.shulker_preview:pixel.png","ascent":-32768,"height":-3,"chars":["\uf801"]},{"type":"bitmap","file":"tryashtar.shulker_preview:pixel.png","ascent":-32768,"height":-4,"chars":["\uf802"]},{"type":"bitmap","file":"tryashtar.shulker_preview:pixel.png","ascent":-32768,"height":-5,"chars":["\uf803"]},{"type":"bitmap","file":"tryashtar.shulker_preview:pixel.png","ascent":-32768,"height":-6,"chars":["\uf804"]},{"type":"bitmap","file":"tryashtar.shulker_preview:pixel.png","ascent":-32768,"height":-7,"chars":["\uf805"]},{"type":"bitmap","file":"tryashtar.shulker_preview:pixel.png","ascent":-32768,"height":-8,"chars":["\uf806"]},{"type":"bitmap","file":"tryashtar.shulker_preview:pixel.png","ascent":-32768,"height":-9,"chars":["\uf807"]},{"type":"bitmap","file":"tryashtar.shulker_preview:pixel.png","ascent":-32768,"height":-10,"chars":["\uf808"]},{"type":"bitmap","file":"tryashtar.shulker_preview:pixel.png","ascent":-32768,"height":-18,"chars":["\uf809"]},{"type":"bitmap","file":"tryashtar.shulker_preview:pixel.png","ascent":-32768,"height":-34,"chars":["\uf80a"]},{"type":"bitmap","file":"tryashtar.shulker_preview:pixel.png","ascent":-32768,"height":-66,"chars":["\uf80b"]},{"type":"bitmap","file":"tryashtar.shulker_preview:pixel.png","ascent":-32768,"height":-130,"chars":["\uf80c"]},{"type":"bitmap","file":"tryashtar.shulker_preview:pixel.png","ascent":-32768,"height":-258,"chars":["\uf80d"]},{"type":"bitmap","file":"tryashtar.shulker_preview:pixel.png","ascent":-32768,"height":-514,"chars":["\uf80e"]},{"type":"bitmap","file":"tryashtar.shulker_preview:pixel.png","ascent":-32768,"height":-1026,"chars":["\uf80f"]},{"type":"bitmap","file":"tryashtar.shulker_preview:pixel.png","ascent":-32768,"height":0,"chars":["\uf821"]},{"type":"bitmap","file":"tryashtar.shulker_preview:pixel.png","ascent":-32768,"height":1,"chars":["\uf822"]},{"type":"bitmap","file":"tryashtar.shulker_preview:pixel.png","ascent":-32768,"height":2,"chars":["\uf823"]},{"type":"bitmap","file":"tryashtar.shulker_preview:pixel.png","ascent":-32768,"height":3,"chars":["\uf824"]},{"type":"bitmap","file":"tryashtar.shulker_preview:pixel.png","ascent":-32768,"height":4,"chars":["\uf825"]},{"type":"bitmap","file":"tryashtar.shulker_preview:pixel.png","ascent":-32768,"height":5,"chars":["\uf826"]},{"type":"bitmap","file":"tryashtar.shulker_preview:pixel.png","ascent":-32768,"height":6,"chars":["\uf827"]},{"type":"bitmap","file":"tryashtar.shulker_preview:pixel.png","ascent":-32768,"height":7,"chars":["\uf828"]},{"type":"bitmap","file":"tryashtar.shulker_preview:pixel.png","ascent":-32768,"height":15,"chars":["\uf829"]},{"type":"bitmap","file":"tryashtar.shulker_preview:pixel.png","ascent":-32768,"height":31,"chars":["\uf82a"]},{"type":"bitmap","file":"tryashtar.shulker_preview:pixel.png","ascent":-32768,"height":63,"chars":["\uf82b"]},{"type":"bitmap","file":"tryashtar.shulker_preview:pixel.png","ascent":-32768,"height":127,"chars":["\uf82c"]},{"type":"bitmap","file":"tryashtar.shulker_preview:pixel.png","ascent":-32768,"height":255,"chars":["\uf82d"]},{"type":"bitmap","file":"tryashtar.shulker_preview:pixel.png","ascent":-32768,"height":511,"chars":["\uf82e"]},{"type":"bitmap","file":"tryashtar.shulker_preview:pixel.png","ascent":-32768,"height":1023,"chars":["\uf82f"]},{"type":"bitmap","file":"tryashtar.shulker_preview:pixel.png","ascent":-32770,"height":-32770,"chars":["\uf800"]},{"type":"bitmap","file":"tryashtar.shulker_preview:pixel.png","ascent":-32768,"height":32767,"chars":["\uf820"]},{"type":"bitmap","file":"tryashtar.shulker_preview:comma.png","ascent":7,"chars":[","]}]
   providers.append(register_single("tryashtar.shulker_preview:shulker_tooltip.png", "shulker_tooltip", 23, 78, (["max",-4],[-175,"-max"])))
   providers.append(register_single("tryashtar.shulker_preview:shulker_tooltip_header.png", "shulker_tooltip_header", 23, 78, (["max",-4],[-175,"-max"])))
   providers.append(register_single("tryashtar.shulker_preview:ender_tooltip.png", "ender_tooltip", 23, 78, (["max",-4],[-175,"-max"])))

   # per-row icons
   for row in range(0, 3):
      height=-18*row
      numbers=[f"number.{i}.{row}" for i in range(0,10)]
      providers.append(register_grid("tryashtar.shulker_preview:numbers.png", [numbers], height-4, 8, (["max",-7],[-6,"-max"])))
      dur1=[f"durability.{i}.{row}" for i in range(1,6)]
      dur2=[f"durability.{i}.{row}" for i in range(6,11)]
      dur3=[f"durability.{i}.{row}" for i in range(11,15)]+[None]
      providers.append(register_grid("tryashtar.shulker_preview:durability.png", [dur1,dur2,dur3], height-8, 2, (["max",-16],[-4,"-max"])))

      # item/block/overlay grids
      providers.append(register_grid("tryashtar.shulker_preview:item_sheet.png", apply_to_all(grid_keys(itemgrid), lambda x: f"item.{x}.{row}"), height+5, 16, (["max"],[-5,"-max"])))
      providers.append(register_grid("tryashtar.shulker_preview:block_sheet.png", apply_to_all(grid_keys(blockgrid), lambda x: f"block.{x}.{row}"), height+5, 16, (["max"],[-5,"-max"])))
      providers.append(register_grid("tryashtar.shulker_preview:overlay_sheet.png", apply_to_all(grid_keys(overlaygrid), lambda x: f"overlay.{x}.{row}"), height+5, 16, (["max",-18],[-5,"-max"])))

      # remaining numbers 10-64
      for n in range(10, 65):
         digit1=str(n)[0]
         digit2=str(n)[1]
         translations[f"tryashtar.shulker_preview.number.{n}.{row}"]=get_spacing(["max",-13])+charmap[f"number.{digit1}.{row}"]+get_spacing([-1])+charmap[f"number.{digit2}.{row}"]+get_spacing([-6,"-max"])

   # write translations and providers
   print("Writing JSONs...")
   ctx.assets.languages['minecraft:en_us'] = beet.Language(translations)
   ctx.assets.fonts['minecraft:default'] = beet.Font({"providers":providers})

   # create dictionary of item lengths
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
         ctx.data.functions[f'tryashtar.shulker_preview:row_{row}/process_item\\length_{length}'] = beet.Function(sublines)
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
            command += "{id:shulker_box,Count:1b,Slot:" +str(boxes)+ "b,tag:{BlockEntityTag:{Items:["
            boxes += 1
         command += "{id:\"" +item+ "\",Count:1b,Slot:" +str(boxslot)+ "b},"
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

   ctx.assets.save(path='out/resourcepack', overwrite=True)
   ctx.assets.save(path=f'out/Shulker Preview Resource Pack ({ctx.minecraft_version}).zip', zipped=True, overwrite=True)
   ctx.data.save(path='out/datapack', overwrite=True)
   ctx.data.save(path=f'out/Shulker Preview Data Pack ({ctx.minecraft_version}).zip', zipped=True, overwrite=True)
   dark_theme = beet.ResourcePack(path='in/resourcepack_dark')
   dark_theme.pack_format = ctx.assets.pack_format
   dark_theme.description = '(apply this pack above the normal resource pack)'
   dark_theme.save(path='out/dark_theme', overwrite=True)
   dark_theme.save(path=f'out/Shulker Preview Dark Theme ({ctx.minecraft_version}).zip', zipped=True, overwrite=True)

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

# fewest positive/negative spaces required to move this many pixels
positive_spaces=OrderedDict([(1024,'\uF82F'),(512,'\uF82E'),(256,'\uF82D'),(128,'\uF82C'),(64,'\uF82B'),(32,'\uF82A'),(16,'\uF829'),(8,'\uF828'),(7,'\uF827'),(6,'\uF826'),(5,'\uF825'),(4,'\uF824'),(3,'\uF823'),(2,'\uF822'),(1,'\uF821')])
negative_spaces=OrderedDict([(-1024,'\uF80F'),(-512,'\uF80E'),(-256,'\uF80D'),(-128,'\uF80C'),(-64,'\uF80B'),(-32,'\uF80A'),(-16,'\uF809'),(-8,'\uF808'),(-7,'\uF807'),(-6,'\uF806'),(-5,'\uF805'),(-4,'\uF804'),(-3,'\uF803'),(-2,'\uF802'),(-1,'\uF801')])
# input is list of spaces to apply
# numbers are in pixels, alternativey "max" or "-max" in sequence applies respective size space
def get_spacing(sequence):
   result=""
   for pixels in sequence:
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

currentchar='\uE000'
charmap={}
translations={"%1$s":"%2$s","tryashtar.shulker_preview.empty_slot":get_spacing(["max",12,"-max"]),"tryashtar.shulker_preview.row_end":get_spacing(["max",-168,"-max"])}
# create a provider from file name, grid of icon names, and ascent/height
# returns provider and also modifies charmap, a global [icon->character code] dictionary, and translations, which is charmap but with prefixed keys, and values padded with positive/negative spaces as specified in spacing
def register_grid(fileid, icongrid, ascent, height, spacing):
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
         translations[f"tryashtar.shulker_preview.{entry}"]=get_spacing(spacing[0])+currentchar+get_spacing(spacing[1])
         string+=currentchar
         currentchar=chr(ord(currentchar)+1)
      chars.append(string)
   base["chars"]=chars
   return base

# shortcut to create provider from one image
def register_single(fileid, iconname, ascent, height, spacing):
   return register_grid(fileid, [[iconname]], ascent, height, spacing)

# take [item name->path] dictionary and form it into an ordered square 2D array of tuples (missing spaces are filled in with None)
def create_grid(icondict):
   size=get_dimensions(len(icondict))
   ordered=sorted(icondict.items(), key=lambda x: x[0])
   ordered.extend([None]*(size[0]*size[1]-len(ordered)))
   result=numpy.array(ordered, dtype=object)
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
durability_dict={"leather_helmet":55,"leather_chestplate":80,"leather_leggings":75,"leather_boots":65,"golden_helmet":77,"golden_chestplate":112,"golden_leggings":105,"golden_boots":91,"chainmail_helmet":165,"chainmail_chestplate":240,"chainmail_leggings":225,"chainmail_boots":195,"iron_helmet":165,"iron_chestplate":240,"iron_leggings":225,"iron_boots":195,"diamond_helmet":363,"diamond_chestplate":528,"diamond_leggings":495,"diamond_boots":429,"golden_axe":32,"golden_pickaxe":32,"golden_shovel":32,"golden_hoe":32,"golden_sword":32,"wooden_axe":59,"wooden_pickaxe":59,"wooden_shovel":59,"wooden_hoe":59,"wooden_sword":59,"stone_axe":131,"stone_pickaxe":131,"stone_shovel":131,"stone_hoe":131,"stone_sword":131,"iron_axe":250,"iron_pickaxe":250,"iron_shovel":250,"iron_hoe":250,"iron_sword":250,"diamond_axe":1561,"diamond_pickaxe":1561,"diamond_shovel":1561,"diamond_hoe":1561,"diamond_sword":1561,"fishing_rod":64,"flint_and_steel":64,"carrot_on_a_stick":25,"shears":238,"shield":336,"bow":384,"trident":250,"elytra":432,"crossbow":326}
potion_dict={"night_vision":"night_vision","long_night_vision":"night_vision","invisibility":"invisibility","long_invisibility":"invisibility","leaping":"leaping","strong_leaping":"leaping","long_leaping":"leaping","fire_resistance":"fire_resistance","long_fire_resistance":"fire_resistance","swiftness":"swiftness","strong_swiftness":"swiftness","long_swiftness":"swiftness","water_breathing":"water_breathing","long_water_breathing":"water_breathing","healing":"healing","strong_healing":"healing","harming":"harming","strong_harming":"harming","poison":"poison","strong_poison":"poison","long_poison":"poison","regeneration":"regeneration","strong_regeneration":"regeneration","long_regeneration":"regeneration","strength":"strength","strong_strength":"strength","long_strength":"strength","weakness":"weakness","long_weakness":"weakness","luck":"luck","turtle_master":"turtle_master","strong_turtle_master":"turtle_master","long_turtle_master":"turtle_master","slow_falling":"slow_falling","long_slow_falling":"slow_falling"}

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
