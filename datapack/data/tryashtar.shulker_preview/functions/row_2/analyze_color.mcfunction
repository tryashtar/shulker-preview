# pick the closest of the 16 dye colors
scoreboard players operation #red shulker_preview = #color shulker_preview
scoreboard players operation #red shulker_preview /= #256 shulker_preview
scoreboard players operation #red shulker_preview /= #256 shulker_preview
scoreboard players operation #red shulker_preview %= #256 shulker_preview
scoreboard players operation #green shulker_preview = #color shulker_preview
scoreboard players operation #green shulker_preview /= #256 shulker_preview
scoreboard players operation #green shulker_preview %= #256 shulker_preview
scoreboard players operation #blue shulker_preview = #color shulker_preview
scoreboard players operation #blue shulker_preview %= #256 shulker_preview
scoreboard players set #nearest shulker_preview 2147483647

# white
scoreboard players operation #mean shulker_preview = #red shulker_preview
scoreboard players add #mean shulker_preview 249
scoreboard players operation #mean shulker_preview /= #2 shulker_preview
scoreboard players set #mean2 shulker_preview 767
scoreboard players operation #mean2 shulker_preview -= #mean shulker_preview
scoreboard players operation #red_diff shulker_preview = #red shulker_preview
scoreboard players remove #red_diff shulker_preview 249
scoreboard players operation #red_diff shulker_preview *= #red_diff shulker_preview
scoreboard players operation #green_diff shulker_preview = #green shulker_preview
scoreboard players remove #green_diff shulker_preview 255
scoreboard players operation #green_diff shulker_preview *= #green_diff shulker_preview
scoreboard players operation #blue_diff shulker_preview = #blue shulker_preview
scoreboard players remove #blue_diff shulker_preview 254
scoreboard players operation #blue_diff shulker_preview *= #blue_diff shulker_preview
scoreboard players add #mean shulker_preview 512
scoreboard players operation #red_diff shulker_preview *= #mean shulker_preview
scoreboard players operation #red_diff shulker_preview /= #256 shulker_preview
scoreboard players operation #green_diff shulker_preview *= #4 shulker_preview
scoreboard players operation #blue_diff shulker_preview *= #mean2 shulker_preview
scoreboard players operation #blue_diff shulker_preview /= #256 shulker_preview
scoreboard players operation #diff0 shulker_preview = #red_diff shulker_preview
scoreboard players operation #diff0 shulker_preview += #green_diff shulker_preview
scoreboard players operation #diff0 shulker_preview += #blue_diff shulker_preview
scoreboard players operation #nearest shulker_preview < #diff0 shulker_preview

# orange
scoreboard players operation #mean shulker_preview = #red shulker_preview
scoreboard players add #mean shulker_preview 249
scoreboard players operation #mean shulker_preview /= #2 shulker_preview
scoreboard players set #mean2 shulker_preview 767
scoreboard players operation #mean2 shulker_preview -= #mean shulker_preview
scoreboard players operation #red_diff shulker_preview = #red shulker_preview
scoreboard players remove #red_diff shulker_preview 249
scoreboard players operation #red_diff shulker_preview *= #red_diff shulker_preview
scoreboard players operation #green_diff shulker_preview = #green shulker_preview
scoreboard players remove #green_diff shulker_preview 128
scoreboard players operation #green_diff shulker_preview *= #green_diff shulker_preview
scoreboard players operation #blue_diff shulker_preview = #blue shulker_preview
scoreboard players remove #blue_diff shulker_preview 29
scoreboard players operation #blue_diff shulker_preview *= #blue_diff shulker_preview
scoreboard players add #mean shulker_preview 512
scoreboard players operation #red_diff shulker_preview *= #mean shulker_preview
scoreboard players operation #red_diff shulker_preview /= #256 shulker_preview
scoreboard players operation #green_diff shulker_preview *= #4 shulker_preview
scoreboard players operation #blue_diff shulker_preview *= #mean2 shulker_preview
scoreboard players operation #blue_diff shulker_preview /= #256 shulker_preview
scoreboard players operation #diff1 shulker_preview = #red_diff shulker_preview
scoreboard players operation #diff1 shulker_preview += #green_diff shulker_preview
scoreboard players operation #diff1 shulker_preview += #blue_diff shulker_preview
scoreboard players operation #nearest shulker_preview < #diff1 shulker_preview

