import arcade
import arcade.gui
from arcade.draw import arc
import json

from core.constants import SCREEN_TITLE, SCREEN_WIDTH, SCREEN_HEIGHT

class MenuView(arcade.View):

    def __init__(self, options = None):
        super().__init__()

        self.ui_manager = arcade.gui.UIManager()

        play_game_button = arcade.gui.UIFlatButton(text = "Play", width=200)
        show_credits_button = arcade.gui.UIFlatButton(text = "Credits", width=200)
        leader_board_button = arcade.gui.UIFlatButton(text = "Leaderboard", width = 200)
        options_button = arcade.gui.UIFlatButton(text = "Options", width=200)
        quit_button = arcade.gui.UIFlatButton(text = "Quit", width=200)

        self.grid = arcade.gui.UIGridLayout(
            column_count = 1, row_count=5, horizontal_spacing=20, vertical_spacing=20
        )

        self.background = arcade.load_texture("../assets/bg/menu.jpg")

        self.grid.add(play_game_button, row = 0)
        self.grid.add(leader_board_button, row = 1)
        self.grid.add(show_credits_button, row = 2)
        self.grid.add(options_button, row = 3)
        self.grid.add(quit_button, row = 4)

        self.anchor = self.ui_manager.add(arcade.gui.UIAnchorLayout())

        self.anchor.add(
            anchor_x="left",
            align_x=20,
            anchor_y="center",
            child=self.grid
        )

        if options == None:
            self.options = {
                "username": "default",
                "show_enemy_hp": False
            }
        else:
            self.options = options

        @options_button.event("on_click")
        def on_click_options(event):
            options_menu = OptionsMenu(self.options)
            self.ui_manager.add(options_menu, layer=1)

        @leader_board_button.event("on_click")
        def on_click_leaderboard(event):
            leaderboard_menu = LeaderBoard()
            self.ui_manager.add(leaderboard_menu, layer=1)

        @quit_button.event("on_click")
        def on_click_quit(event):
            arcade.exit()

        @play_game_button.event("on_click")
        def on_click_play(event):
            from core.game import GameView

            game_view = GameView(self.options)
            game_view.setup()
            self.window.show_view(game_view)

        @show_credits_button.event("on_click")
        def on_click_credits(event):
            credits_menu = CreditsMenu()
            self.ui_manager.add(credits_menu, layer = 1)

    def on_show_view(self):
        arcade.set_background_color(arcade.color.BLUE_BELL)

        self.ui_manager.enable()

    def on_hide_view(self):
        self.ui_manager.disable()

    def on_draw(self):
        self.clear()

        arcade.draw_texture_rect(
            self.background,
            arcade.LBWH(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT)
        )

        self.ui_manager.draw()

class OptionsMenu(arcade.gui.UIMouseFilterMixin, arcade.gui.UIAnchorLayout):

    def __init__(self, options):
        super().__init__(size_hint=(1, 1))

        on_texture = arcade.load_texture(
            ":resources:gui_basic_assets/simple_checkbox/circle_on.png"
        )
        off_texture = arcade.load_texture(
            ":resources:gui_basic_assets/simple_checkbox/circle_off.png"
        )

        frame = self.add(arcade.gui.UIAnchorLayout(width=1000, height=520, size_hint=None))
        frame.with_padding(all=30)

        frame.with_background(
            color=arcade.color.GRAY
        )

        back_button = arcade.gui.UIFlatButton(text = "Back", width=200)
        back_button.on_click = self.on_click_back_button

        self.options = options

        title_label = arcade.gui.UILabel(
            text="Options",
            text_color=arcade.color.BLACK,
            font_size=20
        )

        username_label = arcade.gui.UILabel(
            text="Username: ",
            text_color=arcade.color.BLACK,
            font_size=15
        )
        show_enemy_hp_label = arcade.gui.UILabel(
            text = "Show Enemy Hp",
            text_color=arcade.color.BLACK,
            font_size=15
        )

        self.show_enemy_hp = arcade.gui.UITextureToggle(
            on_texture=on_texture,
            off_texture=off_texture,
            width=25,
            height=25,
            value=self.options["show_enemy_hp"]
        )


        input_style = arcade.gui.widgets.text.UIInputTextStyle(
            arcade.color.GHOST_WHITE,
            arcade.color.BLACK
        )

        dict_style = {
            "disabled": input_style,
            "invalid": input_style,
            "hover": input_style,
            "normal": input_style,
            "press": input_style
        }

        self.username = arcade.gui.UIInputText(
            text = self.options["username"],
            text_color=arcade.color.BLACK,
            align = "center",
            multiline=False,
            width=200,
            style = dict_style,
            caret_color=arcade.color.BLACK
        )

        widget_layout = arcade.gui.UIGridLayout(
            row_count=4,
            column_count=3,
            vertical_spacing=25,
            horizontal_spacing=25
        )

        widget_layout.add(title_label, column_span=3)
        widget_layout.add(username_label, row = 1)
        widget_layout.add(self.username, row = 1, column=1, column_span=2)
        widget_layout.add(show_enemy_hp_label, row = 2)
        widget_layout.add(self.show_enemy_hp, row = 2, column=1)
        widget_layout.add(back_button, row = 3, column_span=3)

        frame.add(
            child=widget_layout,
            anchor_x="center_x",
            anchor_y="center_y"
        )

    def on_click_back_button(self, event):
        self.parent.remove(self)

        self.options["username"] = self.username.text
        self.options["show_enemy_hp"] = self.show_enemy_hp.value

