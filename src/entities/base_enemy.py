import arcade
from core.constants import GRAVITY

class GroundEnemy(arcade.Sprite):
    def __init__(self, scene, path=":resources:/images/enemies/slimePurple.png", scale=1, damage=1, max_health=1, position=(128,128)):
        super().__init__(
            path,
            scale=scale
        )

        self.center_x, self.center_y = position
        self.scene = scene
        self.max_health = max_health
        self.health = max_health
        self.physics_engine = arcade.PhysicsEnginePlatformer(
            self, scene["Platforms"], GRAVITY
        )


    def update(self, delta_time):
        self.physics_engine.update()
        if(self.health <= 0):
            pass
