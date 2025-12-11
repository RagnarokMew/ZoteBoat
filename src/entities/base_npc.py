import arcade
from pyglet.graphics import Batch
from core.constants import GRAVITY, SCREEN_HEIGHT, SCREEN_WIDTH

class BaseNpc(arcade.Sprite):
    def __init__(self, scene, id,
            sprite_path = ":resources:/images/animated_characters/male_person/malePerson_idle.png",
            position = (128, 128), scale = 1, name = "NPC", title = "Title",
            has_shop = False, has_game = False, game_map = None
        ):
        super().__init__(
            sprite_path,
            scale = scale
        )

        self.id = id
        self.name = name
        self.title = title
        self.has_shop = has_shop
        self.has_game = has_game
        self.game_map = game_map
        self.scene = scene
        self.center_x, self.center_y = position
        self.physics_engine = arcade.PhysicsEnginePlatformer(
            self, scene["Platforms"], GRAVITY
        )

    def update(self, delta_time):
        self.physics_engine.update()

class DialogueMenu():
    def __init__(self, id,
            content = ["This is a dialogue text", "Another text"],
            npc_name = "NPC_NAME", npc_title = "NPC_TITLE",
            before_shop_interaction = False, before_game = False, game_map = None
        ):
        self.npc_id = id
        self.npc_name = npc_name
        self.before_shop_interation = before_shop_interaction
        self.before_game = before_game
        self.game_map = game_map
        self.game_quit = False
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

        self.next(stats = None)

    def next(self, stats):
        try:
            next_text = self.content[self.text_index]

            if stats is not None:                
                next_text = next_text.replace("ARENA_SCORE_CHECK",
                "NEW_HI_TEXT Your current score is ARENA_KILL_CUR kills in ARENA_TIME_CUR seconds, and your best is ARENA_KILL_HI in ARENA_TIME_HI."
                if stats.arena_hiscore["kill"] != -1 else
                "You liar! You've never even stepped foot in that arena, have you? Come back when you're a little, mmm... braver!")

                next_text = next_text.replace("PARKOUR_SCORE_CHECK",
                "NEW_HI_TEXT Your last attempt was PARKOUR_TIME_CUR, while your best run was PARKOUR_TIME_HI."
                if stats.parkour_hiscore["hrs"] != -1 else
                "Hey, listen! You almost tricked me there, but I know you haven't actually been in the cave. Don't worry though, your secret's safe with me! Return whenever you decide to give my challenge a go!")

                next_text = next_text.replace("NEW_HI_TEXT",
                "Wow, that's even better than before!" if stats.parkour_break or stats.arena_break
                else "Well, you've had a great performance, but maybe you could do better next time.")

                kill_cur = stats.arena_score["kill"]
                time_cur = stats.arena_score["time"]
                kill_hi = stats.arena_hiscore["kill"]
                time_hi = stats.arena_hiscore["time"]

                next_text = next_text.replace("ARENA_KILL_CUR", f"{kill_cur}")
                next_text = next_text.replace("ARENA_TIME_CUR", f"{time_cur}")
                next_text = next_text.replace("ARENA_KILL_HI", f"{kill_hi}")
                next_text = next_text.replace("ARENA_TIME_HI", f"{time_hi}")

                hrs_cur = stats.parkour_score["hrs"]
                min_cur = stats.parkour_score["min"]
                sec_cur = stats.parkour_score["sec"]
                hrs_hi = stats.parkour_hiscore["hrs"]
                min_hi = stats.parkour_hiscore["min"]
                sec_hi = stats.parkour_hiscore["min"]

                next_text = next_text.replace("PARKOUR_TIME_HI", f"{hrs_hi}:{min_hi}:{sec_hi}")
                next_text = next_text.replace("PARKOUR_TIME_CUR", f"{hrs_cur}:{min_cur}:{sec_cur}")

            self.text = arcade.Text(
                next_text,
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

    def bye(self, accept):
        if not self.game_quit:
            self.game_quit = True
            self.game_accept = accept

            self.text = arcade.Text(
                "Great! I'll get you there right away." if accept else
                "Alright then, good luck on your adventures.",
                x=SCREEN_WIDTH // 6 + 24,
                y=SCREEN_HEIGHT * 5 // 6 + 36,
                color=arcade.color.WHITE,
                font_size=14,
                width=SCREEN_WIDTH * 2 // 3 - 48,
                align="left",
                multiline=True,
                batch=self.batch
            )

            return (False, False)
    
        else:
            return (True, self.game_accept)

    def draw(self):
        arcade.draw_rect_filled(
            arcade.rect.XYWH(SCREEN_WIDTH // 2, SCREEN_HEIGHT * 4 // 5, SCREEN_WIDTH * 2 // 3, SCREEN_HEIGHT // 4),
            arcade.color.BLACK
        )

        self.batch.draw()

