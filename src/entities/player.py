import arcade

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
            self.position
        )

        self.attack_cooldown = 0.5

    def update(self, delta_time):
        if(self.attack_cooldown > 0):
            self.attack_cooldown -= delta_time

        if(self.player_attack != None):
            self.player_attack.update(delta_time)


class PlayerAttack(arcade.Sprite):

    def __init__(self, scene, position, scale=1.0, damage=1):
        super().__init__(
            ":resources:/images/tiles/lockRed.png",
            scale=scale
        )

        self.scene = scene
        self.center_x, self.center_y = position
        self.damage = damage
        self.remaining_duration = 0.5

        self.scene.add_sprite("PlayerAttack", self)

    def update(self, delta_time):
        # TODO: Update position based on Player
        self.remaining_duration -= delta_time

        if(self.remaining_duration <= 0):
            self.remove_from_sprite_lists()

