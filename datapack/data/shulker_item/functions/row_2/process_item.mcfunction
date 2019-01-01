# get the length of this item and call the appropriate function
execute store result score #length shulker_item run data get block ~2 1 ~ RecordItem.id
execute if score #length shulker_item matches 13 run function shulker_item:row_2/process_item/length_13
execute if score #length shulker_item matches 14 run function shulker_item:row_2/process_item/length_14
execute if score #length shulker_item matches 15 run function shulker_item:row_2/process_item/length_15
execute if score #length shulker_item matches 16 run function shulker_item:row_2/process_item/length_16
execute if score #length shulker_item matches 17 run function shulker_item:row_2/process_item/length_17
execute if score #length shulker_item matches 18 run function shulker_item:row_2/process_item/length_18
execute if score #length shulker_item matches 19 run function shulker_item:row_2/process_item/length_19
execute if score #length shulker_item matches 20 run function shulker_item:row_2/process_item/length_20
execute if score #length shulker_item matches 21 run function shulker_item:row_2/process_item/length_21
execute if score #length shulker_item matches 22 run function shulker_item:row_2/process_item/length_22
execute if score #length shulker_item matches 23 run function shulker_item:row_2/process_item/length_23
execute if score #length shulker_item matches 24 run function shulker_item:row_2/process_item/length_24
execute if score #length shulker_item matches 25 run function shulker_item:row_2/process_item/length_25
execute if score #length shulker_item matches 26 run function shulker_item:row_2/process_item/length_26
execute if score #length shulker_item matches 27 run function shulker_item:row_2/process_item/length_27
execute if score #length shulker_item matches 28 run function shulker_item:row_2/process_item/length_28
execute if score #length shulker_item matches 29 run function shulker_item:row_2/process_item/length_29
execute if score #length shulker_item matches 30 run function shulker_item:row_2/process_item/length_30
execute if score #length shulker_item matches 31 run function shulker_item:row_2/process_item/length_31
execute if score #length shulker_item matches 32 run function shulker_item:row_2/process_item/length_32
execute if score #length shulker_item matches 33 run function shulker_item:row_2/process_item/length_33
execute if score #length shulker_item matches 34 run function shulker_item:row_2/process_item/length_34
execute if score #length shulker_item matches 35 run function shulker_item:row_2/process_item/length_35
execute if score #length shulker_item matches 36 run function shulker_item:row_2/process_item/length_36
execute if score #length shulker_item matches 37 run function shulker_item:row_2/process_item/length_37
execute if score #length shulker_item matches 38 run function shulker_item:row_2/process_item/length_38
execute if score #length shulker_item matches 39 run function shulker_item:row_2/process_item/length_39
execute if score #length shulker_item matches 40 run function shulker_item:row_2/process_item/length_40

# summon in count entity
execute store result score #count shulker_item run data get block ~2 1 ~ RecordItem.Count
execute if score #count shulker_item matches 2.. run function shulker_item:row_2/process_count
