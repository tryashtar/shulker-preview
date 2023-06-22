execute if data storage tryashtar.shulker_preview:data item{id:"minecraft:bow"} run summon marker ~ ~ ~ {Tags:["tryashtar.shulker_preview"],CustomName:'{"translate":"tryashtar.shulker_preview.item.bow.1"}'}
execute if data storage tryashtar.shulker_preview:data item{id:"minecraft:bow"} run scoreboard players set #max shulker_preview 384
execute if data storage tryashtar.shulker_preview:data item{id:"minecraft:cod"} run summon marker ~ ~ ~ {Tags:["tryashtar.shulker_preview"],CustomName:'{"translate":"tryashtar.shulker_preview.item.cod.1"}'}
execute if data storage tryashtar.shulker_preview:data item{id:"minecraft:egg"} run summon marker ~ ~ ~ {Tags:["tryashtar.shulker_preview"],CustomName:'{"translate":"tryashtar.shulker_preview.item.egg.1"}'}
execute if data storage tryashtar.shulker_preview:data item{id:"minecraft:ice"} run summon marker ~ ~ ~ {Tags:["tryashtar.shulker_preview"],CustomName:'{"translate":"tryashtar.shulker_preview.block.ice.1"}'}
execute if data storage tryashtar.shulker_preview:data item{id:"minecraft:map"} run summon marker ~ ~ ~ {Tags:["tryashtar.shulker_preview"],CustomName:'{"translate":"tryashtar.shulker_preview.item.map.1"}'}
execute if data storage tryashtar.shulker_preview:data item{id:"minecraft:mud"} run summon marker ~ ~ ~ {Tags:["tryashtar.shulker_preview"],CustomName:'{"translate":"tryashtar.shulker_preview.block.mud.1"}'}
execute if data storage tryashtar.shulker_preview:data item{id:"minecraft:tnt"} run summon marker ~ ~ ~ {Tags:["tryashtar.shulker_preview"],CustomName:'{"translate":"tryashtar.shulker_preview.block.tnt.1"}'}
execute store result score #durability shulker_preview run data get storage tryashtar.shulker_preview:data item.tag.Damage
execute if data storage tryashtar.shulker_preview:data item.tag.Damage run function tryashtar.shulker_preview:row_1/overlay/durability
