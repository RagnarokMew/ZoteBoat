import arcade
from pyglet.graphics import Batch
from core.constants import SCREEN_HEIGHT, SCREEN_WIDTH

class ShopItem:
    def __init__(self, name, id, currency, price, description=""):
        self.display_name = name
        self.id = id
        self.description = description
        self.currency = currency
        self.price = price

class ShopMenu:
    def __init__(self, items, player_stats, title):
        self.batch = Batch()
        self.handler = ShopHandler(player_stats)
        self.items = [ item for item in items if not self.handler.check_owned(item.id) ]
        self.active_index = 0

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
            "",
            x = SCREEN_WIDTH // 2 - SCREEN_WIDTH * 3 // 4 // 2 // 2 + 40,
            y = SCREEN_HEIGHT // 2 + SCREEN_HEIGHT * 3 // 4 // 4 + 10,
            color=arcade.color.WHITE,
            font_size=14,
            anchor_y="center",
            anchor_x="center",
            batch=self.batch
        )

        self.active_item_text = arcade.Text(
            "",
            x = SCREEN_WIDTH // 2 - SCREEN_WIDTH * 3 // 4 // 2 // 2 + 40,
            y = SCREEN_HEIGHT // 2,
            color=arcade.color.WHITE,
            font_size=18,
            anchor_y="center",
            anchor_x="center",
            batch=self.batch
        )

        self.next_item_text = arcade.Text(
            "",
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
            "",
            x = SCREEN_WIDTH // 2 + SCREEN_WIDTH * 3 // 4 // 2 // 2 + 20,
            y = SCREEN_HEIGHT * 3 // 4,
            color = arcade.color.WHITE,
            bold = True,
            font_size=16,
            anchor_x="center",
            batch=self.batch
        )

        self.item_desc_text = arcade.Text(
            "",
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
            "",
            x = SCREEN_WIDTH // 2 + SCREEN_WIDTH * 3 // 4 // 4 // 2 - 16,
            y = SCREEN_HEIGHT // 4 - 16,
            color = arcade.color.WHITE,
            font_size=16,
            batch=self.batch
        )

        if len(self.items) == 0:
            self.items.append(ShopItem(
                name="No more items left...",
                id="Null",
                currency="?",
                price=0,
                description="Wow! You've bought everything my shop had to offer. Thank you so much Zote! I'll make sure to go and deposit all this currency at the nearest bank as soon as possible."
            ))

        self._update_text()

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
            arcade.color.CARIBBEAN_GREEN
        )

        # Prev Item Window
        if self.active_index > 0:
            arcade.draw_rect_filled(
                arcade.rect.XYWH(
                    SCREEN_WIDTH // 2 - SCREEN_WIDTH * 3 // 4 // 2 // 2 + 40,
                    SCREEN_HEIGHT // 2 + SCREEN_HEIGHT * 3 // 4 // 4 + 10,
                    SCREEN_WIDTH * 3 // 4 // 2 - 120,
                    SCREEN_HEIGHT * 3 // 4 // 4 // 1.5
                ),
                arcade.color.AZURE
            )

        # Next Item Window
        if self.active_index < len(self.items) -1:
            arcade.draw_rect_filled(
                arcade.rect.XYWH(
                    SCREEN_WIDTH // 2 - SCREEN_WIDTH * 3 // 4 // 2 // 2 + 40,
                    SCREEN_HEIGHT // 2 - SCREEN_HEIGHT * 3 // 4 // 4 - 10,
                    SCREEN_WIDTH * 3 // 4 // 2 - 120,
                    SCREEN_HEIGHT * 3 // 4 // 4 // 1.5
                ),
                arcade.color.AZURE
            )

        # Active Item Window
        arcade.draw_rect_filled(
            arcade.rect.XYWH(
                SCREEN_WIDTH // 2 + SCREEN_WIDTH * 3 // 4 // 2 // 2 + 20,
                SCREEN_HEIGHT // 2,
                SCREEN_WIDTH * 3 // 4 // 2 - 120,
                SCREEN_HEIGHT * 3 // 4 - 100
            ),
            arcade.color.ANTIQUE_RUBY
        )

        self.batch.draw()

    def next_item(self):
        if self.active_index < len(self.items) - 1:
            self.active_index += 1
            self._update_text()

    def previous_item(self):
        if self.active_index > 0:
            self.active_index -= 1
            self._update_text()

    def purchase(self):
        if self.items[self.active_index].currency == "?":
            return

        if not self.handler.decrease_currency(
            self.items[self.active_index].price,
            self.items[self.active_index].currency
        ):
            return

        self.handler.unlock(self.items[self.active_index].id)

        self.items.pop(self.active_index)

        if len(self.items) == 0:
            self.items.append(ShopItem(
                name="No more items left...",
                id="Null",
                currency="?",
                price=0,
                description="Wow! You've bought everything my shop had to offer. Thank you so much Zote! I'll make sure to go and deposit all this currency at the nearest bank as soon as possible."
            ))
        if self.active_index >= len(self.items):
            self.active_index -= 1

        self._update_text()

    def _update_text(self):
        self.active_item_text.text = self.items[self.active_index].display_name
        self.item_name_text.text = self.items[self.active_index].display_name
        self.item_desc_text.text = self.items[self.active_index].description
        self.item_price_text.text = f"PRICE: {self.items[self.active_index].price} {self.items[self.active_index].currency}"

        if self.active_index > 0:
            self.prev_item_text.text = self.items[self.active_index - 1].display_name
        else:
            self.prev_item_text.text = ""

        if self.active_index < len(self.items) - 1:
            self.next_item_text.text = self.items[self.active_index + 1].display_name
        else:
            self.next_item_text.text = ""

