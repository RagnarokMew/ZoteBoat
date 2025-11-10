import arcade
from arcade.color import BLACK
from core.constants import GRAVITY

class BaseEnemy(arcade.Sprite):
    def __init__(self, scene, sprite_path, position=(128, 128), scale=1, damage=1, max_health=1):
        super().__init__(
            sprite_path,
            scale=scale
        )

        self.center_x, self.center_y = position
        self.scene = scene
        self.damage = damage
        self.max_health = max_health
        self.health = max_health
        self.hp_text = arcade.Text(
            f"{self.health}/{self.max_health}",
            x=0,
            y=0,
            color=arcade.color.BLACK,
            font_size=10
        )

    def update_text(self):
        self.hp_text.text = f"{self.health}/{self.max_health}"

class GroundEnemy(BaseEnemy):
    def __init__(self, scene, sprite_path=":resources:/images/enemies/slimePurple.png", scale=1, damage=1, max_health=1, position=(128,128)):
        super().__init__(
            scene,
            sprite_path,
            scale=scale,
            max_health=max_health,
            position=position,
            damage=damage
        )

        self.physics_engine = arcade.PhysicsEnginePlatformer(
            self, scene["Platforms"], GRAVITY
        )


    def update(self, delta_time):
        self.physics_engine.update()
        if(self.health <= 0):
            pass

class FlyingEnemy(BaseEnemy):
    def __init__(self, scene, sprite_path=":resources:/images/enemies/bee.png", scale=1, damage=1, max_health=1, position=(128,128)):
        super().__init__(
            scene,
            sprite_path,
            scale=scale,
            max_health=max_health,
            position=position,
            damage=damage

        )

        self.physics_engine = arcade.PhysicsEngineSimple(
            self, scene["Platforms"]
        )

    def update(self, delta_time):
        self.physics_engine.update()
        if(self.health <= 0):
            pass


