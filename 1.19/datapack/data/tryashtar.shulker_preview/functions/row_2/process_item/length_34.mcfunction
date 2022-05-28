execute if data storage tryashtar.shulker_preview:data item{id:"minecraft:black_stained_glass_pane"} run summon marker ~ ~ ~ {Tags:["tryashtar.shulker_preview"],CustomName:'{"translate":"tryashtar.shulker_preview.block.black_stained_glass.2"}'}
execute if data storage tryashtar.shulker_preview:data item{id:"minecraft:brown_stained_glass_pane"} run summon marker ~ ~ ~ {Tags:["tryashtar.shulker_preview"],CustomName:'{"translate":"tryashtar.shulker_preview.block.brown_stained_glass.2"}'}
execute if data storage tryashtar.shulker_preview:data item{id:"minecraft:elder_guardian_spawn_egg"} run summon marker ~ ~ ~ {Tags:["tryashtar.shulker_preview"],CustomName:'[{"translate":"tryashtar.shulker_preview.item.spawn_egg.2","color":"#ceccba"},{"translate":"tryashtar.shulker_preview.overlay"},{"translate":"tryashtar.shulker_preview.item.spawn_egg_overlay.2","color":"#747693"}]'}
execute if data storage tryashtar.shulker_preview:data item{id:"minecraft:green_stained_glass_pane"} run summon marker ~ ~ ~ {Tags:["tryashtar.shulker_preview"],CustomName:'{"translate":"tryashtar.shulker_preview.block.green_stained_glass.2"}'}
execute if data storage tryashtar.shulker_preview:data item{id:"minecraft:skeleton_horse_spawn_egg"} run summon marker ~ ~ ~ {Tags:["tryashtar.shulker_preview"],CustomName:'[{"translate":"tryashtar.shulker_preview.item.spawn_egg.2","color":"#68684f"},{"translate":"tryashtar.shulker_preview.overlay"},{"translate":"tryashtar.shulker_preview.item.spawn_egg_overlay.2","color":"#e5e5d8"}]'}
execute if data storage tryashtar.shulker_preview:data item{id:"minecraft:warped_fungus_on_a_stick"} run summon marker ~ ~ ~ {Tags:["tryashtar.shulker_preview"],CustomName:'{"translate":"tryashtar.shulker_preview.item.warped_fungus_on_a_stick.2"}'}
execute if data storage tryashtar.shulker_preview:data item{id:"minecraft:warped_fungus_on_a_stick"} run scoreboard players set #max shulker_preview 100
execute if data storage tryashtar.shulker_preview:data item{id:"minecraft:white_stained_glass_pane"} run summon marker ~ ~ ~ {Tags:["tryashtar.shulker_preview"],CustomName:'{"translate":"tryashtar.shulker_preview.block.white_stained_glass.2"}'}
execute store result score #durability shulker_preview run data get storage tryashtar.shulker_preview:data item.tag.Damage
execute if data storage tryashtar.shulker_preview:data item.tag.Damage run function tryashtar.shulker_preview:row_2/overlay/durability
