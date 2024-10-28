# these items have model override predicates, requiring special checks to render properly
execute if items entity @s contents bee_nest run return run function tryashtar.shulker_preview:render/row_1/special_render/bee_nest with storage tryashtar.shulker_preview:data item
execute if items entity @s contents beehive run return run function tryashtar.shulker_preview:render/row_1/special_render/beehive with storage tryashtar.shulker_preview:data item
execute if items entity @s contents crossbow run return run function tryashtar.shulker_preview:render/row_1/special_render/crossbow with storage tryashtar.shulker_preview:data item
execute if items entity @s contents elytra run return run function tryashtar.shulker_preview:render/row_1/special_render/elytra with storage tryashtar.shulker_preview:data item
execute if items entity @s contents light run return run function tryashtar.shulker_preview:render/row_1/special_render/light with storage tryashtar.shulker_preview:data item
