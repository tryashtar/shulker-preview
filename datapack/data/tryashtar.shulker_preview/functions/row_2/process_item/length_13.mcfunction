execute if block ~2 1 ~ jukebox{RecordItem:{id:"minecraft:bow"}} run summon area_effect_cloud ~ ~ ~ {Tags:["tryashtar.shulker_preview"],CustomName:'{"translate":"tryashtar.shulker_preview.item.bow.2"}'}
execute if block ~2 1 ~ jukebox{RecordItem:{id:"minecraft:bow"}} run scoreboard players set #max shulker_preview 384
execute if block ~2 1 ~ jukebox{RecordItem:{id:"minecraft:cod"}} run summon area_effect_cloud ~ ~ ~ {Tags:["tryashtar.shulker_preview"],CustomName:'{"translate":"tryashtar.shulker_preview.item.cod.2"}'}
execute if block ~2 1 ~ jukebox{RecordItem:{id:"minecraft:egg"}} run summon area_effect_cloud ~ ~ ~ {Tags:["tryashtar.shulker_preview"],CustomName:'{"translate":"tryashtar.shulker_preview.item.egg.2"}'}
execute if block ~2 1 ~ jukebox{RecordItem:{id:"minecraft:ice"}} run summon area_effect_cloud ~ ~ ~ {Tags:["tryashtar.shulker_preview"],CustomName:'{"translate":"tryashtar.shulker_preview.block.ice.2"}'}
execute if block ~2 1 ~ jukebox{RecordItem:{id:"minecraft:map"}} run summon area_effect_cloud ~ ~ ~ {Tags:["tryashtar.shulker_preview"],CustomName:'{"translate":"tryashtar.shulker_preview.item.map.2"}'}
execute if block ~2 1 ~ jukebox{RecordItem:{id:"minecraft:tnt"}} run summon area_effect_cloud ~ ~ ~ {Tags:["tryashtar.shulker_preview"],CustomName:'{"translate":"tryashtar.shulker_preview.block.tnt.2"}'}
execute store result score #durability shulker_preview run data get block ~2 1 ~ RecordItem.tag.Damage
execute if data block ~2 1 ~ RecordItem.tag.Damage run function tryashtar.shulker_preview:row_2/process_durability
