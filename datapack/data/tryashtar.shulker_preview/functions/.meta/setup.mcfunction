# place the global shulker box, sub-global shulker box, and sign
fill 29999976 0 9831 29999980 2 9833 bedrock
setblock 29999977 1 9832 shulker_box{CustomName:'"tryashtar Global Shulker Box®"'}
setblock 29999978 1 9832 jukebox
setblock 29999979 1 9832 birch_sign{Text1:'""',Text2:'"tryashtar"',Text3:'"Evaluation Sign®"',Text4:'""'}
execute if block 29999978 1 9832 jukebox run tellraw @a {"text":"Success! Thank you and enjoy.","color":"yellow"}
execute unless block 29999978 1 9832 jukebox run tellraw @a {"text":"It failed somehow? Trying again in one second...","color":"red"}
execute unless block 29999978 1 9832 jukebox run schedule function tryashtar.shulker_preview:.meta/check_setup 1s
