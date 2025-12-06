import arcade
from arcade.color import BLACK
from core.constants import GRAVITY, CELL_SIZE

class BaseEnemy(arcade.Sprite):
    def __init__(self, scene, sprite_path,
                 position=(128, 128),
                 scale=1,
                 damage=1,
                 max_health=1,
                 drop_curr1=1,
                 drop_curr2=1,
                 drop_curr3=1,
                 drop_curr4=1):
        super().__init__(
            sprite_path,
            scale=scale
        )

        self.inv_time = 0
        self.center_x, self.center_y = position
        self.scene = scene
        self.damage = damage
        self.max_health = max_health
        self.health = max_health
        self.hp_text = arcade.Text(
            f"HP:{self.health}/{self.max_health}",
            x=self.center_x,
            y=self.center_y + 10,
            color=arcade.color.BLACK,
            font_size=15,
            anchor_x="center"
        )

        self.drop_curr1 = drop_curr1
        self.drop_curr2 = drop_curr2
        self.drop_curr3 = drop_curr3
        self.drop_curr4 = drop_curr4

    def update_text(self):
        self.hp_text.text = f"HP:{self.health}/{self.max_health}"

    def update(self, delta_time):
        self.hp_text.x = self.center_x
        self.hp_text.y = self.center_y + 10

        if self.inv_time >= 0:
            self.inv_time -= delta_time

class GroundEnemy(BaseEnemy):
    def __init__(self, scene,
                 sprite_path=":resources:/images/enemies/slimePurple.png",
                 scale=1,
                 damage=1,
                 max_health=1,
                 position=(128,128),
                 drop_curr1=1,
                 drop_curr2=1,
                 drop_curr3=1,
                 drop_curr4=1):

        super().__init__(
            scene,
            sprite_path,
            scale=scale,
            max_health=max_health,
            position=position,
            damage=damage,
            drop_curr1=drop_curr1,
            drop_curr2=drop_curr2,
            drop_curr3=drop_curr3,
            drop_curr4=drop_curr4
        )

        self.physics_engine = arcade.PhysicsEnginePlatformer(
            self, scene["Platforms"], GRAVITY
        )

    def update(self, delta_time):
        super().update(delta_time)

        self.physics_engine.update()
        if(self.health <= 0):
            pass

class FlyingEnemy(BaseEnemy):
    def __init__(self, scene,
                 sprite_path=":resources:/images/enemies/bee.png",
                 scale=1,
                 damage=1,
                 max_health=1,
                 position=(128,128),
                 drop_curr1=1,
                 drop_curr2=1,
                 drop_curr3=1,
                 drop_curr4=1):
        super().__init__(
            scene,
            sprite_path,
            scale=scale,
            max_health=max_health,
            position=position,
            damage=damage,
            drop_curr1=drop_curr1,
            drop_curr2=drop_curr2,
            drop_curr3=drop_curr3,
            drop_curr4=drop_curr4
        )

        self.physics_engine = arcade.PhysicsEngineSimple(
            self, scene["Platforms"]
        )

    def update(self, delta_time):
        super().update(delta_time)

        self.physics_engine.update()
        if(self.health <= 0):
            pass


