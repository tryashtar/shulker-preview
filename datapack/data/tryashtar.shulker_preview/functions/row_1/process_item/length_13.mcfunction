execute if block 29999978 1 9832 jukebox{RecordItem:{id:"minecraft:bow"}} run summon area_effect_cloud ~ ~ ~ {Tags:["tryashtar.shulker_preview"],CustomName:'{"translate":"tryashtar.shulker_preview.item.bow.1"}'}
execute if block 29999978 1 9832 jukebox{RecordItem:{id:"minecraft:bow"}} run scoreboard players set #max shulker_preview 384
execute if block 29999978 1 9832 jukebox{RecordItem:{id:"minecraft:cod"}} run summon area_effect_cloud ~ ~ ~ {Tags:["tryashtar.shulker_preview"],CustomName:'{"translate":"tryashtar.shulker_preview.item.cod.1"}'}
execute if block 29999978 1 9832 jukebox{RecordItem:{id:"minecraft:egg"}} run summon area_effect_cloud ~ ~ ~ {Tags:["tryashtar.shulker_preview"],CustomName:'{"translate":"tryashtar.shulker_preview.item.egg.1"}'}
execute if block 29999978 1 9832 jukebox{RecordItem:{id:"minecraft:ice"}} run summon area_effect_cloud ~ ~ ~ {Tags:["tryashtar.shulker_preview"],CustomName:'{"translate":"tryashtar.shulker_preview.block.ice.1"}'}
execute if block 29999978 1 9832 jukebox{RecordItem:{id:"minecraft:map"}} run summon area_effect_cloud ~ ~ ~ {Tags:["tryashtar.shulker_preview"],CustomName:'{"translate":"tryashtar.shulker_preview.item.map.1"}'}
execute if block 29999978 1 9832 jukebox{RecordItem:{id:"minecraft:tnt"}} run summon area_effect_cloud ~ ~ ~ {Tags:["tryashtar.shulker_preview"],CustomName:'{"translate":"tryashtar.shulker_preview.block.tnt.1"}'}
execute store result score #durability shulker_preview run data get block 29999978 1 9832 RecordItem.tag.Damage
execute if data block 29999978 1 9832 RecordItem.tag.Damage run function tryashtar.shulker_preview:row_1/process_durability
