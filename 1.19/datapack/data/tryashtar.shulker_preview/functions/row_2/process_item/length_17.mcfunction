execute if data storage tryashtar.shulker_preview:data item{id:"minecraft:barrier"} run summon marker ~ ~ ~ {Tags:["tryashtar.shulker_preview"],CustomName:'{"translate":"tryashtar.shulker_preview.item.barrier.2"}'}
execute if data storage tryashtar.shulker_preview:data item{id:"minecraft:chicken"} run summon marker ~ ~ ~ {Tags:["tryashtar.shulker_preview"],CustomName:'{"translate":"tryashtar.shulker_preview.item.chicken.2"}'}
execute if data storage tryashtar.shulker_preview:data item{id:"minecraft:diamond"} run summon marker ~ ~ ~ {Tags:["tryashtar.shulker_preview"],CustomName:'{"translate":"tryashtar.shulker_preview.item.diamond.2"}'}
execute if data storage tryashtar.shulker_preview:data item{id:"minecraft:emerald"} run summon marker ~ ~ ~ {Tags:["tryashtar.shulker_preview"],CustomName:'{"translate":"tryashtar.shulker_preview.item.emerald.2"}'}
execute if data storage tryashtar.shulker_preview:data item{id:"minecraft:feather"} run summon marker ~ ~ ~ {Tags:["tryashtar.shulker_preview"],CustomName:'{"translate":"tryashtar.shulker_preview.item.feather.2"}'}
execute if data storage tryashtar.shulker_preview:data item{id:"minecraft:ink_sac"} run summon marker ~ ~ ~ {Tags:["tryashtar.shulker_preview"],CustomName:'{"translate":"tryashtar.shulker_preview.item.ink_sac.2"}'}
execute if data storage tryashtar.shulker_preview:data item{id:"minecraft:lantern"} run summon marker ~ ~ ~ {Tags:["tryashtar.shulker_preview"],CustomName:'{"translate":"tryashtar.shulker_preview.item.lantern.2"}'}
execute if data storage tryashtar.shulker_preview:data item{id:"minecraft:leather"} run summon marker ~ ~ ~ {Tags:["tryashtar.shulker_preview"],CustomName:'{"translate":"tryashtar.shulker_preview.item.leather.2"}'}
execute if data storage tryashtar.shulker_preview:data item{id:"minecraft:red_dye"} run summon marker ~ ~ ~ {Tags:["tryashtar.shulker_preview"],CustomName:'{"translate":"tryashtar.shulker_preview.item.red_dye.2"}'}
execute if data storage tryashtar.shulker_preview:data item{id:"minecraft:trident"} run summon marker ~ ~ ~ {Tags:["tryashtar.shulker_preview"],CustomName:'{"translate":"tryashtar.shulker_preview.item.trident.2"}'}
execute if data storage tryashtar.shulker_preview:data item{id:"minecraft:trident"} run scoreboard players set #max shulker_preview 250
execute store result score #durability shulker_preview run data get storage tryashtar.shulker_preview:data item.tag.Damage
execute if data storage tryashtar.shulker_preview:data item.tag.Damage run function tryashtar.shulker_preview:row_2/overlay/durability
