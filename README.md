# ZoteBoat

A project made for IA4: Python Projects by 2 student

ZoteBoat is a small metroidvania made in Python, that seeks to replicate the
the feel of the original Hollow Knight game made by Team Cherry. The game
has an open area to explore and two addicting minigames to master with
most of the features that are expected of a metroidvania. Explore, test your
skills and become stronger while meeting many intruiging characters, some of
which are willing to sell you upgrades to aid you in your travels.

## GitHub Link

https://github.com/RagnarokMew/ZoteBoat

## Technologies used

- Python
- Python Arcade Library (and its dependencies such as Pyglet, Pillow, etc)
- JSON
- Tiled

## How to use / run

### Before you start

Make sure that in the root of the project you have the following folders:

- `src` - contains the source code of the app
- `saves` - contains the save files of different users
- `assets` - contains all the assets used by the game such as sprites and maps

To run the game you need to go into the `src` folder and run `main.py` with python:

```bash
cd src
python main.py
```

### Main Menu

Upon booting the game you will be met by the main menu where you will be
presented with multiple options:

- `Play` - jumps into the game with the setting set in options
- `Leaderboard` - view the scores of all local players
- `Credits` - view the credits of the game
- `Options` - change the settings of the game
- `Quit` - exits the game

!!! IMPORTANT !!!

Upon starting the game by running `python main.py`, you should go to the
`Options` menu and set a username. The username is saved in the current session
but upon closing and restarting the game with the `python main.py` it gets
reset. If you do not set a username in `Options` you will use the default user
`default`.

While in `Options` you can choose if you want to display enemy hp or not. This
is considered more of a debug setting as Hollow Knight does not display them
but we believe the user should be able to choose

### Controls

The control scheme matches the one of Hollow Knight being:

- `Arrow Keys` - movement keys
- `Z` - jumping & double jumping & walljumping
- `X` - attack
- `C` - dash
- `Esc` - quit to main menu

## Media

TODO: screenshots and video links

## Team Contribution

### RagnarokMew (Stefan Simion 324CC)

TODO

### Luxaks (Lucas Ciuca 324CC)

TODO

## Implementation Difficulties

### Movement Physics

One of the greatest problems we encountered during the development of Zoteboat
was the implementation of the movement physics.

Originally we planned to use the Pymunk Physiscs Engine included with Arcade and
wrote the basic movement mechanics with it, but we had difficulties in making the
player character stop moving as they continued to glide as if the ground was ice
despite setting the friction with the ground to be quite high.

After that we decided to completely rewrite the movement with the Arcade Physics
Engine placing our movement logic in the `on_key_pressed` functions and this
worked well until we implemented the map changing logic and did some testing.
While implementing more complex movement mechanics we discovered that the player
character would glide on the new map despite no movement keys being pressed.

We discovered this was because when the map changed, the key press handling made
in Arcade was interfering with the preservation of movement we implemented to
make the transitions work. We tried some workarounds like forcefully decreasing
the speeds but it introduced more bugs than it fixed.

As a final resort we once again rewrote the whole movement logic moving
everything to `on_update` and only the key detection in the old system. This
did not come without its own problems as this rewrite broke our advanced
movement mechanics logic that was based on our old movement. We were forced
to also rewrite this logic arriving at the current implementation of our
movement mechanics.

### Arcade Pixel Coordinates

TODO

TODO: Any extra sections we wish to include
