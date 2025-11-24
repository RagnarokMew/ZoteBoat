import arcade
from pyglet.graphics import Batch
from core.constants import SCREEN_HEIGHT, SCREEN_WIDTH

class ShopItem:
    def __init__(self, name, currency, price, description=""):
        self.name = name
        self.description = description
        self.currency = currency
        self.price = price

class ShopMenu:
    def __init__(self, items, player_stats, title):
        self.batch = Batch()
        self.items = items
        self.title = arcade.Text(
            title,
            x=SCREEN_WIDTH // 2 - len(title) * 9, # Hardcooded centering the text
            y=SCREEN_HEIGHT * 5 // 6 - 6,
            color=arcade.color.WHITE,
            align="left",
            bold=True,
            font_size=18,
            batch=self.batch
        )
        self.handler = ShopHandler(player_stats)

        # TODO: go through items and check if player owns it already

    def draw(self):
        # Main Shop Window
        arcade.draw_rect_filled(
            arcade.rect.XYWH(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, SCREEN_WIDTH * 3 // 4, SCREEN_HEIGHT * 3 // 4 ),
            arcade.color.BLACK
        )

        # Active Item Window
        arcade.draw_rect_filled(
            arcade.rect.XYWH(
                SCREEN_WIDTH // 2 - SCREEN_WIDTH * 3 // 4 // 2 // 2 + 40,
                SCREEN_HEIGHT // 2,
                SCREEN_WIDTH * 3 // 4 // 2 - 20,
                SCREEN_HEIGHT * 3 // 4 // 4
            ),
            arcade.color.GRAY
        )

        # Prev Item Window
        arcade.draw_rect_filled(
            arcade.rect.XYWH(
                SCREEN_WIDTH // 2 - SCREEN_WIDTH * 3 // 4 // 2 // 2 + 40,
                SCREEN_HEIGHT // 2 + SCREEN_HEIGHT * 3 // 4 // 4 + 10,
                SCREEN_WIDTH * 3 // 4 // 2 - 120,
                SCREEN_HEIGHT * 3 // 4 // 4 // 1.5
            ),
            arcade.color.BLUE
        )

        # Next Item Window
        arcade.draw_rect_filled(
            arcade.rect.XYWH(
                SCREEN_WIDTH // 2 - SCREEN_WIDTH * 3 // 4 // 2 // 2 + 40,
                SCREEN_HEIGHT // 2 - SCREEN_HEIGHT * 3 // 4 // 4 - 10,
                SCREEN_WIDTH * 3 // 4 // 2 - 120,
                SCREEN_HEIGHT * 3 // 4 // 4 // 1.5
            ),
            arcade.color.GREEN
        )

        # Active Item Window
        arcade.draw_rect_filled(
            arcade.rect.XYWH(
                SCREEN_WIDTH // 2 + SCREEN_WIDTH * 3 // 4 // 2 // 2 + 20,
                SCREEN_HEIGHT // 2,
                SCREEN_WIDTH * 3 // 4 // 2 - 120,
                SCREEN_HEIGHT * 3 // 4 - 100
            ),
            arcade.color.RED
        )

        self.batch.draw()


class ShopHandler:
    def __init__(self, player_stats):
        self.stats = player_stats

    # TODO: Find better name for this
    def do(self, action):
        pass

    def check_owned(self, item):
        pass

