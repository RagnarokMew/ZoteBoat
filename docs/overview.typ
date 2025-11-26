The general architecture of the game is split between multiple components
(each implemented in its own class), making use of Python's poweful OOP capacities.

== Launch
Upon launching the game, a new `GameView` (inheriting Arcade's `View` class) is created,
which essentially contains all the elements to be rendered in the game window.
Then, scenes are loaded in, depending on context (first, a main menu; then, the
levels/arenas where the player character can move around).

== Scenes
The algorithm for scene loading is as follows:

- fetch the corresponding XML file, and generate a new `Scene` object
- create the player sprite
- look for enemy spawn points, and place their sprites at those locations
- set up the correct layers and render everything to screen.  

Using Tiled, different sprites (positions) in the map can contain
key-value pairs of custom data, which helps with setting up the scene.

This logic is also used whenever a room transition occurs (simply load
a new scene with the necessary attributes).

== Player
The player character (Zote the Mighty) is created using his own class
containing the movement and attack logic. Zote is controlled using the
arrow keys, Z for jumping, X for attacking, and C for dashing.

== Enemies
Throughout the game, Zote will encounter various challenges, of which
enemies will be the primary one. Taking advantage of the game's internal class
hierarchy, each enemy has its own attacks and behaviour, which the player
must counter accordingly.

== Loader
As mentioned earlier, whenever entering a new room, the scene has to be
changed. This is done via a level loader in the GameView class:

When interacting with a door or overlapping with the `Load Zone` layer
in the map, the next scene ID and other data are read from the sprite.
Then, the screen fades to black; once fully dark, the scene is reloaded
as described above, and the screen turns back to normal.
In the case of a vertical transition (the player goes up), a jump-like
trajectory is also added to the player's movement.
