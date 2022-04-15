execute if entity @a[limit=1] run schedule function tryashtar.shulker_preview:.meta/player_online 1s
execute unless entity @a[limit=1] run schedule function tryashtar.shulker_preview:.meta/await_player 2s