# magenta
scoreboard players operation #mean shulker_preview = #red shulker_preview
scoreboard players add #mean shulker_preview 199
scoreboard players operation #mean shulker_preview /= #2 shulker_preview
scoreboard players set #mean2 shulker_preview 767
scoreboard players operation #mean2 shulker_preview -= #mean shulker_preview
scoreboard players operation #red_diff shulker_preview = #red shulker_preview
scoreboard players remove #red_diff shulker_preview 199
scoreboard players operation #red_diff shulker_preview *= #red_diff shulker_preview
scoreboard players operation #green_diff shulker_preview = #green shulker_preview
scoreboard players remove #green_diff shulker_preview 78
scoreboard players operation #green_diff shulker_preview *= #green_diff shulker_preview
scoreboard players operation #blue_diff shulker_preview = #blue shulker_preview
scoreboard players remove #blue_diff shulker_preview 189
scoreboard players operation #blue_diff shulker_preview *= #blue_diff shulker_preview
scoreboard players add #mean shulker_preview 512
scoreboard players operation #red_diff shulker_preview *= #mean shulker_preview
scoreboard players operation #red_diff shulker_preview /= #256 shulker_preview
scoreboard players operation #green_diff shulker_preview *= #4 shulker_preview
scoreboard players operation #blue_diff shulker_preview *= #mean2 shulker_preview
scoreboard players operation #blue_diff shulker_preview /= #256 shulker_preview
scoreboard players operation #diff2 shulker_preview = #red_diff shulker_preview
scoreboard players operation #diff2 shulker_preview += #green_diff shulker_preview
scoreboard players operation #diff2 shulker_preview += #blue_diff shulker_preview
scoreboard players operation #nearest shulker_preview < #diff2 shulker_preview

# light_blue
scoreboard players operation #mean shulker_preview = #red shulker_preview
scoreboard players add #mean shulker_preview 58
scoreboard players operation #mean shulker_preview /= #2 shulker_preview
scoreboard players set #mean2 shulker_preview 767
scoreboard players operation #mean2 shulker_preview -= #mean shulker_preview
scoreboard players operation #red_diff shulker_preview = #red shulker_preview
scoreboard players remove #red_diff shulker_preview 58
scoreboard players operation #red_diff shulker_preview *= #red_diff shulker_preview
scoreboard players operation #green_diff shulker_preview = #green shulker_preview
scoreboard players remove #green_diff shulker_preview 179
scoreboard players operation #green_diff shulker_preview *= #green_diff shulker_preview
scoreboard players operation #blue_diff shulker_preview = #blue shulker_preview
scoreboard players remove #blue_diff shulker_preview 218
scoreboard players operation #blue_diff shulker_preview *= #blue_diff shulker_preview
scoreboard players add #mean shulker_preview 512
scoreboard players operation #red_diff shulker_preview *= #mean shulker_preview
scoreboard players operation #red_diff shulker_preview /= #256 shulker_preview
scoreboard players operation #green_diff shulker_preview *= #4 shulker_preview
scoreboard players operation #blue_diff shulker_preview *= #mean2 shulker_preview
scoreboard players operation #blue_diff shulker_preview /= #256 shulker_preview
scoreboard players operation #diff3 shulker_preview = #red_diff shulker_preview
scoreboard players operation #diff3 shulker_preview += #green_diff shulker_preview
scoreboard players operation #diff3 shulker_preview += #blue_diff shulker_preview
scoreboard players operation #nearest shulker_preview < #diff3 shulker_preview

# yellow
scoreboard players operation #mean shulker_preview = #red shulker_preview
scoreboard players add #mean shulker_preview 254
scoreboard players operation #mean shulker_preview /= #2 shulker_preview
scoreboard players set #mean2 shulker_preview 767
scoreboard players operation #mean2 shulker_preview -= #mean shulker_preview
scoreboard players operation #red_diff shulker_preview = #red shulker_preview
scoreboard players remove #red_diff shulker_preview 254
scoreboard players operation #red_diff shulker_preview *= #red_diff shulker_preview
scoreboard players operation #green_diff shulker_preview = #green shulker_preview
scoreboard players remove #green_diff shulker_preview 216
scoreboard players operation #green_diff shulker_preview *= #green_diff shulker_preview
scoreboard players operation #blue_diff shulker_preview = #blue shulker_preview
scoreboard players remove #blue_diff shulker_preview 61
scoreboard players operation #blue_diff shulker_preview *= #blue_diff shulker_preview
scoreboard players add #mean shulker_preview 512
scoreboard players operation #red_diff shulker_preview *= #mean shulker_preview
scoreboard players operation #red_diff shulker_preview /= #256 shulker_preview
scoreboard players operation #green_diff shulker_preview *= #4 shulker_preview
scoreboard players operation #blue_diff shulker_preview *= #mean2 shulker_preview
scoreboard players operation #blue_diff shulker_preview /= #256 shulker_preview
scoreboard players operation #diff4 shulker_preview = #red_diff shulker_preview
scoreboard players operation #diff4 shulker_preview += #green_diff shulker_preview
scoreboard players operation #diff4 shulker_preview += #blue_diff shulker_preview
scoreboard players operation #nearest shulker_preview < #diff4 shulker_preview

