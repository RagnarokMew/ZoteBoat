ZoteBoat runs entirely on the player's local machine.

== Launch
Upon launching the game, using the Arcade library, a new GameView is created,
which essentially contains all the elements to be rendered in the game window.
Then, scenes are loaded in, depending on context (first, a main menu; then, the
levels/arenas where the player character can move around).

== Scenes
The algorithm for scene loading is as follows:
- fetch the corresponding XML file, and generate a new Scene object
- create the Player sprite
- look for Enemy spawn points, and create those sprites as well
- set up the correct layers and render everything to screen.
This logic is also used whenever a room transition occurs (simply load
a new scene with the necessary attributes).

== Player
The player character (Zote the Mighty) is created using his own class
containing the movement and attack logic. Zote is controlled using the
arrow keys, Z for jumping, X for attacking, and C for dashing.

== Enemies
// enemy implementation

== Loader
As mentioned earlier, whenever entering a new room, the scene has to be
changed. This is done via a level loader in the GameView class:

When interacting with a door or overlapping with the Load Zone layer
in the map, the next scene ID and other data are read from the sprite.
Then, the screen fades to black; once fully dark, the scene is reloaded
as described above, and the screen turns back to normal.
In the case of a vertical transition (the player goes up), a jump-like
trajectory is also added to the player's movement.
