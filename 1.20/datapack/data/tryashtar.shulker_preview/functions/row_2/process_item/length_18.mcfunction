execute if data storage tryashtar.shulker_preview:data item{id:"minecraft:andesite"} run summon marker ~ ~ ~ {Tags:["tryashtar.shulker_preview"],CustomName:'{"translate":"tryashtar.shulker_preview.block.andesite.2"}'}
execute if data storage tryashtar.shulker_preview:data item{id:"minecraft:bee_nest"} run summon marker ~ ~ ~ {Tags:["tryashtar.shulker_preview"],CustomName:'{"translate":"tryashtar.shulker_preview.block.bee_nest.2"}'}
execute if data storage tryashtar.shulker_preview:data item{id:"minecraft:beetroot"} run summon marker ~ ~ ~ {Tags:["tryashtar.shulker_preview"],CustomName:'{"translate":"tryashtar.shulker_preview.item.beetroot.2"}'}
execute if data storage tryashtar.shulker_preview:data item{id:"minecraft:blue_bed"} run summon marker ~ ~ ~ {Tags:["tryashtar.shulker_preview"],CustomName:'{"translate":"tryashtar.shulker_preview.block.blue_bed.2"}'}
execute if data storage tryashtar.shulker_preview:data item{id:"minecraft:blue_dye"} run summon marker ~ ~ ~ {Tags:["tryashtar.shulker_preview"],CustomName:'{"translate":"tryashtar.shulker_preview.item.blue_dye.2"}'}
execute if data storage tryashtar.shulker_preview:data item{id:"minecraft:blue_ice"} run summon marker ~ ~ ~ {Tags:["tryashtar.shulker_preview"],CustomName:'{"translate":"tryashtar.shulker_preview.block.blue_ice.2"}'}
execute if data storage tryashtar.shulker_preview:data item{id:"minecraft:campfire"} run summon marker ~ ~ ~ {Tags:["tryashtar.shulker_preview"],CustomName:'{"translate":"tryashtar.shulker_preview.item.campfire.2"}'}
execute if data storage tryashtar.shulker_preview:data item{id:"minecraft:cauldron"} run summon marker ~ ~ ~ {Tags:["tryashtar.shulker_preview"],CustomName:'{"translate":"tryashtar.shulker_preview.item.cauldron.2"}'}
execute if data storage tryashtar.shulker_preview:data item{id:"minecraft:charcoal"} run summon marker ~ ~ ~ {Tags:["tryashtar.shulker_preview"],CustomName:'{"translate":"tryashtar.shulker_preview.item.charcoal.2"}'}
execute if data storage tryashtar.shulker_preview:data item{id:"minecraft:coal_ore"} run summon marker ~ ~ ~ {Tags:["tryashtar.shulker_preview"],CustomName:'{"translate":"tryashtar.shulker_preview.block.coal_ore.2"}'}
execute if data storage tryashtar.shulker_preview:data item{id:"minecraft:crossbow",tag:{ChargedProjectiles:[{id:"minecraft:firework_rocket"}]}} run summon marker ~ ~ ~ {Tags:["tryashtar.shulker_preview"],CustomName:'{"translate":"tryashtar.shulker_preview.item.crossbow_firework.2"}'}
execute if data storage tryashtar.shulker_preview:data item{id:"minecraft:crossbow",tag:{ChargedProjectiles:[{}]}} unless data storage tryashtar.shulker_preview:data item.tag.ChargedProjectiles[{id:"minecraft:firework_rocket"}] run summon marker ~ ~ ~ {Tags:["tryashtar.shulker_preview"],CustomName:'{"translate":"tryashtar.shulker_preview.item.crossbow_arrow.2"}'}
execute if data storage tryashtar.shulker_preview:data item{id:"minecraft:crossbow"} unless data storage tryashtar.shulker_preview:data item.tag.ChargedProjectiles[{}] run summon marker ~ ~ ~ {Tags:["tryashtar.shulker_preview"],CustomName:'{"translate":"tryashtar.shulker_preview.item.crossbow.2"}'}
execute if data storage tryashtar.shulker_preview:data item{id:"minecraft:crossbow"} run scoreboard players set #max shulker_preview 465
execute if data storage tryashtar.shulker_preview:data item{id:"minecraft:cyan_bed"} run summon marker ~ ~ ~ {Tags:["tryashtar.shulker_preview"],CustomName:'{"translate":"tryashtar.shulker_preview.block.cyan_bed.2"}'}
execute if data storage tryashtar.shulker_preview:data item{id:"minecraft:cyan_dye"} run summon marker ~ ~ ~ {Tags:["tryashtar.shulker_preview"],CustomName:'{"translate":"tryashtar.shulker_preview.item.cyan_dye.2"}'}
execute if data storage tryashtar.shulker_preview:data item{id:"minecraft:farmland"} run summon marker ~ ~ ~ {Tags:["tryashtar.shulker_preview"],CustomName:'{"translate":"tryashtar.shulker_preview.block.farmland.2"}'}
execute if data storage tryashtar.shulker_preview:data item{id:"minecraft:gold_ore"} run summon marker ~ ~ ~ {Tags:["tryashtar.shulker_preview"],CustomName:'{"translate":"tryashtar.shulker_preview.block.gold_ore.2"}'}
execute if data storage tryashtar.shulker_preview:data item{id:"minecraft:gray_bed"} run summon marker ~ ~ ~ {Tags:["tryashtar.shulker_preview"],CustomName:'{"translate":"tryashtar.shulker_preview.block.gray_bed.2"}'}
execute if data storage tryashtar.shulker_preview:data item{id:"minecraft:gray_dye"} run summon marker ~ ~ ~ {Tags:["tryashtar.shulker_preview"],CustomName:'{"translate":"tryashtar.shulker_preview.item.gray_dye.2"}'}
execute if data storage tryashtar.shulker_preview:data item{id:"minecraft:iron_axe"} run summon marker ~ ~ ~ {Tags:["tryashtar.shulker_preview"],CustomName:'{"translate":"tryashtar.shulker_preview.item.iron_axe.2"}'}
execute if data storage tryashtar.shulker_preview:data item{id:"minecraft:iron_axe"} run scoreboard players set #max shulker_preview 250
execute if data storage tryashtar.shulker_preview:data item{id:"minecraft:iron_hoe"} run summon marker ~ ~ ~ {Tags:["tryashtar.shulker_preview"],CustomName:'{"translate":"tryashtar.shulker_preview.item.iron_hoe.2"}'}
execute if data storage tryashtar.shulker_preview:data item{id:"minecraft:iron_hoe"} run scoreboard players set #max shulker_preview 250
execute if data storage tryashtar.shulker_preview:data item{id:"minecraft:iron_ore"} run summon marker ~ ~ ~ {Tags:["tryashtar.shulker_preview"],CustomName:'{"translate":"tryashtar.shulker_preview.block.iron_ore.2"}'}
execute if data storage tryashtar.shulker_preview:data item{id:"minecraft:lily_pad"} run summon marker ~ ~ ~ {Tags:["tryashtar.shulker_preview"],CustomName:'{"translate":"tryashtar.shulker_preview.item.lily_pad.2","color":"#71c35c"}'}
execute if data storage tryashtar.shulker_preview:data item{id:"minecraft:lime_bed"} run summon marker ~ ~ ~ {Tags:["tryashtar.shulker_preview"],CustomName:'{"translate":"tryashtar.shulker_preview.block.lime_bed.2"}'}
execute if data storage tryashtar.shulker_preview:data item{id:"minecraft:lime_dye"} run summon marker ~ ~ ~ {Tags:["tryashtar.shulker_preview"],CustomName:'{"translate":"tryashtar.shulker_preview.item.lime_dye.2"}'}
execute if data storage tryashtar.shulker_preview:data item{id:"minecraft:minecart"} run summon marker ~ ~ ~ {Tags:["tryashtar.shulker_preview"],CustomName:'{"translate":"tryashtar.shulker_preview.item.minecart.2"}'}
execute if data storage tryashtar.shulker_preview:data item{id:"minecraft:mycelium"} run summon marker ~ ~ ~ {Tags:["tryashtar.shulker_preview"],CustomName:'{"translate":"tryashtar.shulker_preview.block.mycelium.2"}'}
execute if data storage tryashtar.shulker_preview:data item{id:"minecraft:name_tag"} run summon marker ~ ~ ~ {Tags:["tryashtar.shulker_preview"],CustomName:'{"translate":"tryashtar.shulker_preview.item.name_tag.2"}'}
execute if data storage tryashtar.shulker_preview:data item{id:"minecraft:oak_boat"} run summon marker ~ ~ ~ {Tags:["tryashtar.shulker_preview"],CustomName:'{"translate":"tryashtar.shulker_preview.item.oak_boat.2"}'}
execute if data storage tryashtar.shulker_preview:data item{id:"minecraft:oak_door"} run summon marker ~ ~ ~ {Tags:["tryashtar.shulker_preview"],CustomName:'{"translate":"tryashtar.shulker_preview.item.oak_door.2"}'}
execute if data storage tryashtar.shulker_preview:data item{id:"minecraft:oak_sign"} run summon marker ~ ~ ~ {Tags:["tryashtar.shulker_preview"],CustomName:'{"translate":"tryashtar.shulker_preview.item.oak_sign.2"}'}
execute if data storage tryashtar.shulker_preview:data item{id:"minecraft:oak_slab"} run summon marker ~ ~ ~ {Tags:["tryashtar.shulker_preview"],CustomName:'{"translate":"tryashtar.shulker_preview.block.oak_slab.2"}'}
execute if data storage tryashtar.shulker_preview:data item{id:"minecraft:oak_wood"} run summon marker ~ ~ ~ {Tags:["tryashtar.shulker_preview"],CustomName:'{"translate":"tryashtar.shulker_preview.block.oak_wood.2"}'}
execute if data storage tryashtar.shulker_preview:data item{id:"minecraft:observer"} run summon marker ~ ~ ~ {Tags:["tryashtar.shulker_preview"],CustomName:'{"translate":"tryashtar.shulker_preview.block.observer.2"}'}
execute if data storage tryashtar.shulker_preview:data item{id:"minecraft:obsidian"} run summon marker ~ ~ ~ {Tags:["tryashtar.shulker_preview"],CustomName:'{"translate":"tryashtar.shulker_preview.block.obsidian.2"}'}
execute if data storage tryashtar.shulker_preview:data item{id:"minecraft:painting"} run summon marker ~ ~ ~ {Tags:["tryashtar.shulker_preview"],CustomName:'{"translate":"tryashtar.shulker_preview.item.painting.2"}'}
execute if data storage tryashtar.shulker_preview:data item{id:"minecraft:pink_bed"} run summon marker ~ ~ ~ {Tags:["tryashtar.shulker_preview"],CustomName:'{"translate":"tryashtar.shulker_preview.block.pink_bed.2"}'}
execute if data storage tryashtar.shulker_preview:data item{id:"minecraft:pink_dye"} run summon marker ~ ~ ~ {Tags:["tryashtar.shulker_preview"],CustomName:'{"translate":"tryashtar.shulker_preview.item.pink_dye.2"}'}
execute if data storage tryashtar.shulker_preview:data item{id:"minecraft:porkchop"} run summon marker ~ ~ ~ {Tags:["tryashtar.shulker_preview"],CustomName:'{"translate":"tryashtar.shulker_preview.item.porkchop.2"}'}
execute if data storage tryashtar.shulker_preview:data item{id:"minecraft:raw_gold"} run summon marker ~ ~ ~ {Tags:["tryashtar.shulker_preview"],CustomName:'{"translate":"tryashtar.shulker_preview.item.raw_gold.2"}'}
execute if data storage tryashtar.shulker_preview:data item{id:"minecraft:raw_iron"} run summon marker ~ ~ ~ {Tags:["tryashtar.shulker_preview"],CustomName:'{"translate":"tryashtar.shulker_preview.item.raw_iron.2"}'}
execute if data storage tryashtar.shulker_preview:data item{id:"minecraft:red_sand"} run summon marker ~ ~ ~ {Tags:["tryashtar.shulker_preview"],CustomName:'{"translate":"tryashtar.shulker_preview.block.red_sand.2"}'}
execute if data storage tryashtar.shulker_preview:data item{id:"minecraft:red_wool"} run summon marker ~ ~ ~ {Tags:["tryashtar.shulker_preview"],CustomName:'{"translate":"tryashtar.shulker_preview.block.red_wool.2"}'}
execute if data storage tryashtar.shulker_preview:data item{id:"minecraft:redstone"} run summon marker ~ ~ ~ {Tags:["tryashtar.shulker_preview"],CustomName:'{"translate":"tryashtar.shulker_preview.item.redstone.2"}'}
execute if data storage tryashtar.shulker_preview:data item{id:"minecraft:repeater"} run summon marker ~ ~ ~ {Tags:["tryashtar.shulker_preview"],CustomName:'{"translate":"tryashtar.shulker_preview.item.repeater.2"}'}
execute if data storage tryashtar.shulker_preview:data item{id:"minecraft:seagrass"} run summon marker ~ ~ ~ {Tags:["tryashtar.shulker_preview"],CustomName:'{"translate":"tryashtar.shulker_preview.item.seagrass.2"}'}
execute if data storage tryashtar.shulker_preview:data item{id:"minecraft:snowball"} run summon marker ~ ~ ~ {Tags:["tryashtar.shulker_preview"],CustomName:'{"translate":"tryashtar.shulker_preview.item.snowball.2"}'}
execute if data storage tryashtar.shulker_preview:data item{id:"minecraft:spyglass"} run summon marker ~ ~ ~ {Tags:["tryashtar.shulker_preview"],CustomName:'{"translate":"tryashtar.shulker_preview.item.spyglass.2"}'}
execute store result score #durability shulker_preview run data get storage tryashtar.shulker_preview:data item.tag.Damage
execute if data storage tryashtar.shulker_preview:data item.tag.Damage run function tryashtar.shulker_preview:row_2/overlay/durability
