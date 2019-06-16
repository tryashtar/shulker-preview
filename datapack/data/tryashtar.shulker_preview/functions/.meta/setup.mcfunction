# place the global shulker box, jukebox, and sign
execute as @a run trigger shulker_trigger set 0
summon area_effect_cloud ~ 1 ~ {UUIDMost:29999977L,UUIDLeast:9832L,CustomName:'"Shulker Marker"',Age:-2147483648,Duration:-1,WaitTime:-2147483648}
fill ~-1 0 ~-1 ~3 2 ~1 bedrock
setblock ~ 1 ~ shulker_box{CustomName:'"tryashtar Global Shulker Box®"'}
setblock ~1 1 ~ jukebox
setblock ~2 1 ~ birch_sign{Text1:'""',Text2:'"tryashtar"',Text3:'"Evaluation Sign®"',Text4:'""'}
execute if block ~1 1 ~ jukebox run scoreboard players reset #ender_enabled shulker_preview
execute if block ~1 1 ~ jukebox run tellraw @a [{"text":"\n\n\nSuccess! Thank you and enjoy.","color":"yellow"},{"text":"\n\uE24C\n     ","color":"white"},{"text":"If you want, you can click this text\nto enable previews for ender chest items too.","color":"green","clickEvent":{"action":"run_command","value":"/function tryashtar.shulker_preview:.meta/enable_ender"}},{"text":"\nIt's a bit experimental and will prevent ender chest\nitems from stacking in most cases.","color":"gray"}]
execute unless block ~1 1 ~ jukebox run tellraw @a {"text":"It failed somehow? Trying again in one second...","color":"red"}
execute unless block ~1 1 ~ jukebox run schedule function tryashtar.shulker_preview:.meta/check_setup 1s
