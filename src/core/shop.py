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
        self.active_index = 0
        self.handler = ShopHandler(player_stats)

        self.title = arcade.Text(
            title,
            x=SCREEN_WIDTH // 2,
            y=SCREEN_HEIGHT * 5 // 6 - 6,
            color=arcade.color.WHITE,
            bold=True,
            anchor_x="center",
            font_size=18,
            batch=self.batch
        )

        self.instructions = arcade.Text(
            "Z = Buy, X = Exit, UP/DOWN = Navigation between items",
            x=SCREEN_WIDTH // 2 - SCREEN_WIDTH * 3 // 4 // 2 // 2 + 40,
            y=SCREEN_HEIGHT // 6,
            color=arcade.color.WHITE,
            font_size=12,
            anchor_x="center",
            batch=self.batch
        )

        # NOTE: Below are the Text names of the "scrollable" items

        self.prev_item_text = arcade.Text(
            "ZoteBoat The Biography",
            x = SCREEN_WIDTH // 2 - SCREEN_WIDTH * 3 // 4 // 2 // 2 + 40,
            y = SCREEN_HEIGHT // 2 + SCREEN_HEIGHT * 3 // 4 // 4 + 10,
            color=arcade.color.WHITE,
            font_size=14,
            anchor_y="center",
            anchor_x="center",
            batch=self.batch
        )

        self.active_item_text = arcade.Text(
            "ZoteBoat The Biography",
            x = SCREEN_WIDTH // 2 - SCREEN_WIDTH * 3 // 4 // 2 // 2 + 40,
            y = SCREEN_HEIGHT // 2,
            color=arcade.color.WHITE,
            font_size=18,
            anchor_y="center",
            anchor_x="center",
            batch=self.batch
        )

        self.next_item_text = arcade.Text(
            "ZoteBoat The Biography",
            x = SCREEN_WIDTH // 2 - SCREEN_WIDTH * 3 // 4 // 2 // 2 + 40,
            y = SCREEN_HEIGHT // 2 - SCREEN_HEIGHT * 3 // 4 // 4 - 10,
            color=arcade.color.WHITE,
            font_size=14,
            anchor_y="center",
            anchor_x="center",
            batch=self.batch
        )

        # NOTE: Below are the stats of the active (selected) item

        self.item_name_text = arcade.Text(
            "ZoteBoat The Biography",
            x = SCREEN_WIDTH // 2 + SCREEN_WIDTH * 3 // 4 // 2 // 2 + 20,
            y = SCREEN_HEIGHT * 3 // 4,
            color = arcade.color.WHITE,
            bold = True,
            font_size=16,
            anchor_x="center",
            batch=self.batch
        )

        self.item_desc_text = arcade.Text(
            "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.",
            x = SCREEN_WIDTH // 2 + SCREEN_WIDTH * 3 // 4 // 2 // 2 + 20,
            y = SCREEN_HEIGHT * 3 // 4 - 16 * 3,
            color = arcade.color.WHITE,
            font_size=12,
            italic=True,
            anchor_x="center",
            width=SCREEN_WIDTH * 3 // 4 // 2 - 120 - 12 - 12 - 12,
            multiline=True,
            batch=self.batch
        )

        self.item_price_text = arcade.Text(
            "PRICE: 1500 currency1",
            x = SCREEN_WIDTH // 2 + SCREEN_WIDTH * 3 // 4 // 4 // 2 - 16,
            y = SCREEN_HEIGHT // 4 - 16,
            color = arcade.color.WHITE,
            font_size=16,
            batch=self.batch
        )

        # TODO: go through items and check if player owns it already
        # TODO: Set up Text strings based on shop items and active item

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
            arcade.color.BLUE
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

