import arcade
from entities.base_npc import BaseNpc
from core.shop import ShopItem
import json

def load_npc(id, scene, position):
    try:
        base_path = "../assets/sprites/"
        with open("../assets/data/npcs.json", "r") as file:
            data = json.load(file)

        npc = BaseNpc(
            scene = scene,
            id = id,
            sprite_path = f"{base_path}{data[id]["sprite_path"]}",
            position = position,
            scale = data[id]["scale"],
            name = data[id]["name"],
            title = data[id]["title"],
            has_shop = data[id]["has_shop"],
            )
    except Exception as e:
        npc = BaseNpc(scene)
        print(f"Error Load Npc: {e}")
    finally:
        scene.add_sprite("NPC", npc)
        print(position)

def load_dialogue(id):
    try:
        with open("../assets/data/dialogue.json", "r") as file:
            data = json.load(file)

        return data[id]
    except Exception as e:
        print(f"Error Load Dialogue: {e}")
        return ["Sorry, I got nothing to say."]

def load_shop_items(id):
    try:
        with open("../assets/data/shops.json", "r") as shop_file:
            item_ids = json.load(shop_file)
            item_ids = item_ids[id]

        with open("../assets/data/items.json", "r") as items_file:
            data = json.load(items_file)

        items = []

        for id in item_ids:
            items.append(ShopItem(
                id=id,
                name=data[id]["display_name"],
                currency=data[id]["currency"],
                price=data[id]["price"],
                description=data[id]["description"]
            ))
    except Exception as e:
        print(f"Error Load Shop Items: {e}")
        items = [ShopItem(
            name="No more items left...",
            id="Null",
            currency="?",
            price=0,
            description="Wow! You've bought everything my shop had to offer. Thank you so much Zote! I'll make sure to go and deposit all this currency at the nearest bank as soon as possible."
        )]
    finally:
        return items
