== Scene Loader
The way scenes change is implemented with 3 functions in the `GameView`:

- `change_map`: if a transition hasn't occured yet, check for scene change conditions (such as collision with a `Load Zone`) and set up the correct data (new scene ID, entry point, initial trajectory), then begin the transition animation 
- `update_fade`: if not already fading, the screen first gets darker, then brighter (handled by a loop that increments/decrements the transparency of a solid black overlay); the actual scene change occurs at maximum darkness (when the overlay is fully opaque, create the new scene with the parameters set by `change_map`)
- `draw_fading`: on each frame, if needed, draw the black overlay using the correct transparency set by `update_fade`.

A bug which can occur when changing the scene is having the Player move when they shouldn't. This is because, upon a scene change, the game forgets whether the Player should move or not (only key presses and releases are detected, so if the movement begins before a transition, the Player will gain a permanent speed in the opposite direction afterwards). The fix we implemented is to simply save and restore the Player's state in the `GameView` when the transition actually occurs.
