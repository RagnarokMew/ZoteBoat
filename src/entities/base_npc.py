import arcade
from pyglet.graphics import Batch
from core.constants import GRAVITY, SCREEN_HEIGHT, SCREEN_WIDTH, P_DIALOGUE, P_SHOP

class BaseNpc(arcade.Sprite):
    def __init__(
        self, scene, id = "default", sprite_path = "../assets/sprites/npc/flav0_guide.png",
        alt_sprite = None, anim = False, position = (128, 128), scale = 1,
        name = "NPC", title = "Title", has_shop = False, has_game = False, game_map = None
    ):
        super().__init__(
            sprite_path,
            scale=scale
        )

        self.id = id
        self.scene = scene
        self.name = name
        self.title = title

        self.has_shop = has_shop
        self.has_game = has_game
        self.game_map = game_map

        self.anim = anim
        self.active = False
        try:
            self.sprites = [self.texture, arcade.load_texture(alt_sprite)]
            self.anim_timer = 0
            self.anim_frame = 0
            self.has_alt = True
        except:
            self.has_alt = False

        self.center_x, self.center_y = position
        self.physics_engine = arcade.PhysicsEnginePlatformer(
            self, scene["Platforms"], GRAVITY
        )

    def update(self, delta_time, curr_state):
        self.physics_engine.update()

        if self.has_alt:
            if self.anim:
                self.anim_timer += delta_time
                if self.anim_timer * 1000 >= 200:
                    self.anim_timer = 0
                    self.anim_frame = 1 - self.anim_frame
                    self.texture = self.sprites[self.anim_frame]
            elif self.active and (curr_state == P_DIALOGUE or curr_state == P_SHOP):
                self.texture = self.sprites[1]
            else:
                self.texture = self.sprites[0]
    
    def set_active(self, who = None):
        self.active = (who == self)

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

