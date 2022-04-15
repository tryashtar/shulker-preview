execute if data storage tryashtar.shulker_preview:data item{id:"minecraft:blue_stained_glass"} run summon marker ~ ~ ~ {Tags:["tryashtar.shulker_preview"],CustomName:'{"translate":"tryashtar.shulker_preview.block.blue_stained_glass.0"}'}
execute if data storage tryashtar.shulker_preview:data item{id:"minecraft:bubble_coral_block"} run summon marker ~ ~ ~ {Tags:["tryashtar.shulker_preview"],CustomName:'{"translate":"tryashtar.shulker_preview.block.bubble_coral_block.0"}'}
execute if data storage tryashtar.shulker_preview:data item{id:"minecraft:chainmail_leggings"} run summon marker ~ ~ ~ {Tags:["tryashtar.shulker_preview"],CustomName:'{"translate":"tryashtar.shulker_preview.item.chainmail_leggings.0"}'}
execute if data storage tryashtar.shulker_preview:data item{id:"minecraft:chainmail_leggings"} run scoreboard players set #max shulker_preview 225
execute if data storage tryashtar.shulker_preview:data item{id:"minecraft:chiseled_deepslate"} run summon marker ~ ~ ~ {Tags:["tryashtar.shulker_preview"],CustomName:'{"translate":"tryashtar.shulker_preview.block.chiseled_deepslate.0"}'}
execute if data storage tryashtar.shulker_preview:data item{id:"minecraft:chiseled_sandstone"} run summon marker ~ ~ ~ {Tags:["tryashtar.shulker_preview"],CustomName:'{"translate":"tryashtar.shulker_preview.block.chiseled_sandstone.0"}'}
execute if data storage tryashtar.shulker_preview:data item{id:"minecraft:cobblestone_stairs"} run summon marker ~ ~ ~ {Tags:["tryashtar.shulker_preview"],CustomName:'{"translate":"tryashtar.shulker_preview.block.cobblestone_stairs.0"}'}
execute if data storage tryashtar.shulker_preview:data item{id:"minecraft:crimson_fence_gate"} run summon marker ~ ~ ~ {Tags:["tryashtar.shulker_preview"],CustomName:'{"translate":"tryashtar.shulker_preview.block.crimson_fence_gate.0"}'}
execute if data storage tryashtar.shulker_preview:data item{id:"minecraft:cut_sandstone_slab"} run summon marker ~ ~ ~ {Tags:["tryashtar.shulker_preview"],CustomName:'{"translate":"tryashtar.shulker_preview.block.cut_sandstone_slab.0"}'}
execute if data storage tryashtar.shulker_preview:data item{id:"minecraft:cyan_stained_glass"} run summon marker ~ ~ ~ {Tags:["tryashtar.shulker_preview"],CustomName:'{"translate":"tryashtar.shulker_preview.block.cyan_stained_glass.0"}'}
execute if data storage tryashtar.shulker_preview:data item{id:"minecraft:deepslate_coal_ore"} run summon marker ~ ~ ~ {Tags:["tryashtar.shulker_preview"],CustomName:'{"translate":"tryashtar.shulker_preview.block.deepslate_coal_ore.0"}'}
execute if data storage tryashtar.shulker_preview:data item{id:"minecraft:deepslate_gold_ore"} run summon marker ~ ~ ~ {Tags:["tryashtar.shulker_preview"],CustomName:'{"translate":"tryashtar.shulker_preview.block.deepslate_gold_ore.0"}'}
execute if data storage tryashtar.shulker_preview:data item{id:"minecraft:deepslate_iron_ore"} run summon marker ~ ~ ~ {Tags:["tryashtar.shulker_preview"],CustomName:'{"translate":"tryashtar.shulker_preview.block.deepslate_iron_ore.0"}'}
execute if data storage tryashtar.shulker_preview:data item{id:"minecraft:diamond_chestplate"} run summon marker ~ ~ ~ {Tags:["tryashtar.shulker_preview"],CustomName:'{"translate":"tryashtar.shulker_preview.item.diamond_chestplate.0"}'}
execute if data storage tryashtar.shulker_preview:data item{id:"minecraft:diamond_chestplate"} run scoreboard players set #max shulker_preview 528
execute if data storage tryashtar.shulker_preview:data item{id:"minecraft:enderman_spawn_egg"} run summon marker ~ ~ ~ {Tags:["tryashtar.shulker_preview"],CustomName:'[{"translate":"tryashtar.shulker_preview.item.spawn_egg.0","color":"#161616"},{"translate":"tryashtar.shulker_preview.overlay.spawn_egg_overlay.0","color":"#000000"}]'}
execute if data storage tryashtar.shulker_preview:data item{id:"minecraft:exposed_cut_copper"} run summon marker ~ ~ ~ {Tags:["tryashtar.shulker_preview"],CustomName:'{"translate":"tryashtar.shulker_preview.block.exposed_cut_copper.0"}'}
execute if data storage tryashtar.shulker_preview:data item{id:"minecraft:golden_horse_armor"} run summon marker ~ ~ ~ {Tags:["tryashtar.shulker_preview"],CustomName:'{"translate":"tryashtar.shulker_preview.item.golden_horse_armor.0"}'}
execute if data storage tryashtar.shulker_preview:data item{id:"minecraft:gray_stained_glass"} run summon marker ~ ~ ~ {Tags:["tryashtar.shulker_preview"],CustomName:'{"translate":"tryashtar.shulker_preview.block.gray_stained_glass.0"}'}
execute if data storage tryashtar.shulker_preview:data item{id:"minecraft:guardian_spawn_egg"} run summon marker ~ ~ ~ {Tags:["tryashtar.shulker_preview"],CustomName:'[{"translate":"tryashtar.shulker_preview.item.spawn_egg.0","color":"#5a8272"},{"translate":"tryashtar.shulker_preview.overlay.spawn_egg_overlay.0","color":"#f17d30"}]'}
execute if data storage tryashtar.shulker_preview:data item{id:"minecraft:infested_deepslate"} run summon marker ~ ~ ~ {Tags:["tryashtar.shulker_preview"],CustomName:'{"translate":"tryashtar.shulker_preview.block.infested_deepslate.0"}'}
execute if data storage tryashtar.shulker_preview:data item{id:"minecraft:large_amethyst_bud"} run summon marker ~ ~ ~ {Tags:["tryashtar.shulker_preview"],CustomName:'{"translate":"tryashtar.shulker_preview.item.large_amethyst_bud.0"}'}
execute if data storage tryashtar.shulker_preview:data item{id:"minecraft:leather_chestplate"} unless data storage tryashtar.shulker_preview:data item.tag.display.color run summon marker ~ ~ ~ {Tags:["tryashtar.shulker_preview"],CustomName:'{"translate":"tryashtar.shulker_preview.item.leather_chestplate.0","color":"#a06540"}'}
execute if data storage tryashtar.shulker_preview:data item{id:"minecraft:leather_chestplate"} if data storage tryashtar.shulker_preview:data item.tag.display.color run function tryashtar.shulker_preview:row_0/dye_armor/chestplate
execute if data storage tryashtar.shulker_preview:data item{id:"minecraft:leather_chestplate"} run scoreboard players set #max shulker_preview 80
execute if data storage tryashtar.shulker_preview:data item{id:"minecraft:lily_of_the_valley"} run summon marker ~ ~ ~ {Tags:["tryashtar.shulker_preview"],CustomName:'{"translate":"tryashtar.shulker_preview.item.lily_of_the_valley.0"}'}
execute if data storage tryashtar.shulker_preview:data item{id:"minecraft:lime_stained_glass"} run summon marker ~ ~ ~ {Tags:["tryashtar.shulker_preview"],CustomName:'{"translate":"tryashtar.shulker_preview.block.lime_stained_glass.0"}'}
execute if data storage tryashtar.shulker_preview:data item{id:"minecraft:magenta_terracotta"} run summon marker ~ ~ ~ {Tags:["tryashtar.shulker_preview"],CustomName:'{"translate":"tryashtar.shulker_preview.block.magenta_terracotta.0"}'}
execute if data storage tryashtar.shulker_preview:data item{id:"minecraft:mangrove_propagule"} run summon marker ~ ~ ~ {Tags:["tryashtar.shulker_preview"],CustomName:'{"translate":"tryashtar.shulker_preview.item.mangrove_propagule.0"}'}
execute if data storage tryashtar.shulker_preview:data item{id:"minecraft:mossy_stone_bricks"} run summon marker ~ ~ ~ {Tags:["tryashtar.shulker_preview"],CustomName:'{"translate":"tryashtar.shulker_preview.block.mossy_stone_bricks.0"}'}
execute if data storage tryashtar.shulker_preview:data item{id:"minecraft:music_disc_mellohi"} run summon marker ~ ~ ~ {Tags:["tryashtar.shulker_preview"],CustomName:'{"translate":"tryashtar.shulker_preview.item.music_disc_mellohi.0"}'}
execute if data storage tryashtar.shulker_preview:data item{id:"minecraft:music_disc_pigstep"} run summon marker ~ ~ ~ {Tags:["tryashtar.shulker_preview"],CustomName:'{"translate":"tryashtar.shulker_preview.item.music_disc_pigstep.0"}'}
execute if data storage tryashtar.shulker_preview:data item{id:"minecraft:nether_brick_fence"} run summon marker ~ ~ ~ {Tags:["tryashtar.shulker_preview"],CustomName:'{"translate":"tryashtar.shulker_preview.block.nether_brick_fence.0"}'}
execute if data storage tryashtar.shulker_preview:data item{id:"minecraft:netherite_leggings"} run summon marker ~ ~ ~ {Tags:["tryashtar.shulker_preview"],CustomName:'{"translate":"tryashtar.shulker_preview.item.netherite_leggings.0"}'}
execute if data storage tryashtar.shulker_preview:data item{id:"minecraft:netherite_leggings"} run scoreboard players set #max shulker_preview 555
execute if data storage tryashtar.shulker_preview:data item{id:"minecraft:oak_pressure_plate"} run summon marker ~ ~ ~ {Tags:["tryashtar.shulker_preview"],CustomName:'{"translate":"tryashtar.shulker_preview.block.oak_pressure_plate.0"}'}
execute if data storage tryashtar.shulker_preview:data item{id:"minecraft:orange_shulker_box"} run summon marker ~ ~ ~ {Tags:["tryashtar.shulker_preview"],CustomName:'{"translate":"tryashtar.shulker_preview.block.orange_shulker_box.0"}'}
execute if data storage tryashtar.shulker_preview:data item{id:"minecraft:petrified_oak_slab"} run summon marker ~ ~ ~ {Tags:["tryashtar.shulker_preview"],CustomName:'{"translate":"tryashtar.shulker_preview.block.petrified_oak_slab.0"}'}
execute if data storage tryashtar.shulker_preview:data item{id:"minecraft:pillager_spawn_egg"} run summon marker ~ ~ ~ {Tags:["tryashtar.shulker_preview"],CustomName:'[{"translate":"tryashtar.shulker_preview.item.spawn_egg.0","color":"#532f36"},{"translate":"tryashtar.shulker_preview.overlay.spawn_egg_overlay.0","color":"#959b9b"}]'}
execute if data storage tryashtar.shulker_preview:data item{id:"minecraft:pink_stained_glass"} run summon marker ~ ~ ~ {Tags:["tryashtar.shulker_preview"],CustomName:'{"translate":"tryashtar.shulker_preview.block.pink_stained_glass.0"}'}
execute if data storage tryashtar.shulker_preview:data item{id:"minecraft:polished_deepslate"} run summon marker ~ ~ ~ {Tags:["tryashtar.shulker_preview"],CustomName:'{"translate":"tryashtar.shulker_preview.block.polished_deepslate.0"}'}
execute if data storage tryashtar.shulker_preview:data item{id:"minecraft:powder_snow_bucket"} run summon marker ~ ~ ~ {Tags:["tryashtar.shulker_preview"],CustomName:'{"translate":"tryashtar.shulker_preview.item.powder_snow_bucket.0"}'}
execute if data storage tryashtar.shulker_preview:data item{id:"minecraft:purple_shulker_box"} run summon marker ~ ~ ~ {Tags:["tryashtar.shulker_preview"],CustomName:'{"translate":"tryashtar.shulker_preview.block.purple_shulker_box.0"}'}
execute if data storage tryashtar.shulker_preview:data item{id:"minecraft:red_mushroom_block"} run summon marker ~ ~ ~ {Tags:["tryashtar.shulker_preview"],CustomName:'{"translate":"tryashtar.shulker_preview.block.red_mushroom_block.0"}'}
execute if data storage tryashtar.shulker_preview:data item{id:"minecraft:red_sandstone_slab"} run summon marker ~ ~ ~ {Tags:["tryashtar.shulker_preview"],CustomName:'{"translate":"tryashtar.shulker_preview.block.red_sandstone_slab.0"}'}
execute if data storage tryashtar.shulker_preview:data item{id:"minecraft:red_sandstone_wall"} run summon marker ~ ~ ~ {Tags:["tryashtar.shulker_preview"],CustomName:'{"translate":"tryashtar.shulker_preview.block.red_sandstone_wall.0"}'}
execute if data storage tryashtar.shulker_preview:data item{id:"minecraft:skeleton_spawn_egg"} run summon marker ~ ~ ~ {Tags:["tryashtar.shulker_preview"],CustomName:'[{"translate":"tryashtar.shulker_preview.item.spawn_egg.0","color":"#c1c1c1"},{"translate":"tryashtar.shulker_preview.overlay.spawn_egg_overlay.0","color":"#494949"}]'}
execute if data storage tryashtar.shulker_preview:data item{id:"minecraft:small_amethyst_bud"} run summon marker ~ ~ ~ {Tags:["tryashtar.shulker_preview"],CustomName:'{"translate":"tryashtar.shulker_preview.item.small_amethyst_bud.0"}'}
execute if data storage tryashtar.shulker_preview:data item{id:"minecraft:smooth_quartz_slab"} run summon marker ~ ~ ~ {Tags:["tryashtar.shulker_preview"],CustomName:'{"translate":"tryashtar.shulker_preview.block.smooth_quartz_slab.0"}'}
execute if data storage tryashtar.shulker_preview:data item{id:"minecraft:stone_brick_stairs"} run summon marker ~ ~ ~ {Tags:["tryashtar.shulker_preview"],CustomName:'{"translate":"tryashtar.shulker_preview.block.stone_brick_stairs.0"}'}
execute if data storage tryashtar.shulker_preview:data item{id:"minecraft:stripped_birch_log"} run summon marker ~ ~ ~ {Tags:["tryashtar.shulker_preview"],CustomName:'{"translate":"tryashtar.shulker_preview.block.stripped_birch_log.0"}'}
execute if data storage tryashtar.shulker_preview:data item{id:"minecraft:villager_spawn_egg"} run summon marker ~ ~ ~ {Tags:["tryashtar.shulker_preview"],CustomName:'[{"translate":"tryashtar.shulker_preview.item.spawn_egg.0","color":"#563c33"},{"translate":"tryashtar.shulker_preview.overlay.spawn_egg_overlay.0","color":"#bd8b72"}]'}
execute if data storage tryashtar.shulker_preview:data item{id:"minecraft:waxed_copper_block"} run summon marker ~ ~ ~ {Tags:["tryashtar.shulker_preview"],CustomName:'{"translate":"tryashtar.shulker_preview.block.waxed_copper_block.0"}'}
execute if data storage tryashtar.shulker_preview:data item{id:"minecraft:yellow_shulker_box"} run summon marker ~ ~ ~ {Tags:["tryashtar.shulker_preview"],CustomName:'{"translate":"tryashtar.shulker_preview.block.yellow_shulker_box.0"}'}
execute store result score #durability shulker_preview run data get storage tryashtar.shulker_preview:data item.tag.Damage
execute if data storage tryashtar.shulker_preview:data item.tag.Damage run function tryashtar.shulker_preview:row_0/overlay/durability
