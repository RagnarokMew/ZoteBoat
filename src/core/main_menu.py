import arcade
import arcade.gui
from arcade.draw import arc

from core.game import GameView
from core.constants import SCREEN_TITLE, SCREEN_WIDTH, SCREEN_HEIGHT

class MenuView(arcade.View):

    def __init__(self):
        super().__init__()

        self.ui_manager = arcade.gui.UIManager()

        play_game_button = arcade.gui.UIFlatButton(text = "Play")
        show_credits_button = arcade.gui.UIFlatButton(text = "Credits")
        leader_board_button = arcade.gui.UIFlatButton(text = "Leaderboard")
        options_button = arcade.gui.UIFlatButton(text = "Options")
        quit_button = arcade.gui.UIFlatButton(text = "Quit")

        self.grid = arcade.gui.UIGridLayout(
            column_count = 1, row_count=5, horizontal_spacing=20, vertical_spacing=20
        )

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

        @leader_board_button.event("on_click")
        def on_click_leaderboard(event):
            leaderboard_menu = LeaderBoard()
            self.ui_manager.add(leaderboard_menu, layer=1)

        @quit_button.event("on_click")
        def on_click_quit(event):
            arcade.exit()

        @play_game_button.event("on_click")
        def on_click_play(event):
            game_view = GameView()
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

        self.ui_manager.draw()

class LeaderBoard(arcade.gui.UIMouseFilterMixin, arcade.gui.UIAnchorLayout):

    def __init__(self):
        super().__init__(size_hint=(1, 1))

        frame = self.add(arcade.gui.UIAnchorLayout(width=1000, height=520, size_hint=None))
        frame.with_padding(all=30)

        frame.with_background(
            color=arcade.color.GHOST_WHITE
        )

        title_label = arcade.gui.UILabel(
            text = "Leaderboard",
            align="center",
            font_size=20,
            multiline=False,
            text_color=arcade.color.BLACK
        )

        widget_layout = arcade.gui.UIGridLayout(
            row_count=3,
            column_count=2,
            horizontal_spacing=167,
            vertical_spacing=25
        )

        back_button = arcade.gui.UIFlatButton(text = "Back")
        back_button.on_click = self.on_click_back_button
        change_button = arcade.gui.UIFlatButton(text = "Change Minigame")
        change_button.on_click = self.on_click_change_button

        # NOTE: Should hold at most 10 values
        player_names = arcade.gui.UILabel(
            text = "placeholder\nplaceholder",
            align="center",
            font_size=15,
            multiline=True,
            text_color=arcade.color.BLACK
        )

        # NOTE: Should hold at most 10 values
        player_scores = arcade.gui.UILabel(
            text = "0\n0",
            align="center",
            font_size=15,
            multiline=True,
            text_color=arcade.color.BLACK
        )

        widget_layout.add(title_label, column_span=2)
        widget_layout.add(player_names, row = 1, column=0)
        widget_layout.add(player_scores, row = 1, column=1)
        widget_layout.add(back_button, row=2)
        widget_layout.add(change_button, row=2, column=1)
        frame.add(child=widget_layout, anchor_x="center_x", anchor_y="top")

    def on_click_back_button(self, event):
        self.parent.remove(self)

    def on_click_change_button(self, event):
        # TODO: Implement changing minigames
        pass

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