# lime
scoreboard players operation #mean shulker_preview = #red shulker_preview
scoreboard players add #mean shulker_preview 128
scoreboard players operation #mean shulker_preview /= #2 shulker_preview
scoreboard players set #mean2 shulker_preview 767
scoreboard players operation #mean2 shulker_preview -= #mean shulker_preview
scoreboard players operation #red_diff shulker_preview = #red shulker_preview
scoreboard players remove #red_diff shulker_preview 128
scoreboard players operation #red_diff shulker_preview *= #red_diff shulker_preview
scoreboard players operation #green_diff shulker_preview = #green shulker_preview
scoreboard players remove #green_diff shulker_preview 199
scoreboard players operation #green_diff shulker_preview *= #green_diff shulker_preview
scoreboard players operation #blue_diff shulker_preview = #blue shulker_preview
scoreboard players remove #blue_diff shulker_preview 31
scoreboard players operation #blue_diff shulker_preview *= #blue_diff shulker_preview
scoreboard players add #mean shulker_preview 512
scoreboard players operation #red_diff shulker_preview *= #mean shulker_preview
scoreboard players operation #red_diff shulker_preview /= #256 shulker_preview
scoreboard players operation #green_diff shulker_preview *= #4 shulker_preview
scoreboard players operation #blue_diff shulker_preview *= #mean2 shulker_preview
scoreboard players operation #blue_diff shulker_preview /= #256 shulker_preview
scoreboard players operation #diff5 shulker_preview = #red_diff shulker_preview
scoreboard players operation #diff5 shulker_preview += #green_diff shulker_preview
scoreboard players operation #diff5 shulker_preview += #blue_diff shulker_preview
scoreboard players operation #nearest shulker_preview < #diff5 shulker_preview

# pink
scoreboard players operation #mean shulker_preview = #red shulker_preview
scoreboard players add #mean shulker_preview 243
scoreboard players operation #mean shulker_preview /= #2 shulker_preview
scoreboard players set #mean2 shulker_preview 767
scoreboard players operation #mean2 shulker_preview -= #mean shulker_preview
scoreboard players operation #red_diff shulker_preview = #red shulker_preview
scoreboard players remove #red_diff shulker_preview 243
scoreboard players operation #red_diff shulker_preview *= #red_diff shulker_preview
scoreboard players operation #green_diff shulker_preview = #green shulker_preview
scoreboard players remove #green_diff shulker_preview 139
scoreboard players operation #green_diff shulker_preview *= #green_diff shulker_preview
scoreboard players operation #blue_diff shulker_preview = #blue shulker_preview
scoreboard players remove #blue_diff shulker_preview 170
scoreboard players operation #blue_diff shulker_preview *= #blue_diff shulker_preview
scoreboard players add #mean shulker_preview 512
scoreboard players operation #red_diff shulker_preview *= #mean shulker_preview
scoreboard players operation #red_diff shulker_preview /= #256 shulker_preview
scoreboard players operation #green_diff shulker_preview *= #4 shulker_preview
scoreboard players operation #blue_diff shulker_preview *= #mean2 shulker_preview
scoreboard players operation #blue_diff shulker_preview /= #256 shulker_preview
scoreboard players operation #diff6 shulker_preview = #red_diff shulker_preview
scoreboard players operation #diff6 shulker_preview += #green_diff shulker_preview
scoreboard players operation #diff6 shulker_preview += #blue_diff shulker_preview
scoreboard players operation #nearest shulker_preview < #diff6 shulker_preview