class ShopHandler:
    def __init__(self, player_stats):
        self.stats = player_stats

    # TODO: Find better name for this
    def unlock(self, item):
        """Unlocks a shop item for the player.

        Args:
            item(str): The id of the shop item.

        """
        # TODO: Add unlocks for all features

        unlock_handler = {
            "Mask_1": self.stats.increase_max_hp,
            "Mask_2": self.stats.increase_max_hp,
            "Mask_3": self.stats.increase_max_hp,
            "Mask_4": self.stats.increase_max_hp,
            "Nail_Upgrade_Kit_1": self.stats.increase_damage,
            "Nail_Upgrade_Kit_2": self.stats.increase_damage,
            "Wall_Jump": self.stats.mark_unlocked,
            "Double_Jump": self.stats.mark_unlocked,
            "Dash": self.stats.mark_unlocked
        }

        unlock_value = {
            "Mask_1": 1,
            "Mask_2": 1,
            "Mask_3": 1,
            "Mask_4": 1,
            "Nail_Upgrade_Kit_1": 2,
            "Nail_Upgrade_Kit_2": 2,
            "Wall_Jump": True,
            "Double_Jump": True,
            "Dash": True
        }

        try:
            # TODO: Fix duplicate logic
            # currently the duplicate is needed because some unlocks increase
            # stats while some don't but all need to be marked as unlocked.
            unlock_handler[item](unlock_value[item])
            self.stats.unlocks[item] = True
        except: pass

    def check_owned(self, item):
        """Checks if an item from the shop is already owned by the player.

        Args:
            item(str): The id of the shop item.

        Returns:
            bool: True if the item is owned, False if not.

        """

        try:
            return self.stats.unlocks[item]
        except:
            return False

    def decrease_currency(self, amount, currency):
        """Decreases an amount of currency from the player.

        Tries to decrease currency from the player without going into negatives.

        Args:
            amount(int): The amount of currency to be decreased.
            currency(str): Which currency to be decreased.

        Returns:
            bool: True if the currency was decreased, False if not.

        """

        if currency == "currency1":
            if self.stats.currency_1 < amount:
                return False
            self.stats.currency_1 -= amount

        elif currency == "currency2":
            if self.stats.currency_2 < amount:
                return False
            self.stats.currency_2 -= amount

        elif currency == "currency3":
            if self.stats.currency_3 < amount:
                return False
            self.stats.currency_3 -= amount

        elif currency == "currency4":
            if self.stats.currency_4 < amount:
                return False
            self.stats.currency_4 -= amount

        else:
            return False

        return True
