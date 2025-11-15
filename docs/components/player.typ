== Player Character
The player character is mostly implemented in the entities module and has 3 important classes `PlayerSprite`, `PlayerAttack` in `entities.player` and `PlayerStats` in `core.player_stats`.

// TODO: Update the PlayerSprite section by mentioning abilities
`PlayerSprite` is derived from `arcade.Sprite` and implements the following functions:

- `attack()`: makes the player attack by spawning a `PlayerAttack`
- `update()`: updates the attack cooldown, calls `PlayerAttack.update()` and `update_animation()`
- `update_animation()`: changes the player animation based on the current state
- `_load_textures()`: internal function called once to load all player textures required for player animations
- `_next_texture()`: changes the current texture of the animation to the next one

`PlayerAttack` is derived from `arcade.Sprite` and implements the following function:

- `update()`: changes the scale and position of the attack based on player directionality and despawns the attack when its duration has expired

`PlayerStats` is a helper that holds important player statistics that 
shouldn't reset when a scene changes. Its fields include but aren't limited to:

- `inv_time`: how much invincibility time the player still has left after taking damage
- `damage`: the amount of damage the player deals to enemies with attacks
- `health`: the current health the player has

// TODO: Update controls section if needed
The player controls are handled in the `GameView` where keypresses are checked 
and the appropriate handler function gets called.

The player's physics engine is placed in `GameView`. The player character's and 
its attacks' collisions are also handled in `GameView`.