# gray
scoreboard players operation #mean shulker_preview = #red shulker_preview
scoreboard players add #mean shulker_preview 71
scoreboard players operation #mean shulker_preview /= #2 shulker_preview
scoreboard players set #mean2 shulker_preview 767
scoreboard players operation #mean2 shulker_preview -= #mean shulker_preview
scoreboard players operation #red_diff shulker_preview = #red shulker_preview
scoreboard players remove #red_diff shulker_preview 71
scoreboard players operation #red_diff shulker_preview *= #red_diff shulker_preview
scoreboard players operation #green_diff shulker_preview = #green shulker_preview
scoreboard players remove #green_diff shulker_preview 79
scoreboard players operation #green_diff shulker_preview *= #green_diff shulker_preview
scoreboard players operation #blue_diff shulker_preview = #blue shulker_preview
scoreboard players remove #blue_diff shulker_preview 82
scoreboard players operation #blue_diff shulker_preview *= #blue_diff shulker_preview
scoreboard players add #mean shulker_preview 512
scoreboard players operation #red_diff shulker_preview *= #mean shulker_preview
scoreboard players operation #red_diff shulker_preview /= #256 shulker_preview
scoreboard players operation #green_diff shulker_preview *= #4 shulker_preview
scoreboard players operation #blue_diff shulker_preview *= #mean2 shulker_preview
scoreboard players operation #blue_diff shulker_preview /= #256 shulker_preview
scoreboard players operation #diff7 shulker_preview = #red_diff shulker_preview
scoreboard players operation #diff7 shulker_preview += #green_diff shulker_preview
scoreboard players operation #diff7 shulker_preview += #blue_diff shulker_preview
scoreboard players operation #nearest shulker_preview < #diff7 shulker_preview

# light_gray
scoreboard players operation #mean shulker_preview = #red shulker_preview
scoreboard players add #mean shulker_preview 157
scoreboard players operation #mean shulker_preview /= #2 shulker_preview
scoreboard players set #mean2 shulker_preview 767
scoreboard players operation #mean2 shulker_preview -= #mean shulker_preview
scoreboard players operation #red_diff shulker_preview = #red shulker_preview
scoreboard players remove #red_diff shulker_preview 157
scoreboard players operation #red_diff shulker_preview *= #red_diff shulker_preview
scoreboard players operation #green_diff shulker_preview = #green shulker_preview
scoreboard players remove #green_diff shulker_preview 157
scoreboard players operation #green_diff shulker_preview *= #green_diff shulker_preview
scoreboard players operation #blue_diff shulker_preview = #blue shulker_preview
scoreboard players remove #blue_diff shulker_preview 151
scoreboard players operation #blue_diff shulker_preview *= #blue_diff shulker_preview
scoreboard players add #mean shulker_preview 512
scoreboard players operation #red_diff shulker_preview *= #mean shulker_preview
scoreboard players operation #red_diff shulker_preview /= #256 shulker_preview
scoreboard players operation #green_diff shulker_preview *= #4 shulker_preview
scoreboard players operation #blue_diff shulker_preview *= #mean2 shulker_preview
scoreboard players operation #blue_diff shulker_preview /= #256 shulker_preview
scoreboard players operation #diff8 shulker_preview = #red_diff shulker_preview
scoreboard players operation #diff8 shulker_preview += #green_diff shulker_preview
scoreboard players operation #diff8 shulker_preview += #blue_diff shulker_preview
scoreboard players operation #nearest shulker_preview < #diff8 shulker_preview

# cyan
scoreboard players operation #mean shulker_preview = #red shulker_preview
scoreboard players add #mean shulker_preview 22
scoreboard players operation #mean shulker_preview /= #2 shulker_preview
scoreboard players set #mean2 shulker_preview 767
scoreboard players operation #mean2 shulker_preview -= #mean shulker_preview
scoreboard players operation #red_diff shulker_preview = #red shulker_preview
scoreboard players remove #red_diff shulker_preview 22
scoreboard players operation #red_diff shulker_preview *= #red_diff shulker_preview
scoreboard players operation #green_diff shulker_preview = #green shulker_preview
scoreboard players remove #green_diff shulker_preview 156
scoreboard players operation #green_diff shulker_preview *= #green_diff shulker_preview
scoreboard players operation #blue_diff shulker_preview = #blue shulker_preview
scoreboard players remove #blue_diff shulker_preview 156
scoreboard players operation #blue_diff shulker_preview *= #blue_diff shulker_preview
scoreboard players add #mean shulker_preview 512
scoreboard players operation #red_diff shulker_preview *= #mean shulker_preview
scoreboard players operation #red_diff shulker_preview /= #256 shulker_preview
scoreboard players operation #green_diff shulker_preview *= #4 shulker_preview
scoreboard players operation #blue_diff shulker_preview *= #mean2 shulker_preview
scoreboard players operation #blue_diff shulker_preview /= #256 shulker_preview
scoreboard players operation #diff9 shulker_preview = #red_diff shulker_preview
scoreboard players operation #diff9 shulker_preview += #green_diff shulker_preview
scoreboard players operation #diff9 shulker_preview += #blue_diff shulker_preview
scoreboard players operation #nearest shulker_preview < #diff9 shulker_preview