class LeaderBoard(arcade.gui.UIMouseFilterMixin, arcade.gui.UIAnchorLayout):

    def __init__(self):
        super().__init__(size_hint=(1, 1))

        self.setup()

        frame = self.add(arcade.gui.UIAnchorLayout(width=1000, height=520, size_hint=None))
        frame.with_padding(all=30)

        frame.with_background(
            color=arcade.color.GHOST_WHITE
        )

        self.minigame = [ "Arena", "Parkour" ]
        self.active_index = 0

        title_label = arcade.gui.UILabel(
            text = "Leaderboard",
            align="center",
            font_size=20,
            multiline=False,
            text_color=arcade.color.BLACK
        )

        self.minigame_label = arcade.gui.UILabel(
            text = self.minigame[self.active_index],
            align="center",
            font_size=18,
            multiline=False,
            text_color=arcade.color.BLACK
        )

        self.widget_layout = arcade.gui.UIGridLayout(
            row_count=4,
            column_count=2,
            horizontal_spacing=167,
            vertical_spacing=25
        )

        back_button = arcade.gui.UIFlatButton(text = "Back", width=200)
        back_button.on_click = self.on_click_back_button
        change_button = arcade.gui.UIFlatButton(text = "Change Minigame", width=200)
        change_button.on_click = self.on_click_change_button

        # NOTE: Should hold at most 10 values
        self.player_names = arcade.gui.UILabel(
            text = self.arena_names,
            align="center",
            font_size=15,
            multiline=True,
            text_color=arcade.color.BLACK
        )

        # NOTE: Should hold at most 10 values
        self.player_scores = arcade.gui.UILabel(
            text = self.arena_scores,
            align="center",
            font_size=15,
            multiline=True,
            text_color=arcade.color.BLACK
        )

        self.widget_layout.add(title_label, column_span=2)
        self.widget_layout.add(self.minigame_label, row=1, column_span=2)
        self.widget_layout.add(self.player_names, row = 2, column=0)
        self.widget_layout.add(self.player_scores, row = 2, column=1)
        self.widget_layout.add(back_button, row=3)
        self.widget_layout.add(change_button, row=3, column=1)
        frame.add(child=self.widget_layout, anchor_x="center_x", anchor_y="top")

    def on_click_back_button(self, event):
        self.parent.remove(self)

    def on_click_change_button(self, event):
        self.active_index = (self.active_index + 1) % 2

        self.minigame_label.text = self.minigame[self.active_index]

        if (self.active_index == 0):
            self.player_names.text = self.arena_names
            self.player_scores.text = self.arena_scores
        else:
            self.player_names.text = self.parkour_names
            self.player_scores.text = self.parkour_scores

        self.player_scores.fit_content()
        self.widget_layout.do_layout()

    def setup(self):
        try:
            with open("../saves/scores.json") as file:
                data = json.load(file)

            arena_list = []
            parkour_list = []

            for user in data:
                arena_list.append([user, data[user]["arena"]])
                parkour_list.append([user, data[user]["parkour"]])

            try:
                arena_list.sort(key = lambda val: (-val[1][0], val[1][1]))
                arena_list = arena_list[:10]

                arena_names_list = []
                arena_scores_list = []

                for scores in arena_list:
                    if scores[1][0] != -1:
                        arena_names_list.append(scores[0])
                        arena_scores_list.append(f"{scores[1][0]} kills, {scores[1][1]}s")

                self.arena_names = "\n".join(arena_names_list)
                self.arena_scores = "\n".join(arena_scores_list)

            except Exception as e:
                self.arena_names = ""
                self.arena_score = ""
                print(f"Exception loading arena scores: {e}")

            try:
                parkour_list.sort(key = lambda val: (val[1][0], val[1][1]))
                parkour_list = parkour_list[:10]

                names_list = []
                scores_list = []

                for scores in parkour_list:
                    if scores[1][0] != -1:
                        names_list.append(scores[0])
                        scores_list.append(f"{scores[1][0]}min {scores[1][1]}s")

                self.parkour_names = "\n".join(names_list)
                self.parkour_scores = "\n".join(scores_list)

            except Exception as e:
                self.parkour_names = ""
                self.parkour_scores = ""
                print(f"Exception loading parkour scores: {e}")

        except Exception as e:
            self.arena_names = ""
            self.arena_scores = ""
            self.parkour_names = ""
            self.parkour_scores = ""
            print(f"Exception loading user scores: {e}")

