# get the length of this item and call the appropriate function
execute store result score #length shulker_preview run data get storage tryashtar.shulker_preview:data item.id
execute if score #length shulker_preview matches 13 run function tryashtar.shulker_preview:row_2/process_item/length_13
execute if score #length shulker_preview matches 14 run function tryashtar.shulker_preview:row_2/process_item/length_14
execute if score #length shulker_preview matches 15 run function tryashtar.shulker_preview:row_2/process_item/length_15
execute if score #length shulker_preview matches 16 run function tryashtar.shulker_preview:row_2/process_item/length_16
execute if score #length shulker_preview matches 17 run function tryashtar.shulker_preview:row_2/process_item/length_17
execute if score #length shulker_preview matches 18 run function tryashtar.shulker_preview:row_2/process_item/length_18
execute if score #length shulker_preview matches 19 run function tryashtar.shulker_preview:row_2/process_item/length_19
execute if score #length shulker_preview matches 20 run function tryashtar.shulker_preview:row_2/process_item/length_20
execute if score #length shulker_preview matches 21 run function tryashtar.shulker_preview:row_2/process_item/length_21
execute if score #length shulker_preview matches 22 run function tryashtar.shulker_preview:row_2/process_item/length_22
execute if score #length shulker_preview matches 23 run function tryashtar.shulker_preview:row_2/process_item/length_23
execute if score #length shulker_preview matches 24 run function tryashtar.shulker_preview:row_2/process_item/length_24
execute if score #length shulker_preview matches 25 run function tryashtar.shulker_preview:row_2/process_item/length_25
execute if score #length shulker_preview matches 26 run function tryashtar.shulker_preview:row_2/process_item/length_26
execute if score #length shulker_preview matches 27 run function tryashtar.shulker_preview:row_2/process_item/length_27
execute if score #length shulker_preview matches 28 run function tryashtar.shulker_preview:row_2/process_item/length_28
execute if score #length shulker_preview matches 29 run function tryashtar.shulker_preview:row_2/process_item/length_29
execute if score #length shulker_preview matches 30 run function tryashtar.shulker_preview:row_2/process_item/length_30
execute if score #length shulker_preview matches 31 run function tryashtar.shulker_preview:row_2/process_item/length_31
execute if score #length shulker_preview matches 32 run function tryashtar.shulker_preview:row_2/process_item/length_32
execute if score #length shulker_preview matches 33 run function tryashtar.shulker_preview:row_2/process_item/length_33
execute if score #length shulker_preview matches 34 run function tryashtar.shulker_preview:row_2/process_item/length_34
execute if score #length shulker_preview matches 35 run function tryashtar.shulker_preview:row_2/process_item/length_35
execute if score #length shulker_preview matches 36 run function tryashtar.shulker_preview:row_2/process_item/length_36
execute if score #length shulker_preview matches 37 run function tryashtar.shulker_preview:row_2/process_item/length_37
execute if score #length shulker_preview matches 38 run function tryashtar.shulker_preview:row_2/process_item/length_38
execute if score #length shulker_preview matches 39 run function tryashtar.shulker_preview:row_2/process_item/length_39
execute if score #length shulker_preview matches 40 run function tryashtar.shulker_preview:row_2/process_item/length_40
execute if score #length shulker_preview matches 41 run function tryashtar.shulker_preview:row_2/process_item/length_41
execute if score #length shulker_preview matches 42 run function tryashtar.shulker_preview:row_2/process_item/length_42
execute if score #length shulker_preview matches 43 run function tryashtar.shulker_preview:row_2/process_item/length_43
execute if score #length shulker_preview matches 44 run function tryashtar.shulker_preview:row_2/process_item/length_44
execute if score #length shulker_preview matches 45 run function tryashtar.shulker_preview:row_2/process_item/length_45
execute if score #length shulker_preview matches 46 run function tryashtar.shulker_preview:row_2/process_item/length_46
execute if score #length shulker_preview matches 48 run function tryashtar.shulker_preview:row_2/process_item/length_48
execute if score #length shulker_preview matches 49 run function tryashtar.shulker_preview:row_2/process_item/length_49
execute if score #length shulker_preview matches 51 run function tryashtar.shulker_preview:row_2/process_item/length_51

# placeholder if item was not found
execute unless entity @e[type=area_effect_cloud,tag=tryashtar.shulker_preview,distance=..0.0001] run summon area_effect_cloud ~ ~ ~ {Tags:["tryashtar.shulker_preview"],CustomName:'{"translate":"tryashtar.shulker_preview.item.missingno.2"}'}

# summon in count entity
execute store result score #count shulker_preview run data get storage tryashtar.shulker_preview:data item.Count
execute if score #count shulker_preview matches 2.. run function tryashtar.shulker_preview:row_2/overlay/count