# purple
scoreboard players operation #mean shulker_preview = #red shulker_preview
scoreboard players add #mean shulker_preview 137
scoreboard players operation #mean shulker_preview /= #2 shulker_preview
scoreboard players set #mean2 shulker_preview 767
scoreboard players operation #mean2 shulker_preview -= #mean shulker_preview
scoreboard players operation #red_diff shulker_preview = #red shulker_preview
scoreboard players remove #red_diff shulker_preview 137
scoreboard players operation #red_diff shulker_preview *= #red_diff shulker_preview
scoreboard players operation #green_diff shulker_preview = #green shulker_preview
scoreboard players remove #green_diff shulker_preview 50
scoreboard players operation #green_diff shulker_preview *= #green_diff shulker_preview
scoreboard players operation #blue_diff shulker_preview = #blue shulker_preview
scoreboard players remove #blue_diff shulker_preview 184
scoreboard players operation #blue_diff shulker_preview *= #blue_diff shulker_preview
scoreboard players add #mean shulker_preview 512
scoreboard players operation #red_diff shulker_preview *= #mean shulker_preview
scoreboard players operation #red_diff shulker_preview /= #256 shulker_preview
scoreboard players operation #green_diff shulker_preview *= #4 shulker_preview
scoreboard players operation #blue_diff shulker_preview *= #mean2 shulker_preview
scoreboard players operation #blue_diff shulker_preview /= #256 shulker_preview
scoreboard players operation #diff10 shulker_preview = #red_diff shulker_preview
scoreboard players operation #diff10 shulker_preview += #green_diff shulker_preview
scoreboard players operation #diff10 shulker_preview += #blue_diff shulker_preview
scoreboard players operation #nearest shulker_preview < #diff10 shulker_preview

# blue
scoreboard players operation #mean shulker_preview = #red shulker_preview
scoreboard players add #mean shulker_preview 60
scoreboard players operation #mean shulker_preview /= #2 shulker_preview
scoreboard players set #mean2 shulker_preview 767
scoreboard players operation #mean2 shulker_preview -= #mean shulker_preview
scoreboard players operation #red_diff shulker_preview = #red shulker_preview
scoreboard players remove #red_diff shulker_preview 60
scoreboard players operation #red_diff shulker_preview *= #red_diff shulker_preview
scoreboard players operation #green_diff shulker_preview = #green shulker_preview
scoreboard players remove #green_diff shulker_preview 68
scoreboard players operation #green_diff shulker_preview *= #green_diff shulker_preview
scoreboard players operation #blue_diff shulker_preview = #blue shulker_preview
scoreboard players remove #blue_diff shulker_preview 170
scoreboard players operation #blue_diff shulker_preview *= #blue_diff shulker_preview
scoreboard players add #mean shulker_preview 512
scoreboard players operation #red_diff shulker_preview *= #mean shulker_preview
scoreboard players operation #red_diff shulker_preview /= #256 shulker_preview
scoreboard players operation #green_diff shulker_preview *= #4 shulker_preview
scoreboard players operation #blue_diff shulker_preview *= #mean2 shulker_preview
scoreboard players operation #blue_diff shulker_preview /= #256 shulker_preview
scoreboard players operation #diff11 shulker_preview = #red_diff shulker_preview
scoreboard players operation #diff11 shulker_preview += #green_diff shulker_preview
scoreboard players operation #diff11 shulker_preview += #blue_diff shulker_preview
scoreboard players operation #nearest shulker_preview < #diff11 shulker_preview

