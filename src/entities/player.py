import arcade

class PlayerSprite(arcade.Sprite):

    def __init__(self, position=(0, 0), scale=1.0):
        # TODO: Change temp asset to one of our own towards the end of development
        super().__init__(
            ":resources:images/animated_characters/robot/robot_idle.png",
            scale=scale
        )

        self.center_x, self.center_y = position

        # TODO: Add textures for player (idle, walk, etc)
        # TODO: Should also work on logic to handle direction facing etc
        # The implementation of these features can be done later on

    # TODO: Should also work on logic to handle direction facing etc
    # The implementation of these features can be done later on


