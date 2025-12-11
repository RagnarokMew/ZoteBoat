import arcade
from entities import player
from core.constants import SCREEN_WIDTH, SCREEN_HEIGHT, TILE_SCALING,\
    RIGHT_FACING, LEFT_FACING, UP_FACING, DOWN_FACING, SIDE_FACING,\
    P_GAMEPLAY, P_DIALOGUE, P_SHOP,\
    GRAVITY, PLAYER_MOVEMENT_SPEED, P_SLIDE,\
    DEFAULT_MAP, DEFAULT_SPAWN
from core.player_stats import PlayerStats
from entities.base_enemies import GroundEnemy
from entities.base_npc import BaseNpc, DialogueMenu
from ui.text import FadingText
from core.shop import ShopMenu
from core.utils import load_enemy, load_npc, load_dialogue, load_shop_items, load_spawn, load_bg

class GameView(arcade.View):

    def __init__(self):
        super().__init__()

        # Temp Value for setting to show enemy hp:
        self.show_enemy_hp = True

        self.physics_engine = None

        self.player_texture = None
        self.player_sprite = None
        self.player_stats = PlayerStats()
        self.player_spawn = None

        self.tile_map = None
        self.scene = None

        self.camera = None
        self.gui_camera = None
        self.health_text = None
        self.currency_text = None
        self.death_text = None

        self.up_pressed = False
        self.down_pressed = False
        self.right_pressed = False
        self.left_pressed = False
        
        self.jump_pressed = False
        self.dash_pressed = False

        self.map_id = DEFAULT_MAP

        self.fade_out = None
        self.fade_in = None

        self.player_interaction_state = P_GAMEPLAY
        self.active_menu = None

        self.background = None

    def setup(self):
        # DEBUG: make sure map is correct
        # print(f"changed to {map_id}")
        
        self.tile_map = arcade.load_tilemap(
            f"../assets/tilemaps/{self.map_id}.tmx",
            scaling = TILE_SCALING
        )

        self.scene = arcade.Scene.from_tilemap(self.tile_map)
        self.background = load_bg(self.map_id, self.background)

        self.scene.add_sprite_list_before("NPC", "Background")
        self.scene.add_sprite_list_after("Enemy", "Background")
        self.scene.add_sprite_list_after("Player", "Enemy")
        self.scene.add_sprite_list_before("EffectFly", "Player")
        self.scene.add_sprite_list_after("EffectDmg", "Player")

        self.player_spawn = load_spawn(self.map_id)
        if not self.player_spawn:
            print(f"\033[91mThe room you tried to enter does not exist :(\033[0m")
            exit(1)
    
        self.player_sprite = player.PlayerSprite(
            self.scene, self.player_spawn[1]
        )
        self.player_sprite.stats = self.player_stats
        self.scene.add_sprite("Player", self.player_sprite)

        self.physics_engine = arcade.PhysicsEnginePlatformer(
            self.player_sprite,
            walls = self.scene["Platforms"],
            gravity_constant = GRAVITY
        )
        # by default, double jumping is disabled
        if self.player_stats.unlocks["Double_Jump"]:
            self.physics_engine.enable_multi_jump(2)

        # optimise collision detection
        self.scene["Load Zone"].enable_spatial_hashing()
        self.scene["Load Zone"].visible = False
        if "Wall Jump" in self.scene:
            self.scene["Wall Jump"].enable_spatial_hashing()
            self.scene["Wall Jump"].visible = False

        if "Enemy Spawn" in self.scene:
            self.scene["Enemy Spawn"].visible = False
            for spawn in self.scene["Enemy Spawn"]:
                enemy_id = spawn.properties["id"]
                if enemy_id != "random": load_enemy(
                    id = enemy_id,
                    scene = self.scene,
                    position = (spawn.center_x, spawn.center_y),
                    target = self.player_sprite
                )

        if "Npc Spawn" in self.scene:
            self.scene["Npc Spawn"].visible = False
            for spawn in self.scene["Npc Spawn"]:
                load_npc(
                    id = spawn.properties["id"],
                    scene = self.scene,
                    position = (spawn.center_x, spawn.center_y)
                )
    
        self.camera = arcade.Camera2D()
        self.gui_camera = arcade.Camera2D()
        
        self.health_text = arcade.Text(
            f"HP: {self.player_stats.health} / {self.player_stats.max_health}",
            x = 5,
            y = SCREEN_HEIGHT - 30,
            font_size = 20,
            color = arcade.color.ALABAMA_CRIMSON
        )

        self.currency_text = FadingText(
            f"currency1: {self.player_stats.currency_1}\ncurrency2: {self.player_stats.currency_2}\ncurrency3: {self.player_stats.currency_3}\ncurrency4: {self.player_stats.currency_4}",
            x = 5,
            y = SCREEN_HEIGHT - 60,
            duration = 2,
            color = arcade.color.SAE
        )
        self.currency_text.duration = self.currency_text.trans_duration = 0
        
        self.death_text = FadingText(
            "You died!",
            x = SCREEN_WIDTH // 2 - 100,
            y = SCREEN_HEIGHT // 2,
            duration = 2,
            font_size = 40,
            color = arcade.color.CERISE
        )
        self.death_text.duration = self.death_text.trans_duration = 0
        
    def update_fade(self):
        if self.fade_out is not None:
            self.fade_out += 10
            if self.fade_out > 255:
                self.fade_out = None
                self.fade_in = 255
                self.setup()

        if self.fade_in is not None:
            self.fade_in -= 5
            if self.fade_in <= 0:
                self.fade_in = None

    def draw_fading(self):
        fade_factor = self.fade_out if self.fade_out else self.fade_in
        if self.fade_out or self.fade_in:
            arcade.draw_rect_filled(
                arcade.XYWH(
                    SCREEN_WIDTH // 2,
                    SCREEN_HEIGHT // 2,
                    self.window.width,
                    self.window.height,
                ),
                color = (0, 0, 0, fade_factor)
            )

    def on_draw(self):
        self.clear()
        self.camera.use()

        arcade.draw_texture_rect(self.background, arcade.LBWH(
            self.camera.position[0] - SCREEN_WIDTH // 2,
            self.camera.position[1] - SCREEN_HEIGHT // 2,
            SCREEN_WIDTH, SCREEN_HEIGHT
        ))

        # NOTE: Below this the World gets Rendered
        # (aka everything gets rendered based on world coordinates)

        self.scene.draw()

        if self.show_enemy_hp:
            for enemy in self.scene["Enemy"]:
                enemy.hp_text.draw()

        self.gui_camera.use()

        # NOTE: Below this GUI gets rendered
        # (aka everything gets rendered based on screen coordinates)

        self.draw_fading()

        self.health_text.draw()
        if self.death_text:
            self.death_text.draw()
        if self.currency_text:
            self.currency_text.draw()

        if self.active_menu:
            self.active_menu.draw()

    def on_key_release(self, key, modifiers):
        if key == arcade.key.LEFT:
            self.left_pressed = False

        if key == arcade.key.RIGHT:
            self.right_pressed = False

        if key == arcade.key.Z:
                self.jump_pressed = False

        if key == arcade.key.UP:
                self.up_pressed = False
                self.player_sprite.facing_direction = SIDE_FACING

        if key == arcade.key.DOWN:
                self.down_pressed = False
                self.player_sprite.facing_direction = SIDE_FACING

        # manual reset switch (debug)
        if key == arcade.key.R:
            self.change_map()

    def on_key_press(self, key, modifiers):
        if key == arcade.key.LEFT:
            self.left_pressed = True

        if key == arcade.key.RIGHT:
            self.right_pressed = True

        if self.player_interaction_state == P_GAMEPLAY:
            if key == arcade.key.Z:
                self.jump_pressed = True
                self.player_sprite.jump(self.physics_engine)

            if key == arcade.key.UP:
                self.up_pressed = True
                self.player_sprite.facing_direction = UP_FACING

                # NOTE: Starts dialogue
                npc = arcade.check_for_collision_with_list(
                    self.player_sprite,
                    self.scene["NPC"]
                )

                if npc and not self.active_menu:
                    self.active_menu = DialogueMenu(
                        id = npc[0].id,
                        content = load_dialogue(npc[0].id),
                        npc_name = npc[0].name,
                        npc_title = npc[0].title,
                        before_shop_interaction = npc[0].has_shop
                    )
                    for all_npc in self.scene["NPC"]: all_npc.set_active(npc[0])
                    self.player_interaction_state = P_DIALOGUE

            if key == arcade.key.DOWN:
                self.down_pressed = True
                self.player_sprite.facing_direction = DOWN_FACING

            if key == arcade.key.X:
                self.player_sprite.attack()

            if key == arcade.key.F5:
                arcade.window_commands.close_window()
                exit(0)

        elif self.player_interaction_state == P_DIALOGUE:
            # NOTE: Not using match bc in docs we put Python >=3.9
            # But match case was introduced in Python 3.10
            if (key == arcade.key.A) or \
                (key == arcade.key.Z) or \
                (key == arcade.key.X):

                # NOTE: The current implementation is very ugly and should be refactored
                # Currently it works the following way:
                # When a dialogue ends it checks if it leads to a shop interaction
                # If it does it spawns a shop and loads its items
                if self.active_menu:
                    if not self.active_menu.next():
                        if self.active_menu.before_shop_interation:
                            self.active_menu = ShopMenu(
                                load_shop_items(self.active_menu.npc_id),
                                self.player_stats,
                                f"{self.active_menu.npc_name}'s Shop"
                            )
                            self.player_interaction_state = P_SHOP
                            self.currency_text.text = f"currency1: {self.player_stats.currency_1}\ncurrency2: {self.player_stats.currency_2}\ncurrency3: {self.player_stats.currency_3}\ncurrency4: {self.player_stats.currency_4}"
                            self.currency_text.reset()
                            self.currency_text.update(0)
                        else:
                            self.active_menu = None
                            self.player_interaction_state = P_GAMEPLAY

        elif self.player_interaction_state == P_SHOP:
            if key == arcade.key.Z:
                self.active_menu.purchase()
                self.health_text.text = f"HP: {self.player_stats.health} / {self.player_stats.max_health}"
                self.currency_text.text = f"currency1: {self.player_stats.currency_1}\ncurrency2: {self.player_stats.currency_2}\ncurrency3: {self.player_stats.currency_3}\ncurrency4: {self.player_stats.currency_4}"
            elif key == arcade.key.X:
                self.active_menu = None

                if self.player_stats.unlocks["Double_Jump"]:
                    self.physics_engine.enable_multi_jump(2)
                self.player_interaction_state = P_GAMEPLAY
            elif key == arcade.key.UP:
                self.active_menu.previous_item()
            elif key == arcade.key.DOWN:
                self.active_menu.next_item()

        if key == arcade.key.C and self.player_interaction_state == P_GAMEPLAY:
                self.dash_pressed = True

        if key == arcade.key.F5:
            arcade.window_commands.close_window()

    def on_update(self, delta_time):
        self.physics_engine.update()
        px_upd = self.player_sprite.update(delta_time)

        # NOTE: New left-right movement handler moved here
        # to fix all movement related bugs
        if self.player_interaction_state == P_GAMEPLAY:
            if self.left_pressed and not self.right_pressed:
                self.player_sprite.direction = LEFT_FACING
                self.player_sprite.change_x = -PLAYER_MOVEMENT_SPEED

            elif self.right_pressed and not self.left_pressed:
                self.player_sprite.direction = RIGHT_FACING
                self.player_sprite.change_x = PLAYER_MOVEMENT_SPEED

            else:
                self.player_sprite.change_x = 0

            try:
                no_entry = arcade.check_for_collision_with_list(
                    self.player_sprite,
                    self.scene["Wall Jump"],
                    method = 1
                )[0]

                if no_entry.properties["side"] == 0:
                    if self.player_sprite.center_x - no_entry.center_x < 0:
                        self.player_sprite.change_x -= P_SLIDE
                    else:
                        self.player_sprite.change_x += P_SLIDE
            except: pass

            if self.dash_pressed:
                self.player_sprite.dash()
                self.dash_pressed = False
            self.player_sprite.change_x += px_upd

        else:
            self.player_sprite.change_x = 0

        self.scene["Enemy"].update(delta_time)
        self.scene["NPC"].update(delta_time, self.player_interaction_state)
        self.scene["EffectDmg"].update(delta_time)
        self.scene["EffectFly"].update(delta_time)

        self.camera.position = self.player_sprite.position
        min_x = max(self.camera.position[0], self.player_spawn[0][0] + 200)
        min_y = max(self.camera.position[1], self.player_spawn[0][1] - 50)
        self.camera.position = arcade.Vec2(min_x, min_y + 50)

        loadzone_collision = arcade.check_for_collision_with_list(
                self.player_sprite,
                self.scene["Load Zone"],
                method = 1
        )

        if loadzone_collision: self.change_map(loadzone_collision)

        self.update_fade()

        # TODO: Refactor the collision code at a later date
        hit = None

        if self.player_sprite.player_attack:
            if "Hazard" in self.scene and arcade.check_for_collision_with_list(
                self.player_sprite.player_attack, self.scene["Hazard"]
            ):  self.player_sprite.pogo(self.physics_engine)
            
            hit = arcade.check_for_collision_with_list(
                self.player_sprite.player_attack, self.scene["Enemy"]
            )

        if hit:
            self.player_sprite.pogo(self.physics_engine)

            for enemy in hit:
                if enemy.inv_time > 0:
                    continue

                enemy.get_hit(self.player_stats.damage, self.player_sprite.player_attack.remaining_duration)
                enemy.update_text()

                if enemy.health <= 0:
                    self.player_stats.currency_1 += enemy.drop_curr1
                    self.player_stats.currency_2 += enemy.drop_curr2
                    self.player_stats.currency_3 += enemy.drop_curr3
                    self.player_stats.currency_4 += enemy.drop_curr4

                    self.currency_text.text = f"currency1: {self.player_stats.currency_1} (+{enemy.drop_curr1})\ncurrency2: {self.player_stats.currency_2} (+{enemy.drop_curr2})\ncurrency3: {self.player_stats.currency_3} (+{enemy.drop_curr3})\ncurrency4: {self.player_stats.currency_4} (+{enemy.drop_curr4})"
                    self.currency_text.reset()

                    self.scene["Enemy"].remove(enemy)

        hit_by = arcade.check_for_collision_with_list(
            self.player_sprite, self.scene["Enemy"]
        )

        if hit_by and self.player_stats.inv_time <= 0:
            self.player_sprite.get_hit(hit_by[0].damage)
            self.health_text.text = f"HP: {self.player_stats.health} / {self.player_stats.max_health}"
            self.player_stats.inv_time = self.player_stats.max_inv_time
        else:
            self.player_stats.inv_time -= delta_time

        if self.currency_text and self.player_interaction_state != P_SHOP:
            self.currency_text.update(delta_time)
        
        if self.death_text:
            self.death_text.update(delta_time)

        hazard_collision = None
        if "Hazard" in self.scene:
            hazard_collision = arcade.check_for_collision_with_list(
                self.player_sprite, self.scene["Hazard"]
            )
            if hazard_collision: self.player_sprite.get_hit(damage = 1)

        if self.player_stats.health <= 0: self.respawn()
        elif hazard_collision: self.respawn(reset = False)

    # handle scene change and spawn point set
    def change_map(self, sprites_coll = None):
        if self.fade_out is None:
            try:
                map_id = sprites_coll[0].properties["map_id"]
                if map_id == "spawn": self.player_spawn = (
                    self.player_spawn[0],
                    sprites_coll[0].position
                )
                else:
                    self.map_id = map_id
                    self.fade_out = 0
            except:
                self.map_id = DEFAULT_MAP
                self.fade_out = 0
    
    def respawn(self, reset = True):
        if reset:
            self.player_stats.health = self.player_stats.max_health
            self.death_text.text = "You died!"
            self.death_text.reset()
            self.death_text.update(0)
        self.health_text.text = f"HP: {self.player_stats.health} / {self.player_stats.max_health}"

        self.scene["EffectDmg"].clear()
        self.scene["EffectFly"].clear()
        self.fade_in = 255

        self.player_sprite.position = self.player_spawn[0 if reset else 1]