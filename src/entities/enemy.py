import arcade

class EnemySprite(arcade.Sprite):
    
    def __init__(self, scene, position = (0, 0), scale = 1.0):
        super().__init__(
            ":resources:/images/animated_characters/zombie/zombie_idle.png",
            scale = scale
        )

        self.scene = scene
        self.center_x, self.center_y = position