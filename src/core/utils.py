import arcade
from entities.base_npc import BaseNpc
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
        print(f"{e}")
    finally:
        scene.add_sprite("NPC", npc)
        print(position)

def load_dialogue(id):
    try:
        with open("../assets/data/dialogue.json", "r") as file:
            data = json.load(file)

        print(data[id])
        return data[id]
    except Exception as e:
        print(f"{e}")
        return ["Sorry, I got nothing to say."]

