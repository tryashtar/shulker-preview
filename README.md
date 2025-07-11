### Downloads

[This pack is also available on Modrinth!](https://modrinth.com/datapack/shulker-preview-datapack/versions)

When downloading from that page, make sure to click the version you want, then download both the data pack and resource pack. If you just click the download button in the list view, [you'll only get the data pack.](https://github.com/modrinth/code/issues/2277)

|Version|Download|
|---|---|
|Minecraft 1.21.7|• [Data Pack]()<br/>• [Resource Pack]()|
|Minecraft 1.21.6|• [Data Pack]()<br/>• [Resource Pack]()|
|Minecraft 1.21.5|• [Data Pack]()<br/>• [Resource Pack]()|
|Minecraft 1.21.4|• [Data Pack]()<br/>• [Resource Pack]()|
|Minecraft 1.21.2 - 1.21.3|• [Data Pack]()<br/>• [Resource Pack]()|
|Minecraft 1.21 - 1.21.1|• [Data Pack]()<br/>• [Resource Pack]()|
|Minecraft 1.20.5 - 1.20.6|• [Data Pack]()<br/>• [Resource Pack]()|
|Minecraft 1.20.3 - 1.20.4|• [Data Pack]()<br/>• [Resource Pack]()|
|Minecraft 1.20 - 1.20.2|• [Data Pack]()<br/>• [Resource Pack]()|
|Minecraft 1.19.4|• [Data Pack]()<br/>• [Resource Pack]()|
|Minecraft 1.19.3|• [Data Pack]()<br/>• [Resource Pack]()|
|Minecraft 1.19 - 1.19.2|• [Data Pack]()<br/>• [Resource Pack]()|
|Minecraft 1.18.x|• [Data Pack]()<br/>• [Resource Pack]()|
|Minecraft 1.17.x|• [Data Pack]()<br/>• [Resource Pack]()|
|Minecraft 1.16.2 - 1.16.5|• [Data Pack]()<br/>• [Resource Pack]()|
|Minecraft 1.16 - 1.16.1|• [Data Pack]()<br/>• [Resource Pack]()|
|Minecraft 1.15.x|• [Data Pack]()<br/>• [Resource Pack]()|
|Minecraft 1.14.4|• [Data Pack]()<br/>• [Resource Pack]()|

---

### How to use

<ol>
 <li>Download the data pack and resource pack for your Minecraft version.</li>
 <li>
  <details>
   <summary><ins>Add the data pack to your world.</ins></summary>
   <ul>
    <li>Open your world's folder.</li>
    <img src="https://i.imgur.com/4RE3CG9.png" height="60" alt="Select your world"/> <br/>
    <img src="https://i.imgur.com/2Va0DRj.png" height="30" alt="Edit"/> <br/>
    <img src="https://i.imgur.com/KtjQMXo.png" height="30" alt="Open World Folder"/> <br/>
    <li>Drag the data pack zip from your <code>Downloads</code> folder to the <code>datapacks</code> folder in your world.</li>
    <img src="https://i.imgur.com/alG9zB8.png" height="120"/> <br/>
   </ul>
  </details>
 </li>
 <li>
  <details>
   <summary><ins>Equip the resource pack.</ins></summary>
   <ul>
    <li>Go to the resource packs screen.</li>
    <img src="https://i.imgur.com/ervUIn9.png" height="30" alt="Options..."/> <br/>
    <img src="https://i.imgur.com/AotNu07.png" height="30" alt="Resource Packs..."/> <br/>
    <li>Drag the resource pack zip from your <code>Downloads</code> folder onto the screen.</li>
    <img src="https://i.imgur.com/9sTaNUQ.png" height="160" alt="Yes"/> <br/>
    <li>Move the pack from <code>Available</code> to <code>Selected</code></li>
    <img src="https://i.imgur.com/P5F8mqW.png" height="60" alt="Select the pack">
   </ul>
  </details>
 </li>
 <li>Enter your world and enjoy!</li>
</ol>

---

### FAQ

* Does this work with Bukkit/Spigot/Paper?
   * No guarantees. I have experienced countless issues with these modded servers breaking vanilla behavior that this pack requires.
* Does this work with Optifine?
   * Yes.
* Does this work with other resource packs?
   * Items in the preview will look as they do in your personal resource pack, but blocks will appear with vanilla textures.
* What happens if players don't have the resource pack?
   * They will see the vanilla shulker box tooltip, though it may contain a few extra lines.
* How do I enable/disable ender chest previews or colored tooltips?
   * Run `/function tryashtar.shulker_preview:config/show_settings` and click the buttons to toggle these options.
* How do I completely uninstall the pack?
   * After disabling or removing the pack, the following artifacts will remain and must be cleared manually:
      * The `shulker_preview` scoreboard objective. This can be removed with `/scoreboard objectives remove shulker_preview`.
      * The temporary values saved to NBT storage. This can be removed by deleting the `command_storage_tryashtar.shulker_preview.dat` file from your world's `data` folder.
      * Any existing shulker boxes will still show the preview in the tooltip. To remove it, simply place and break the shulker box after the pack has been disabled.
* What is the dark theme pack?
  * That's an extra resource pack you can apply on top of the normal one. All it does is remove the container texture from the tooltip preview, so items appear directly on the vanilla tooltip background.
* It's not working for me!
   * First, please [follow these instructions](https://imgur.com/a/rBukto5) to diagnose and solve some very common issues.
   * If that didn't fix your problem, feel free to message me on twitter ([@tryashtar](https://twitter.com/tryashtar)) or discord (@tryashtar) and I will be happy to help.

---

### Changelog

```diff
1.21.7
+ Only 1.21.7 item (lava chicken music disc)

1.21.6
+ All 1.21.6 items
+ Use dialog instead of text menu for pack options (vanilla 25w20a)

1.21.5
+ All 1.21.5 items
+ Use SNBT text components (vanilla 25w02a)
+ Update component syntax (vanilla 25w04a)
+ Use toggle_tooltips instead of hide_additional_tooltip (vanilla 25w04a)
+ Update fallback translation (vanilla 25w04a)

1.21.4
+ All 1.21.4 items
+ Resin trims (vanilla 24w44a)
+ Support items with custom item_model components (vanilla 24w45a)
+ Hide text shadow of tooltip (vanilla 24w44a)
+ Changed broken elytra texture name (vanilla 24w45a)

1.21.2
+ All 1.21.2 items
+ All 1.21.2 experimental items
+ Changed bundle open texture (vanilla 24w33a)
+ Show honey for full beehives/nests (vanilla 24w35a)

1.21
+ All 1.21 items
+ Rename pack folders (vanilla 24w21a)

1.20.5
+ All 1.20.5 items (armadillo stuff)
+ All 1.20.5 experimental items
+ Show trims on armor
+ Show patterns on decorated pots
+ Show bundle fill bar
+ Show exact colors for colored items
+ Option for colored tooltips
+ Number textures are referenced directly
+ Tooltip textures are referenced directly
- Modded lore workaround and broken lore detection no longer performed
- Removed larger tooltip for items without a custom name
+ Use storage instead of entities for text components (vanilla 19w39a)
+ Use space provider instead of bitmap negative space (vanilla 22w11a)
+ Use macros instead of function trees (vanilla 23w31a)
+ Use item components (vanilla 24w09a)
+ Use item predicates (vanilla 24w11a)

1.20.3
+ All 1.20.3 experimental items
+ Changed grass to short grass (vanilla 1.20.3-pre1)

1.20
+ All 1.20 items
+ Use fallback instead of language trick (vanilla 23w03a)

1.19.4
+ All 1.19.4 experimental items
+ Changed some potion colors (vanilla 1.19.4-pre3)

1.19.3
+ All 1.19.3 items (four spawn eggs)
+ All 1.19.3 experimental items
+ Changed polar bear spawn egg colors (vanilla 22w44a)

1.19
+ All 1.19 items

1.18
+ Only 1.18 item (otherside music disc)
+ Increased crossbow durability (vanilla 21w37a)

1.17
+ All 1.17 items
+ Missing texture shown for unknown items
+ Use item command instead of shulker box loot table trick (vanilla 20w46a)
+ Use item command instead loot tables to resolve text components (vanilla 20w46a)
+ Use markers instead of area effect clouds (vanilla 21w15a)
+ Use separator text component instead of custom comma spacing (vanilla 21w15a)

1.16.2
+ Only 1.16.2 item (piglin brute spawn egg)
+ Icon for data pack (vanilla 20w27a)
+ Use contents for hover events instead of value (vanilla 20w17a)

1.16
+ All 1.16 items
+ Item textures are referenced directly
+ Banners and shields show their patterns
+ Ender chests with preview tooltips now stack
+ Settings menu function
+ Option to disable shulker box previews
- Chests and other containers are no longer processed
+ Use loot tables instead of sign to resolve text components
+ Custom colored armor, potions, etc. show approximate colors (vanilla 20w17a)
+ Use custom font (vanilla 20w17a)

1.15
+ All 1.15 items
+ Alternate lore generation method when modded server is detected, to work around large lores getting deleted
+ Detect when modded server breaks lore and show an error message tooltip
+ Use magic number in language fallback trick
+ Use storage instead of jukebox for item processing (vanilla 19w38a)

1.14
+ All 1.14 items
+ Vanilla tooltip shown for players without the pack
+ Option to preview ender chests
+ Optifine compatibility
+ Intel compatibility (work around MC-180529)
+ Custom item name shown in tooltip
+ More accurate durability bars
+ Forceloaded chunk created automatically (vanilla 1.14.4-pre4)
```