class CreditsMenu(arcade.gui.UIMouseFilterMixin, arcade.gui.UIAnchorLayout):

    def __init__(self):
        super().__init__(size_hint=(1, 1))

        frame = self.add(arcade.gui.UIAnchorLayout(width = 1000, height=520, size_hint=None))
        frame.with_padding(all=30)

        frame.with_background(
            color=arcade.color.GHOST_WHITE
        )

        title_label = arcade.gui.UILabel(
            text="Credits",
            align="center",
            font_size=20,
            multiline=False,
            text_color=arcade.color.BLACK
        )

        lead_dev_label = arcade.gui.UILabel(
            text="Lead Developer:",
            align="left",
            font_size=16,
            multiline=False,
            text_color=arcade.color.BLACK
        )

        lead_dev_value = arcade.gui.UILabel(
            text = "RagnarokMew (Stefan Simion)",
            align="right",
            font_size=16,
            multiline=False,
            text_color=arcade.color.BLACK
        ) 

        dev_label = arcade.gui.UILabel(
            text="Developer:",
            align="left",
            font_size=16,
            multiline=False,
            text_color=arcade.color.BLACK
        )

        dev_value = arcade.gui.UILabel(
            text="Luxaks (Lucas Ciuca)",
            align="left",
            font_size=16,
            multiline=False,
            text_color=arcade.color.BLACK
        )

        enemy_sprites_label = arcade.gui.UILabel(
            text="Enemy & Attack Sprites:",
            align="left",
            font_size=16,
            multiline= False,
            text_color=arcade.color.BLACK
        )

        enemy_sprites_value = arcade.gui.UILabel(
            text="All assets have been extracted from the\noriginal gamefiles of Hollow Knight.\nAll rights belong to Team Cherry.",
            align="left",
            font_size=16,
            multiline= True,
            text_color=arcade.color.BLACK
        )

        player_sprites_label = arcade.gui.UILabel(
            text="Player Character Sprites:",
            align="left",
            font_size=16,
            multiline=False,
            text_color=arcade.color.BLACK
        )

        player_sprites_value = arcade.gui.UILabel(
            text="All assets have been extracted from the\nskin Atlas created by DFTz. All rights\nbelong to DFTz.",
            align="left",
            font_size=16,
            multiline=True,
            text_color=arcade.color.BLACK
        )

        back_button = arcade.gui.UIFlatButton(text = "Back")
        back_button.on_click = self.on_click_back_button

        widget_layout = arcade.gui.UIGridLayout(
            row_count=6,
            column_count=2,
            horizontal_spacing=167,
            vertical_spacing=25
        )

        widget_layout.add(title_label, row=0, column_span=2)
        widget_layout.add(lead_dev_label, row=1, column_span=1)
        widget_layout.add(lead_dev_value, row=1, column=1, column_span=1)
        widget_layout.add(dev_label, row=2, column_span=1)
        widget_layout.add(dev_value, row=2, column=1, column_span=1)
        widget_layout.add(enemy_sprites_label, row=3, column_span=1)
        widget_layout.add(enemy_sprites_value, row=3, column=1, column_span=1)
        widget_layout.add(player_sprites_label, row=4, column_span=1)
        widget_layout.add(player_sprites_value, row=4, column=1, column_span=1)
        widget_layout.add(back_button, row=5, column_span=2)

        frame.add(child=widget_layout, anchor_x="center_x", anchor_y="top")

    def on_click_back_button(self, event):
        self.parent.remove(self)
