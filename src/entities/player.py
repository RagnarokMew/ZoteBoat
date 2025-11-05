import arcade
from core.constants import P_ATTACK_COOLDOWN, P_ATTACK_DAMAGE, P_HEALTH

class PlayerSprite(arcade.Sprite):

    def __init__(self, scene, position=(0, 0), scale=1.0):
        # TODO: Change temp asset to one of our own towards the end of development
        super().__init__(
            ":resources:images/animated_characters/robot/robot_idle.png",
            scale=scale
        )

        self.scene = scene
        self.center_x, self.center_y = position
        self.player_attack = None
        self.attack_cooldown = 0.0
        self.health = P_HEALTH
        # TODO: Add textures for player (idle, walk, etc)
        # TODO: Should also work on logic to handle direction facing etc
        # The implementation of these features can be done later on

    # TODO: Should also work on logic to handle direction facing etc
    # The implementation of these features can be done later on

    def attack(self):
        if(self.attack_cooldown > 0):
            return

        a_x, a_y = self.position
        a_x += 100
        a_y += 10

        self.player_attack = PlayerAttack(
            self.scene,
            self
        )

        self.attack_cooldown = P_ATTACK_COOLDOWN

    def update(self, delta_time):
        if(self.attack_cooldown > 0):
            self.attack_cooldown -= delta_time

        if(self.player_attack != None):
            self.player_attack.position = self.position
            self.player_attack.update(delta_time)


class PlayerAttack(arcade.Sprite):

    def __init__(self, scene, parent, scale=1.0, damage=P_ATTACK_DAMAGE):
        super().__init__(
            # TODO: Change temp sprite with one of our own
            ":resources:/onscreen_controls/flat_dark/right.png",
            scale=scale
        )

        self.parent = parent
        self.scene = scene
        self.damage = damage
        self.remaining_duration = P_ATTACK_COOLDOWN

        self.scene.add_sprite("PlayerAttack", self)

    def update(self, delta_time):
        # TODO: Update position based on Player
        self.remaining_duration -= delta_time
        self.center_x = self.parent.center_x + 32
        self.center_y = self.parent.center_y

        if(self.remaining_duration <= 0):
            self.remove_from_sprite_lists()

