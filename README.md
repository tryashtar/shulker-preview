### Downloads

|Version|Download|
|---|---|
|Minecraft 1.19|• [Data Pack](1.19/Shulker%20Preview%20Data%20Pack%20(1.19).zip?raw=1)<br>• [Resource Pack](1.19/Shulker%20Preview%20Resource%20Pack%20(1.19).zip?raw=1)|
|Minecraft 1.18|• [Data Pack](1.18/Shulker%20Preview%20Data%20Pack%20(1.18).zip?raw=1)<br>• [Resource Pack](1.18/Shulker%20Preview%20Resource%20Pack%20(1.18).zip?raw=1)|
|Minecraft 1.17|• [Data Pack](1.17/Shulker%20Preview%20Data%20Pack%20(1.17).zip?raw=1)<br>• [Resource Pack](1.17/Shulker%20Preview%20Resource%20Pack%20(1.17).zip?raw=1)|
|Minecraft 1.16|• [Data Pack](1.16/Shulker%20Preview%20Data%20Pack%20(1.16).zip?raw=1)<br>• [Resource Pack](1.16/Shulker%20Preview%20Resource%20Pack%20(1.16).zip?raw=1)|
|Minecraft 1.15|• [Data Pack](1.15/Shulker%20Preview%20Data%20Pack%20(1.15).zip?raw=1)<br>• [Resource Pack](1.15/Shulker%20Preview%20Resource%20Pack%20(1.15).zip?raw=1)|
|Minecraft 1.14.3|• [Data Pack](1.14/Shulker%20Preview%20Data%20Pack%20(1.14).zip?raw=1)<br>• [Resource Pack](1.14/Shulker%20Preview%20Resource%20Pack%20(1.14).zip?raw=1)|

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
   * In 1.16+, items in the preview will look as they do in your personal resource pack, but blocks will appear with vanilla textures.
   * In earlier versions, both items and blocks will use vanilla textures. Also, the pack may conflict with other packs that override private use characters.
* What happens if players don't have the resource pack?
   * They will see the vanilla shulker box tooltip, though it may contain a few extra lines.
* How do I disable/enable ender chest previews?
   * In 1.16+: `/function tryashtar.shulker_preview:config/show_settings`
   * In earlier versions, there are two functions in `.meta`
* How do I completely uninstall the pack?
   * After disabling the pack with `/datapack disable`, the following artifacts will remain and must be cleared manually:
      * The `shulker_preview` scoreboard objective. This can be removed with `/scoreboard objectives remove shulker_preview`.
      * In 1.16 and earlier, a forceloaded chunk near the worldborder. This can be removed with `/forceload remove 29999977 9832`. If you wish, you can also delete the region file containing this chunk: `r.58593.19.mca`.
      * The temporary values saved to NBT storage. This can be removed by deleting the `command_storage_tryashtar.shulker_preview.dat` file from your world's `data` folder.
      * Any existing shulker boxes will still show the preview in the tooltip. To remove it, simply place and break the shulker box after the pack has been disabled.
* It's not working for me!
   * First, please [follow these instructions](https://imgur.com/a/rBukto5) to diagnose and solve some very common issues.
   * If that didn't fix your problem, feel free to message me on twitter ([@tryashtar](https://twitter.com/tryashtar)) or discord (@tryashtar#7885) and I will be happy to help.

### Changelog
```diff
Current 1.18 version
+ All 1.18 items (all one of them)

Current 1.17 version
+ All 1.17 items
+ Unknown items show a missing texture instead of messing up the order
+ No longer requires forceloaded chunk

Current 1.16 version
+ All 1.16 items
+ Now uses custom font, preventing potential private use conflicts
+ Item textures use the player's current resource pack
+ Banners and shields show their pattern
+ Custom colored armor, potions, etc. show approximate colors
+ When ender chest previews are enabled, ender chests showing the same preview can stack
+ New settings menu for toggling previews for shulker boxes and ender chests

Current 1.15 version
+ All 1.15 items
+ When Bukkit server is detected, switches to slower but fewer-character lore generation method
+ Detects when Bukkit mangles lore, and adds text to the tooltip notifying you

Current 1.14 version
+ All 1.14 items
+ Option to preview ender chests
+ Optifine compatibility
+ No longer crashes on certain graphics cards
+ Show custom item name in tooltip
+ More accurate durability bars
+ Data pack no longer requires clicking forceload text
+ Default Minecraft tooltip appears for players without the pack

Video release
+ Dropped shulker box items are processed

Initial release (reddit)
```
