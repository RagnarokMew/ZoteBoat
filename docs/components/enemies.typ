#import "@preview/pintorita:0.1.4"
#show raw.where(lang: "pintora"): it => pintorita.render(it.text, style: "default")

== Enemies

Enemies are implemented in the `entities` module. All enemies are dervied from 
one of the two enemy base classes `GroundEnemy` and `FlyingEnemy` which are 
implemented in the `base_enemies` submodule, as can be seen below:

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
hp display text used primarily for debugging.

All enemies have their own physics engine in order to interact with the 
world properly:

- `GroundEnemy` has `arcade.PhysicsEnginePlatformer`, which is suited for gravity-based sprites
- `FlyingEnemy` has `arcade.PhysicsEngineSimple`, which is preferred for simple collision with platforms, without gravity

Enemies deal contact damage to the player and the taking/dealing damage logic 
handled in `GameView.update()`.
