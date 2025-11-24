# On the Subject of Tilemaps

The below document will detail the functionality and usage of the program known as Tiled, for creating maps for ZoteBoat. The complete documentation can be found [here](https://doc.mapeditor.org/en/stable/).

## Installation & Running

In order to create tilemaps, you must first install [Tiled from itch.io](https://thorbjorn.itch.io/tiled). For Linux systems, the AppImage version is the only one available. However, if you do not want to actually install the AppImage, you can instead unpack it using a command which will look like this:

`./Tiled-1.11.2_Linux_Qt-6_x86_64.AppImage --appimage-extract `

This will create a new directory containing the executable files. Finally, run either `AppRun` or `AppRun.wrapped`. Congrats! You are now ready to start making maps for our beautiful game.

## Creating a New Tilemap

Once Tiled is run, you will be greeted by this screen:

<img src="doc_img/main_screen.png" style="padding: 1em">

To begin, click `File > Open File or Project...` or `Ctrl+O` and open `zoteboat.tiled-project`. This file doesn't do much, except enable you to navigate the filesystem in the built-in panel on the left.

Then, to create a new map for whatever area you want, click `New Map...` (or `File > New`) and save it under `assets/tilemaps` with the `.tmx` extension. The tile size should be 128x128 px. The map size can be infinite, since it doesn't affect performance, although you could restrain yourself if you want :)

To move around the main view, use the scroll bars on the right and below (sadly, touchpad scrolling seems inconsistent). To zoom in/out, `Ctrl+scroll` will do the trick.

<img src="doc_img/new_map.png" style="padding: 1em">

## Adding Tiles

First, open whichever *tileset* you want to add tiles from (double click the file in the left panel). You can also create a new tileset if you need to. A tileset is created similar to a map; however, make sure it is a **collection of images**, which allows you to add any sprites you want instead of relying on a spritesheet.

Then, return to the map tab (while leaving the set tab open). Tiles will now be available in the lower-right corner. To add them to your map, just click the tile you want, then click on the grid. To erase tiles, use the *eraser* (`E`); then, to return to painting mode, either use the *brush* (`B`) or click a new tile.

## Layers

You will notice that so far, all tiles will live on the same layer. To give our scene depth (and to later allow for special-purpose tiles), create a new *tile layer* by right-clicking on the upper-right panel, and selecting `New > Tile Layer`. The naming and order of the layers should be as follows:

* Foreground
* Enemy Spawn (optional)
* Load Zone
* Platforms