# brown
scoreboard players operation #mean shulker_preview = #red shulker_preview
scoreboard players add #mean shulker_preview 131
scoreboard players operation #mean shulker_preview /= #2 shulker_preview
scoreboard players set #mean2 shulker_preview 767
scoreboard players operation #mean2 shulker_preview -= #mean shulker_preview
scoreboard players operation #red_diff shulker_preview = #red shulker_preview
scoreboard players remove #red_diff shulker_preview 131
scoreboard players operation #red_diff shulker_preview *= #red_diff shulker_preview
scoreboard players operation #green_diff shulker_preview = #green shulker_preview
scoreboard players remove #green_diff shulker_preview 84
scoreboard players operation #green_diff shulker_preview *= #green_diff shulker_preview
scoreboard players operation #blue_diff shulker_preview = #blue shulker_preview
scoreboard players remove #blue_diff shulker_preview 50
scoreboard players operation #blue_diff shulker_preview *= #blue_diff shulker_preview
scoreboard players add #mean shulker_preview 512
scoreboard players operation #red_diff shulker_preview *= #mean shulker_preview
scoreboard players operation #red_diff shulker_preview /= #256 shulker_preview
scoreboard players operation #green_diff shulker_preview *= #4 shulker_preview
scoreboard players operation #blue_diff shulker_preview *= #mean2 shulker_preview
scoreboard players operation #blue_diff shulker_preview /= #256 shulker_preview
scoreboard players operation #diff12 shulker_preview = #red_diff shulker_preview
scoreboard players operation #diff12 shulker_preview += #green_diff shulker_preview
scoreboard players operation #diff12 shulker_preview += #blue_diff shulker_preview
scoreboard players operation #nearest shulker_preview < #diff12 shulker_preview

# green
scoreboard players operation #mean shulker_preview = #red shulker_preview
scoreboard players add #mean shulker_preview 94
scoreboard players operation #mean shulker_preview /= #2 shulker_preview
scoreboard players set #mean2 shulker_preview 767
scoreboard players operation #mean2 shulker_preview -= #mean shulker_preview
scoreboard players operation #red_diff shulker_preview = #red shulker_preview
scoreboard players remove #red_diff shulker_preview 94
scoreboard players operation #red_diff shulker_preview *= #red_diff shulker_preview
scoreboard players operation #green_diff shulker_preview = #green shulker_preview
scoreboard players remove #green_diff shulker_preview 124
scoreboard players operation #green_diff shulker_preview *= #green_diff shulker_preview
scoreboard players operation #blue_diff shulker_preview = #blue shulker_preview
scoreboard players remove #blue_diff shulker_preview 22
scoreboard players operation #blue_diff shulker_preview *= #blue_diff shulker_preview
scoreboard players add #mean shulker_preview 512
scoreboard players operation #red_diff shulker_preview *= #mean shulker_preview
scoreboard players operation #red_diff shulker_preview /= #256 shulker_preview
scoreboard players operation #green_diff shulker_preview *= #4 shulker_preview
scoreboard players operation #blue_diff shulker_preview *= #mean2 shulker_preview
scoreboard players operation #blue_diff shulker_preview /= #256 shulker_preview
scoreboard players operation #diff13 shulker_preview = #red_diff shulker_preview
scoreboard players operation #diff13 shulker_preview += #green_diff shulker_preview
scoreboard players operation #diff13 shulker_preview += #blue_diff shulker_preview
scoreboard players operation #nearest shulker_preview < #diff13 shulker_preview

# red
scoreboard players operation #mean shulker_preview = #red shulker_preview
scoreboard players add #mean shulker_preview 176
scoreboard players operation #mean shulker_preview /= #2 shulker_preview
scoreboard players set #mean2 shulker_preview 767
scoreboard players operation #mean2 shulker_preview -= #mean shulker_preview
scoreboard players operation #red_diff shulker_preview = #red shulker_preview
scoreboard players remove #red_diff shulker_preview 176
scoreboard players operation #red_diff shulker_preview *= #red_diff shulker_preview
scoreboard players operation #green_diff shulker_preview = #green shulker_preview
scoreboard players remove #green_diff shulker_preview 46
scoreboard players operation #green_diff shulker_preview *= #green_diff shulker_preview
scoreboard players operation #blue_diff shulker_preview = #blue shulker_preview
scoreboard players remove #blue_diff shulker_preview 38
scoreboard players operation #blue_diff shulker_preview *= #blue_diff shulker_preview
scoreboard players add #mean shulker_preview 512
scoreboard players operation #red_diff shulker_preview *= #mean shulker_preview
scoreboard players operation #red_diff shulker_preview /= #256 shulker_preview
scoreboard players operation #green_diff shulker_preview *= #4 shulker_preview
scoreboard players operation #blue_diff shulker_preview *= #mean2 shulker_preview
scoreboard players operation #blue_diff shulker_preview /= #256 shulker_preview
scoreboard players operation #diff14 shulker_preview = #red_diff shulker_preview
scoreboard players operation #diff14 shulker_preview += #green_diff shulker_preview
scoreboard players operation #diff14 shulker_preview += #blue_diff shulker_preview
scoreboard players operation #nearest shulker_preview < #diff14 shulker_preview

