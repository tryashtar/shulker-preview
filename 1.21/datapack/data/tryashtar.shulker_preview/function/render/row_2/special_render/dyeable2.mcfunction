# dyeable items render with a base layer and a colored layer
# wolf armor uniquely doesn't render its top layer when not dyed
$execute if score #has_color shulker_preview matches 1 if items entity @s contents wolf_armor run data modify storage tryashtar.shulker_preview:data tooltip append value [{translate:"tryashtar.shulker_preview.layer.$(id).0.2"},{translate:"tryashtar.shulker_preview.layer.minecraft:wolf_armor.1.2",color:"#$(red)$(green)$(blue)"}]
execute if score #has_color shulker_preview matches 0 if items entity @s contents wolf_armor run data modify storage tryashtar.shulker_preview:data tooltip append value {translate:"tryashtar.shulker_preview.item.minecraft:wolf_armor.2"}
$execute unless items entity @s contents wolf_armor run data modify storage tryashtar.shulker_preview:data tooltip append value [{translate:"tryashtar.shulker_preview.layer.$(id).0.2",color:"#$(red)$(green)$(blue)"},{translate:"tryashtar.shulker_preview.layer.$(id).1.2",color:"white"}]
