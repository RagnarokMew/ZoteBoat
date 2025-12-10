import arcade
from pyglet.graphics import Batch
from core.constants import GRAVITY, SCREEN_HEIGHT, SCREEN_WIDTH

class BaseNpc(arcade.Sprite):
    def __init__(self, scene, id, sprite_path=":resources:/images/animated_characters/male_person/malePerson_idle.png", position=(128, 128), scale=1, name="NPC", title="Title", has_shop=False):
        super().__init__(
            sprite_path,
            scale=scale
        )

        self.id = id
        self.name = name
        self.title = title
        self.has_shop = has_shop
        self.scene = scene
        self.center_x, self.center_y = position
        self.physics_engine = arcade.PhysicsEnginePlatformer(
            self, scene["Platforms"], GRAVITY
        )

    def update(self, delta_time):
        self.physics_engine.update()

class DialogueMenu():
    def __init__(self,
                 id,
                 content=["This is a dialogue text", "Another text"],
                 npc_name="NPC_NAME",
                 npc_title="NPC_TITLE",
                 before_shop_interaction=False
                 ):
        self.npc_id = id
        self.npc_name = npc_name
        self.before_shop_interation = before_shop_interaction
        self.content = content
        self.text = None
        self.text_index = 0

        # NOTE: Due to the amount of text that needs to be rendered here I've 
        # decided to batch it in case it improves performance (at the cost of 
        # a little RAM)
        self.batch = Batch()
        outlines = [
            (0, 2),
            (2, 0),
            (-2, 0),
            (0, -2),
            (2, 2),
            (-2, -2),
            (2, -2),
            (-2, 2)
        ]

        self.npc_text_shadow = list()
        for outline in outlines:
            self.npc_text_shadow.append(arcade.Text(
                npc_name,
                x=100 + outline[0],
                y=100 + outline[1],
                color=arcade.color.BLACK,
                align="left",
                bold=True,
                font_size=32,
                batch=self.batch
            ))

        self.npc_name_text = arcade.Text(
            npc_name,
            x=100,
            y=100,
            color=arcade.color.WHITE,
            align="left",
            bold=True,
            font_size=32,
            batch=self.batch
        )

        for outline in outlines:
            self.npc_text_shadow.append(arcade.Text(
                npc_title,
                x=100 + outline[0],
                y=50 + outline[1],
                color=arcade.color.BLACK,
                align="left",
                bold=True,
                italic=True,
                font_size=28,
                batch=self.batch
            ))


        self.npc_title_text = arcade.Text(
            npc_title,
            x=100,
            y=50,
            color=arcade.color.WHITE,
            align="center",
            bold=True,
            italic=True,
            font_size=28,
            batch=self.batch
        )

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
                multiline=True,
                batch=self.batch
            )
            self.text_index += 1
            return True
        except:
            self.text = "Ok, bye"
            return False

    def draw(self):
        arcade.draw_rect_filled(
            arcade.rect.XYWH(SCREEN_WIDTH // 2, SCREEN_HEIGHT * 4 // 5, SCREEN_WIDTH * 2 // 3, SCREEN_HEIGHT // 4),
            arcade.color.BLACK
        )

        self.batch.draw()

