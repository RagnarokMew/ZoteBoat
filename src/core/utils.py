import arcade
from entities.base_npc import BaseNpc
from entities.base_enemies import GroundEnemy, FlyingEnemy, BaseEnemy
from entities.enemies import IdleGround, IdleFlying, ChaserGround, ChaserFlying
from core.shop import ShopItem
from core.constants import DEFAULT_BG, OP_LOAD_DT, OP_SAVE_DT, OP_LOAD_SC, OP_SAVE_SC
import json

def load_spawn(id):
    try:
        with open("../assets/data/maps.json", "r") as file:
            data = json.load(file)

        return (data[id]["spawn"], data[id]["spawn"])

    except Exception as e:
        print(f"\033[91mCould not load next room:\033[93m {e}\033[0m")
        return []

def load_bg(id, curr_bg):
    base_path = "../assets/bg/"
    if curr_bg is None:
        curr_bg = arcade.load_texture(f"{base_path}{DEFAULT_BG}")
    
    try:
        with open("../assets/data/maps.json", "r") as file:
            new_bg = json.load(file)[id]["bg"]
        
        curr_bg = arcade.load_texture(f"{base_path}{new_bg}")
    
    # we expect this to fail often, since not all maps have a bg, so no error handling is needed
    except: pass
    
    return curr_bg

def load_npc(id, scene, position):
    try:
        base_path = "../assets/sprites/npc/"
        with open("../assets/data/npcs.json", "r") as file:
            data = json.load(file)

        npc = BaseNpc(
            scene = scene,
            id = id,
            sprite_path = f"{base_path}{data[id]["sprite_path"]}",
            alt_sprite = f"{base_path}{data[id]["alt_sprite"]}",
            anim = data[id]["anim"],
            position = position,
            scale = data[id]["scale"],
            name = data[id]["name"],
            title = data[id]["title"],
            has_shop = data[id]["has_shop"],
            has_game = data[id]["has_game"],
            game_map = data[id]["game_map"]
        )
    except Exception as e:
        npc = BaseNpc(scene)
        print(f"Error Load Npc: {e}")
    finally:
        scene.add_sprite("NPC", npc)
        print(f"{id}: {position}")

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

def load_enemy(id, scene, position, target = None):
    # TODO: Add more enemy types as they get implemented
    enemies = {
        "GroundEnemy": GroundEnemy,
        "FlyingEnemy": FlyingEnemy,
        "IdleGround": IdleGround,
        "IdleFlying": IdleFlying,
        "ChaserGround": ChaserGround,
        "ChaserFlying": ChaserFlying
    }
    try:
        with open("../assets/data/enemies.json", "r") as file:
            data = json.load(file)

        npc = enemies[data[id]["type"]](
                scene = scene,
                sprite_path = data[id]["sprite_path"],
                target = target,
                speed = data[id]["speed"],
                wander_range = data[id]["wander_range"],
                position = position,
                scale = data[id]["scale"],
                max_health = data[id]["max_health"],
                damage = data[id]["damage"],
                drop_curr1 = data[id]["drop_curr1"],
                drop_curr2 = data[id]["drop_curr2"],
                drop_curr3 = data[id]["drop_curr3"],
                drop_curr4 = data[id]["drop_curr4"],
                frame_duration = data[id]["frame_duration"]
            )
    except Exception as e:
        print(f"Error Load Enemy: {e}")
        npc = GroundEnemy(
            scene=scene
        )
    finally:
        scene.add_sprite("Enemy", npc)

def save_data(username, player_stats, operation):
    try:
        if operation == OP_LOAD_DT or operation == OP_SAVE_DT:
            with open("../saves/data.json", "r") as file:
                data = json.load(file)
        else:
            with open("../saves/scores.json", "r") as file:
                data = json.load(file)
        
        if operation == OP_LOAD_DT:
            player_stats.load_powers(data[username])
    
        if operation == OP_SAVE_DT:
            # add/update data for current user
            data[username] = player_stats.save_powers()
            with open("../saves/data.json", "w") as file:
                json.dump(data, file, indent = 4)
        
        if operation == OP_LOAD_SC:
            player_stats.load_scores(data[username])
        
        if operation == OP_SAVE_SC:
            data[username] = player_stats.save_scores()
            with open("../saves/scores.json", "w") as file:
                json.dump(data, file, indent = 4)

    except Exception as e:
        print(f"Error loading data: {e}")