# black
scoreboard players operation #mean shulker_preview = #red shulker_preview
scoreboard players add #mean shulker_preview 29
scoreboard players operation #mean shulker_preview /= #2 shulker_preview
scoreboard players set #mean2 shulker_preview 767
scoreboard players operation #mean2 shulker_preview -= #mean shulker_preview
scoreboard players operation #red_diff shulker_preview = #red shulker_preview
scoreboard players remove #red_diff shulker_preview 29
scoreboard players operation #red_diff shulker_preview *= #red_diff shulker_preview
scoreboard players operation #green_diff shulker_preview = #green shulker_preview
scoreboard players remove #green_diff shulker_preview 29
scoreboard players operation #green_diff shulker_preview *= #green_diff shulker_preview
scoreboard players operation #blue_diff shulker_preview = #blue shulker_preview
scoreboard players remove #blue_diff shulker_preview 33
scoreboard players operation #blue_diff shulker_preview *= #blue_diff shulker_preview
scoreboard players add #mean shulker_preview 512
scoreboard players operation #red_diff shulker_preview *= #mean shulker_preview
scoreboard players operation #red_diff shulker_preview /= #256 shulker_preview
scoreboard players operation #green_diff shulker_preview *= #4 shulker_preview
scoreboard players operation #blue_diff shulker_preview *= #mean2 shulker_preview
scoreboard players operation #blue_diff shulker_preview /= #256 shulker_preview
scoreboard players operation #diff15 shulker_preview = #red_diff shulker_preview
scoreboard players operation #diff15 shulker_preview += #green_diff shulker_preview
scoreboard players operation #diff15 shulker_preview += #blue_diff shulker_preview
scoreboard players operation #nearest shulker_preview < #diff15 shulker_preview

execute if score #diff0 shulker_preview = #nearest shulker_preview run scoreboard players set #near_color shulker_preview 16383998
execute if score #diff1 shulker_preview = #nearest shulker_preview run scoreboard players set #near_color shulker_preview 16351261
execute if score #diff2 shulker_preview = #nearest shulker_preview run scoreboard players set #near_color shulker_preview 13061821
execute if score #diff3 shulker_preview = #nearest shulker_preview run scoreboard players set #near_color shulker_preview 3847130
execute if score #diff4 shulker_preview = #nearest shulker_preview run scoreboard players set #near_color shulker_preview 16701501
execute if score #diff5 shulker_preview = #nearest shulker_preview run scoreboard players set #near_color shulker_preview 8439583
execute if score #diff6 shulker_preview = #nearest shulker_preview run scoreboard players set #near_color shulker_preview 15961002
execute if score #diff7 shulker_preview = #nearest shulker_preview run scoreboard players set #near_color shulker_preview 4673362
execute if score #diff8 shulker_preview = #nearest shulker_preview run scoreboard players set #near_color shulker_preview 10329495
execute if score #diff9 shulker_preview = #nearest shulker_preview run scoreboard players set #near_color shulker_preview 1481884
execute if score #diff10 shulker_preview = #nearest shulker_preview run scoreboard players set #near_color shulker_preview 8991416
execute if score #diff11 shulker_preview = #nearest shulker_preview run scoreboard players set #near_color shulker_preview 3949738
execute if score #diff12 shulker_preview = #nearest shulker_preview run scoreboard players set #near_color shulker_preview 8606770
execute if score #diff13 shulker_preview = #nearest shulker_preview run scoreboard players set #near_color shulker_preview 6192150
execute if score #diff14 shulker_preview = #nearest shulker_preview run scoreboard players set #near_color shulker_preview 11546150
execute if score #diff15 shulker_preview = #nearest shulker_preview run scoreboard players set #near_color shulker_preview 1908001
