import arcade
from core.constants import GRAVITY, SCREEN_HEIGHT, SCREEN_WIDTH

class BaseNpc(arcade.Sprite):
    def __init__(self, scene, sprite_path, position=(128, 128), scale=1):
        super().__init__(
            sprite_path,
            scale=scale
        )

        self.scene = scene
        self.center_x, self.center_y = position
        self.menu = None
        self.physics_engine = arcade.PhysicsEnginePlatformer(
            self, scene["Platforms"], GRAVITY
        )

    def add_menu(self, Menu):
        self.menu = Menu
        self.scene.add_sprite("box", self.menu)

    def draw(self):
        if self.menu:
            self.menu.draw()

    def update(self, delta_time):
        self.physics_engine.update()

class DialogueMenu():
    def __init__(self,
                 content=["This is a dialogue text", "Another text"]
                 ):
        self.content = content
        self.text = None
        self.text_index = 0

        self.next()

    def next(self):
        try:
            self.text = arcade.Text(
                self.content[self.text_index],
                x=SCREEN_WIDTH // 6 + 24,
                y=SCREEN_HEIGHT * 5 // 6 + 36,
                color=arcade.color.WHITE,
                font_size=14,
                width=SCREEN_WIDTH * 2 // 3 - 48,
                align="left",
                multiline=True
            )
            self.text_index += 1
            return True
        except:
            self.text = "Exception"
            return False

    def draw(self):
        arcade.draw_rect_filled(
            arcade.rect.XYWH(SCREEN_WIDTH // 2, SCREEN_HEIGHT * 4 // 5, SCREEN_WIDTH * 2 // 3, SCREEN_HEIGHT // 4),
            arcade.color.BLACK
        )
        self.text.draw()

