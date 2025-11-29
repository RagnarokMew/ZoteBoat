import arcade
from entities.base_npc import BaseNpc
from core.shop import ShopItem
import json

def load_spawn(id):
    try:
        with open("../assets/data/maps.json", "r") as file:
            data = json.load(file)

        # TODO: possibly remove trans_x altogether
        # this would make data[id]["speed"] a single element
        # which can be placed directly in the returned tuple
        (trans_x, trans_y) = data[id]["speed"]

        return (data[id]["spawn"], trans_y)

    except Exception as e:
        print(f"\033[91mCould not load next room:\033[93m {e}\033[0m")
        return []