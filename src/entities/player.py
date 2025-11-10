import arcade
from core.constants import P_ATTACK_COOLDOWN, RIGHT_FACING, LEFT_FACING, UP_FACING, DOWN_FACING, SIDE_FACING

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
        self.direction = RIGHT_FACING
        self.facing_direction = SIDE_FACING
        # TODO: Add textures for player (idle, walk, etc)
        # TODO: Should also work on logic to handle direction facing etc
        # The implementation of these features can be done later on

    # TODO: Should also work on logic to handle direction facing etc
    # The implementation of these features can be done later on

    def attack(self):
        if(self.attack_cooldown > 0):
            return

        self.player_attack = PlayerAttack(
            self.scene,
            self
        )

        self.attack_cooldown = P_ATTACK_COOLDOWN

    def update(self, delta_time):
        if(self.attack_cooldown > 0):
            self.attack_cooldown -= delta_time

        if(self.player_attack != None):
            # pogo :3
            # (on enemy, can easily be expanded by adding other layer to check)
            if arcade.check_for_collision_with_list(
                    self.player_attack,
                    self.scene["Enemy"]
                ) and self.facing_direction == DOWN_FACING:
                    self.change_y = PLAYER_JUMP_SPEED
            self.player_attack.position = self.position
            self.player_attack.update(delta_time)


class PlayerAttack(arcade.Sprite):

    def __init__(self, scene, parent, scale=1.0):
        super().__init__(
            # TODO: Change temp sprite with one of our own
            ":resources:/onscreen_controls/flat_dark/right.png",
            scale=scale
        )

        self.base_scale_x = self.scale_x
        self.base_scale_y = self.scale_y
        self.offset_x = 48
        self.offset_y = -48
        self.parent = parent
        self.scene = scene
        self.remaining_duration = P_ATTACK_COOLDOWN

        self.scene.add_sprite("PlayerAttack", self)

    def update(self, delta_time):
        self.remaining_duration -= delta_time

        self.angle = 90 * self.parent.facing_direction

        if (self.parent.facing_direction == SIDE_FACING):
            self.scale_x = self.base_scale_x * self.parent.direction
            self.center_x = self.parent.center_x + self.offset_x * self.parent.direction
        else:
            self.scale_x = self.base_scale_x
            self.scale_y = self.base_scale_y * -1


        self.center_y = self.parent.center_y + self.offset_y * self.parent.facing_direction

        if(self.parent.facing_direction == DOWN_FACING):
            self.center_y = self.center_y + self.offset_y

        if(self.remaining_duration <= 0):
            self.remove_from_sprite_lists()
            self.parent.player_attack = None

