#import "@preview/pintorita:0.1.4"
#show raw.where(lang: "pintora"): it => pintorita.render(it.text, style: "default")

== Enemies

Enemies are implemented in the `entities` module. All enemies are dervied from 
one of the two enemy base classes, `GroundEnemy` and `FlyingEnemy`, which are 
implemented in the `base_enemies` submodule.

#align(center)[
```pintora
mindmap
@param layoutDirection TB
+ arcade.Sprite
++ BaseEnemy
+++ GroundEnemy
++++ ...
+++ FlyingEnemy
++++ ...
```
]

`BaseEnemy` implements the base functionality for all enemies, including the 
HP display text used primarily for debugging.

All enemies have their own physics engine in order to interact with the 
world properly:

- `GroundEnemy` has `arcade.PhysicsEnginePlatformer`, just like the player, which is suited for gravity-based sprites
- `FlyingEnemy` has `arcade.PhysicsEngineSimple`, which is preferred for simple collisions without gravity

Damage dealt between the player and enemies is handled by the logic included in `GameView.update()`.
As such, the player will take contact damage when overlapping with an enemy sprite,
while dealing damage through their attack.
