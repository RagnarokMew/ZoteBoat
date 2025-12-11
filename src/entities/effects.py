import arcade
from core.constants import P_INV_TIME

class EffectDmg(arcade.Sprite):
    def __init__(self, parent, scene, dmg_type = "enemy", scale = 0.8):
        super().__init__(
            f"../assets/sprites/player/dmg_{dmg_type}.png",
            scale = scale
        )

        self.parent = parent
        self.position = self.parent.position
        self.scene = scene
        if dmg_type == "enemy":
            self.type = 1.1
        else:
            self.type = 1
        self.remaining_duration = P_INV_TIME // self.type

        self.scene.add_sprite("EffectDmg", self)

    def update(self, delta_time):
        self.position = self.parent.position
        self.remaining_duration -= delta_time
        self.alpha = 195 * self.type * self.remaining_duration
        if self.remaining_duration <= 0:
            self.remove_from_sprite_lists()
            self.parent.dmg_effect = None

class EffectFly(arcade.Sprite):

    def __init__(self, parent, scene, scale = 0.8):
        self.fly = [
            arcade.load_texture(f"../assets/sprites/player/fly_{i}.png") for i in range(0,3)
        ]

        super().__init__(
            self.fly[0],
            scale = scale
        )

        self.parent = parent
        self.position = self.parent.position
        self.offset = -48
        self.scene = scene
        self.remaining_duration = P_INV_TIME / 4

        self.scene.add_sprite("EffectFly", self)
    
    def update(self, delta_time):
        self.center_x = self.parent.center_x
        self.center_y = self.parent.center_y + self.offset
        self.remaining_duration -= delta_time

        if self.remaining_duration > 0.214:
            self.texture = self.fly[0]
        elif self.remaining_duration > 0.107:
            self.texture = self.fly[1]
        elif self.remaining_duration > 0:
            self.texture = self.fly[2]
        else:
            self.remove_from_sprite_lists()
            self.parent.dmg_effect = None