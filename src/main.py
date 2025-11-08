import arcade
from core.constants import SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE
from core import game

def main():
    window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    start_view = game.GameView()
    start_view.setup(0)
    window.show_view(start_view)
    arcade.run()

if __name__ == "__main__":
    main()
