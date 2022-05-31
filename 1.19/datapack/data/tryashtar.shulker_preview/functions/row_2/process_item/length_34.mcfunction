execute if data storage tryashtar.shulker_preview:data item{id:"minecraft:black_stained_glass_pane"} run data modify storage tryashtar.shulker_preview:data results[-1] set value '{"translate":"tryashtar.shulker_preview.item.black_stained_glass.2"}'
execute if data storage tryashtar.shulker_preview:data item{id:"minecraft:brown_stained_glass_pane"} run data modify storage tryashtar.shulker_preview:data results[-1] set value '{"translate":"tryashtar.shulker_preview.item.brown_stained_glass.2"}'
execute if data storage tryashtar.shulker_preview:data item{id:"minecraft:cobbled_deepslate_stairs"} run data modify storage tryashtar.shulker_preview:data results[-1] set value '{"translate":"tryashtar.shulker_preview.block.cobbled_deepslate.2","color":"#1607fc"}'
execute if data storage tryashtar.shulker_preview:data item{id:"minecraft:cracked_deepslate_bricks"} run data modify storage tryashtar.shulker_preview:data results[-1] set value '{"translate":"tryashtar.shulker_preview.block.cracked_deepslate_bricks.2","color":"#0107fc"}'
execute if data storage tryashtar.shulker_preview:data item{id:"minecraft:elder_guardian_spawn_egg"} run data modify storage tryashtar.shulker_preview:data results[-1] set value '[{"translate":"tryashtar.shulker_preview.item.spawn_egg.2","color":"#ceccba"},{"translate":"tryashtar.shulker_preview.overlay"},{"translate":"tryashtar.shulker_preview.item.spawn_egg_overlay.2","color":"#747693"}]'
execute if data storage tryashtar.shulker_preview:data item{id:"minecraft:green_stained_glass_pane"} run data modify storage tryashtar.shulker_preview:data results[-1] set value '{"translate":"tryashtar.shulker_preview.item.green_stained_glass.2"}'
execute if data storage tryashtar.shulker_preview:data item{id:"minecraft:light_blue_stained_glass"} run data modify storage tryashtar.shulker_preview:data results[-1] set value '{"translate":"tryashtar.shulker_preview.block.light_blue_stained_glass.2","color":"#0107fc"}'
execute if data storage tryashtar.shulker_preview:data item{id:"minecraft:light_gray_stained_glass"} run data modify storage tryashtar.shulker_preview:data results[-1] set value '{"translate":"tryashtar.shulker_preview.block.light_gray_stained_glass.2","color":"#0107fc"}'
execute if data storage tryashtar.shulker_preview:data item{id:"minecraft:mossy_cobblestone_stairs"} run data modify storage tryashtar.shulker_preview:data results[-1] set value '{"translate":"tryashtar.shulker_preview.block.mossy_cobblestone.2","color":"#1607fc"}'
execute if data storage tryashtar.shulker_preview:data item{id:"minecraft:mossy_stone_brick_stairs"} run data modify storage tryashtar.shulker_preview:data results[-1] set value '{"translate":"tryashtar.shulker_preview.block.mossy_stone_bricks.2","color":"#1607fc"}'
execute if data storage tryashtar.shulker_preview:data item{id:"minecraft:orange_glazed_terracotta"} run data modify storage tryashtar.shulker_preview:data results[-1] set value '{"translate":"tryashtar.shulker_preview.block.orange_glazed_terracotta.2","color":"#3307fc"}'
execute if data storage tryashtar.shulker_preview:data item{id:"minecraft:oxidized_cut_copper_slab"} run data modify storage tryashtar.shulker_preview:data results[-1] set value '{"translate":"tryashtar.shulker_preview.block.oxidized_cut_copper.2","color":"#0e07fc"}'
execute if data storage tryashtar.shulker_preview:data item{id:"minecraft:polished_andesite_stairs"} run data modify storage tryashtar.shulker_preview:data results[-1] set value '{"translate":"tryashtar.shulker_preview.block.polished_andesite.2","color":"#1607fc"}'
execute if data storage tryashtar.shulker_preview:data item{id:"minecraft:polished_blackstone_slab"} run data modify storage tryashtar.shulker_preview:data results[-1] set value '{"translate":"tryashtar.shulker_preview.block.polished_blackstone.2","color":"#0e07fc"}'
execute if data storage tryashtar.shulker_preview:data item{id:"minecraft:polished_blackstone_wall"} run data modify storage tryashtar.shulker_preview:data results[-1] set value '{"translate":"tryashtar.shulker_preview.block.polished_blackstone.2","color":"#1207fc"}'
execute if data storage tryashtar.shulker_preview:data item{id:"minecraft:purple_glazed_terracotta"} run data modify storage tryashtar.shulker_preview:data results[-1] set value '{"translate":"tryashtar.shulker_preview.block.purple_glazed_terracotta.2","color":"#3307fc"}'
execute if data storage tryashtar.shulker_preview:data item{id:"minecraft:skeleton_horse_spawn_egg"} run data modify storage tryashtar.shulker_preview:data results[-1] set value '[{"translate":"tryashtar.shulker_preview.item.spawn_egg.2","color":"#68684f"},{"translate":"tryashtar.shulker_preview.overlay"},{"translate":"tryashtar.shulker_preview.item.spawn_egg_overlay.2","color":"#e5e5d8"}]'
execute if data storage tryashtar.shulker_preview:data item{id:"minecraft:warped_fungus_on_a_stick"} run data modify storage tryashtar.shulker_preview:data results[-1] set value '{"translate":"tryashtar.shulker_preview.item.warped_fungus_on_a_stick.2"}'
execute if data storage tryashtar.shulker_preview:data item{id:"minecraft:warped_fungus_on_a_stick"} run scoreboard players set #max shulker_preview 100
execute if data storage tryashtar.shulker_preview:data item{id:"minecraft:waxed_exposed_cut_copper"} run data modify storage tryashtar.shulker_preview:data results[-1] set value '{"translate":"tryashtar.shulker_preview.block.exposed_cut_copper.2","color":"#0107fc"}'
execute if data storage tryashtar.shulker_preview:data item{id:"minecraft:white_stained_glass_pane"} run data modify storage tryashtar.shulker_preview:data results[-1] set value '{"translate":"tryashtar.shulker_preview.item.white_stained_glass.2"}'
execute if data storage tryashtar.shulker_preview:data item{id:"minecraft:yellow_glazed_terracotta"} run data modify storage tryashtar.shulker_preview:data results[-1] set value '{"translate":"tryashtar.shulker_preview.block.yellow_glazed_terracotta.2","color":"#3307fc"}'
execute store result score #durability shulker_preview run data get storage tryashtar.shulker_preview:data item.tag.Damage
execute if data storage tryashtar.shulker_preview:data item.tag.Damage run function tryashtar.shulker_preview:row_2/overlay/durability
