from typing import override
import arcade
from arcade.draw import arc
import arcade.gui

from core.constants import SCREEN_TITLE, SCREEN_WIDTH, SCREEN_HEIGHT

class MenuView(arcade.View):

    def __init__(self):
        super().__init__()

        self.ui_manager = arcade.gui.UIManager()

        play_game_button = arcade.gui.UIFlatButton(text = "Play")
        show_credits_button = arcade.gui.UIFlatButton(text = "Credits")
        options_button = arcade.gui.UIFlatButton(text = "Options")
        quit_button = arcade.gui.UIFlatButton(text = "Quit")

        self.grid = arcade.gui.UIGridLayout(
            column_count = 1, row_count=4, horizontal_spacing=20, vertical_spacing=20
        )

        self.grid.add(play_game_button, row = 0)
        self.grid.add(show_credits_button, row = 1)
        self.grid.add(options_button, row = 2)
        self.grid.add(quit_button, row = 3)

        self.anchor = self.ui_manager.add(arcade.gui.UIAnchorLayout())

        self.anchor.add(
            anchor_x="left",
            align_x=20,
            anchor_y="center",
            child=self.grid
        )


    def on_show_view(self):
        arcade.set_background_color(arcade.color.BLUE_BELL)

        self.ui_manager.enable()

    def on_hide_view(self):
        self.ui_manager.disable()

    def on_draw(self):
        self.clear()

        self.ui_manager.draw()

