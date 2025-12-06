import arcade
from arcade.color import BLACK
from core.constants import GRAVITY, CELL_SIZE
from entities.utils import load_texture_pair_h, count_files

class BaseEnemy(arcade.Sprite):
    def __init__(self, scene, sprite_path,
                 position=(128, 128),
                 scale=1,
                 damage=1,
                 max_health=1,
                 drop_curr1=1,
                 drop_curr2=1,
                 drop_curr3=1,
                 drop_curr4=1,
                 frame_duration=100):
        self._load_texture(sprite_path)
        super().__init__(
            self.animations["wander"][0][0],
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

        self.cur_textures = self.animations["wander"]
        self.cur_tex_index = 0
        self.cur_frame_duration = 0
        self.animation_state = "wander"
        self.frame_duration = frame_duration

        self.spawn_x, self.spawn_y = position
        self.ai_state = "idle"

    def update_text(self):
        self.hp_text.text = f"HP:{self.health}/{self.max_health}"

    def update(self, delta_time):
        self.hp_text.x = self.center_x
        self.hp_text.y = self.center_y + self.texture.height // 2 + 10

        if self.inv_time >= 0:
            self.inv_time -= delta_time

        self.update_animation(delta_time)

    def update_animation(self, delta_time):
        self.cur_textures = self.animations[self.animation_state]

        self._next_texture(delta_time)

    def _next_texture(self, delta_time):
        self.cur_frame_duration += delta_time

        if self.cur_frame_duration * 1000 < self.frame_duration:
            return

        self.cur_frame_duration = 0

        self.cur_tex_index += 1
        self.cur_tex_index %= len(self.cur_textures)

        if self.change_x > 0:
            self.texture = self.cur_textures[self.cur_tex_index][1]
        else:
            self.texture = self.cur_textures[self.cur_tex_index][0]


    def _load_texture(self, base_path):
        wander_path = f"{base_path}wander"

        wander_textures = [
            load_texture_pair_h(f"{base_path}wander_{i}.png") for i in range(0, count_files(base_path, "wander"))
        ]

        self.animations = {
            "wander": wander_textures
        }

class GroundEnemy(BaseEnemy):
    def __init__(self, scene, sprite_path,
                 scale=1,
                 damage=1,
                 max_health=1,
                 position=(128,128),
                 drop_curr1=1,
                 drop_curr2=1,
                 drop_curr3=1,
                 drop_curr4=1,
                 frame_duration=100):

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
            drop_curr4=drop_curr4,
            frame_duration=frame_duration
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
    def __init__(self, scene, sprite_path,
                 scale=1,
                 damage=1,
                 max_health=1,
                 position=(128,128),
                 drop_curr1=1,
                 drop_curr2=1,
                 drop_curr3=1,
                 drop_curr4=1,
                 frame_duration=100):
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
            drop_curr4=drop_curr4,
            frame_duration=frame_duration
        )

        self.physics_engine = arcade.PhysicsEngineSimple(
            self, scene["Platforms"]
        )

    def update(self, delta_time):
        super().update(delta_time)

        self.physics_engine.update()
        if(self.health <= 0):
            pass


