import arcade
from entities import player
from core.constants import GRAVITY, LEFT_FACING, PLAYER_MOVEMENT_SPEED, PLAYER_JUMP_SPEED, RIGHT_FACING, TILE_SCALING, UP_FACING, DOWN_FACING, SIDE_FACING, SCREEN_HEIGHT, DEFAULT_MAP, DEFAULT_SPAWN, P_GAMEPLAY, P_DIALOGUE, P_SHOP
from core.player_stats import PlayerStats
from entities.base_enemies import GroundEnemy
from entities.base_npc import BaseNpc, DialogueMenu
from ui.text import FadingText
from core.shop import ShopMenu

# NOTE: Temporary Import
from core.shop import ShopItem

# TODO: for now time is unused, likely remove import

class GameView(arcade.View):

    def __init__(self):
        super().__init__()

        # Temp Value for setting to show enemy hp:
        self.show_enemy_hp = True

        self.physics_engine = None

        self.player_texture = None
        self.player_sprite = None
        # TODO: Load player stats based on savefile
        self.player_stats = PlayerStats()

        self.player_trans_x = 0
        self.player_trans_y = 0

        self.tile_map = None
        self.scene = None

        self.enemy_list = None
        self.npc_list = None

        self.camera = None
        self.gui_camera = None
        self.health_text = None
        self.currency_text = None

        self.jump_pressed = False
        self.up_pressed = False
        self.down_pressed = False
        self.right_pressed = False
        self.left_pressed = False

        self.map_id = DEFAULT_MAP
        (self.sp_x, self.sp_y) = DEFAULT_SPAWN

        self.fade_out = None
        self.fade_in = None

        self.player_interaction_state = P_GAMEPLAY
        self.active_menu = None

    def setup(self):
        # DEBUG: make sure map is correct
        # print(f"changed to {map_id}")

        self.enemy_list = arcade.SpriteList()
        self.npc_list = arcade.SpriteList()

        self.tile_map = arcade.load_tilemap(
            f"../assets/tilemaps/{self.map_id}.tmx",
            scaling = TILE_SCALING
        )

        self.scene = arcade.Scene.from_tilemap(self.tile_map)
        self.scene.add_sprite_list_after("Enemy", "Foreground")
        self.scene.add_sprite_list_after("Player", "Enemy")

        # optimise collision detection for load zone
        try:    self.scene["Load Zone"].enable_spatial_hashing()
        except: pass

        self.player_sprite = player.PlayerSprite(
            self.scene,
            (self.sp_x, self.sp_y)
        )

        self.scene.add_sprite("Player", self.player_sprite)

        # TODO: improve enemy spawn in new file, merge ragnarokmew/base-enemies
        try:
            for spawn in self.scene["Enemy Spawn"]:
                # TODO: make spawned enemy type be decided based on spawn
                self.enemy_list.append(
                    GroundEnemy(
                        self.scene,
                        position=(spawn.center_x, spawn.center_y)
                    )
                )
        except: pass

        # TODO: Implement NPC spawn
        try:
            for spawn in self.scene["Npc Spawn"]:
                # TODO: When npc spawning gets implemented the dialogue content
                # name, and title will have to be fetched someplace
                # currently the dialogue isn't saved anywhere and a default
                # gets loaded
                self.npc_list.append(
                    BaseNpc(
                        self.scene,
                        position=(spawn.center_x, spawn.center_y)
                    )
                )
        except: pass

        # NOTE: NPC test start
        # Uncomment to spawn the test npc
        #
        self.npc = BaseNpc(self.scene, ":resources:/images/animated_characters/male_person/malePerson_idle.png", position=(500, 500), has_shop=True)
        self.npc_list.append(self.npc)
        # NOTE: NPC test end

        self.camera = arcade.Camera2D()
        self.gui_camera = arcade.Camera2D()

        self.health_text = arcade.Text(
            f"HP: {self.player_stats.health} / {self.player_stats.max_health}",
            x = 5,
            y = SCREEN_HEIGHT - 30,
            color=arcade.color.BLACK,
            font_size=20
        )

        self.currency_text = FadingText(
            f"currency1: {self.player_stats.currency_1}\ncurrency2: {self.player_stats.currency_2}\ncurrency3: {self.player_stats.currency_3}\ncurrency4: {self.player_stats.currency_4}",
            x = 5,
            y = SCREEN_HEIGHT - 60,
            duration=2
        )
        self.currency_text.duration = self.currency_text.trans_duration = 0


        self.background_color = arcade.color.AERO_BLUE

        self.physics_engine = arcade.PhysicsEnginePlatformer(
            self.player_sprite,
            walls = self.scene["Platforms"],
            gravity_constant = GRAVITY
        )

    def update_fade(self):
        if self.fade_out is not None:
            self.fade_out += 10
            if self.fade_out > 255:
                self.fade_out = None
                self.fade_in = 255
                self.setup()

        if self.fade_in is not None:
            self.fade_in -= 5
            if self.fade_in == 200:
                # restore speed after transition (incl. vertical special)
                self.player_sprite.change_x = self.player_trans_x
                self.player_sprite.change_y = self.player_trans_y
            if self.fade_in <= 0:
                self.fade_in = None

    def draw_fading(self):
        fade_factor = self.fade_out if self.fade_out else self.fade_in
        if self.fade_out or self.fade_in:
            arcade.draw_rect_filled(
                arcade.XYWH(
                    self.window.width / 2,
                    self.window.height / 2,
                    self.window.width,
                    self.window.height,
                ),
                color = (0, 0, 0, fade_factor)
            )

    def on_draw(self):
        self.clear()
        self.camera.use()

        # NOTE: Below this the World gets Rendered
        # (aka everything gets rendered based on world coordinates)

        self.scene.draw()
        self.enemy_list.draw()
        self.npc_list.draw()

        if self.show_enemy_hp:
            for enemy in self.enemy_list:
                enemy.hp_text.draw()

        if self.show_enemy_hp:
            for enemy in self.enemy_list:
                enemy.hp_text.draw()

        self.gui_camera.use()

        # NOTE: Below this GUI gets rendered
        # (aka everything gets rendered based on screen coordinates)

        self.draw_fading()

        self.health_text.draw()
        if self.currency_text:
            self.currency_text.draw()

        if self.active_menu:
            self.active_menu.draw()

    def on_key_release(self, key, modifiers):
        if key == arcade.key.LEFT:
            self.left_pressed = False

        if key == arcade.key.RIGHT:
            self.right_pressed = False

        if self.player_interaction_state == P_GAMEPLAY:
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
                self.change_map(force = True)
        elif self.player_interaction_state == P_DIALOGUE:
            pass
        elif self.player_interaction_state == P_SHOP:
            pass

    def on_key_press(self, key, modifiers):
        if key == arcade.key.LEFT:
            self.left_pressed = True

        if key == arcade.key.RIGHT:
            self.right_pressed = True

        if self.player_interaction_state == P_GAMEPLAY:
            if key == arcade.key.Z:
                self.jump_pressed = True

                if self.physics_engine.can_jump():
                    self.player_sprite.change_y = PLAYER_JUMP_SPEED

            if key == arcade.key.UP:
                self.up_pressed = True
                self.player_sprite.facing_direction = UP_FACING

                # NOTE: Starts dialogue
                npc = arcade.check_for_collision_with_list(
                    self.player_sprite,
                    self.npc_list
                )

                if npc and not self.active_menu:
                    # TODO: When we actually add dialogue text the content
                    # should be added as an array to DialogueMenu in content
                    self.active_menu = DialogueMenu(
                        npc_name=npc[0].name,
                        npc_title=npc[0].title,
                        before_shop_interaction = npc[0].has_shop
                    )
                    self.player_interaction_state = P_DIALOGUE

            if key == arcade.key.DOWN:
                self.down_pressed = True
                self.player_sprite.facing_direction = DOWN_FACING

            if key == arcade.key.X:
                self.player_sprite.attack()

            if key == arcade.key.F5:
                arcade.window_commands.close_window()

            # movement reset hotkeu
            # TODO: automate this to prevent slide bug
            if key == arcade.key.Q:
                self.player_sprite.change_x = 0

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
                # TODO: Load shop items based on npc json
                if self.active_menu:
                    if not self.active_menu.next():
                        if self.active_menu.before_shop_interation:
                            self.active_menu = ShopMenu(
                                [],
                                self.player_stats,
                                f"{self.active_menu.npc_name}'s Shop"
                            )
                            self.player_interaction_state = P_SHOP
                            self.currency_text.reset()
                            self.currency_text.update(0)
                        else:
                            self.active_menu = None
                            self.player_interaction_state = P_GAMEPLAY

        elif self.player_interaction_state == P_SHOP:
            if key == arcade.key.Z:
                self.active_menu.purchase()
                self.health_text.text = f"HP: {self.player_stats.health} / {self.player_stats.max_health}"
            elif key == arcade.key.X:
                self.active_menu = None
                self.player_interaction_state = P_GAMEPLAY
            elif key == arcade.key.UP:
                self.active_menu.previous_item()
            elif key == arcade.key.DOWN:
                self.active_menu.next_item()

    def on_update(self, delta_time):
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

        else:
            self.player_sprite.change_x = 0


        self.physics_engine.update()
        self.player_sprite.update(delta_time)
        self.enemy_list.update(delta_time)
        self.npc_list.update(delta_time)
        self.camera.position = self.player_sprite.position

        loadzone_collision = arcade.check_for_collision_with_list(
                self.player_sprite,
                self.scene["Load Zone"]
        )

        if loadzone_collision:
            self.change_map(loadzone_collision)

        self.update_fade()

        # TODO: Refactor the collision code at a later date
        hit = None

        if self.player_sprite.player_attack:
            hit = arcade.check_for_collision_with_list(
                self.player_sprite.player_attack, self.enemy_list
            )

        if hit:
            for enemy in hit:
                if enemy.inv_time > 0:
                    continue

                enemy.inv_time = self.player_sprite.player_attack.remaining_duration
                enemy.health -= self.player_stats.damage
                enemy.update_text()

                if enemy.health <= 0:
                    self.player_stats.currency_1 += enemy.drop_curr1
                    self.player_stats.currency_2 += enemy.drop_curr2
                    self.player_stats.currency_3 += enemy.drop_curr3
                    self.player_stats.currency_4 += enemy.drop_curr4

                    self.currency_text.text = f"currency1: {self.player_stats.currency_1} (+{enemy.drop_curr1})\ncurrency2: {self.player_stats.currency_2} (+{enemy.drop_curr2})\ncurrency3: {self.player_stats.currency_3} (+{enemy.drop_curr3})\ncurrency4: {self.player_stats.currency_4} (+{enemy.drop_curr4})"
                    self.currency_text.reset()

                    self.enemy_list.remove(enemy)

        hit_by = arcade.check_for_collision_with_list(
            self.player_sprite, self.enemy_list
        )

        if hit_by and self.player_stats.inv_time <= 0:
            self.player_stats.health -= hit_by[0].damage
            self.health_text.text = f"HP: {self.player_stats.health} / {self.player_stats.max_health}"
            self.player_stats.inv_time = self.player_stats.max_inv_time
        else:
            self.player_stats.inv_time -= delta_time

        if self.currency_text and self.player_interaction_state != P_SHOP:
            self.currency_text.update(delta_time)

        if self.player_stats.health <= 0:
            # TODO: Add respawning logic once level loader is fully implemented
            # Once more features are added, more logic would be included here
            # Temporarily setup will be called again
            self.player_stats.health = self.player_stats.max_health
            self.setup()

    # scene change handler
    # TODO: improve horizontal transition
    # TODO: add vertical transition (up should apply force)
    def change_map(self, sprites_coll = None):

        if self.fade_out is None:
            self.fade_out = 0
            # set spawn in new map
            try:
                self.map_id = sprites_coll[0].properties["mapid"]
                self.sp_x = sprites_coll[0].properties["spawn_x"]
                self.sp_y = sprites_coll[0].properties["spawn_y"]
                # DEBUG: make sure spawn coords are set correctly
                # print(sp_x, sp_y)
            except:
                self.map_id = DEFAULT_MAP
                (self.sp_x, self.sp_y) = DEFAULT_SPAWN
            # set transition velocity
            try:
                self.player_trans_x = sprites_coll[0].properties["trans_x"]
                self.player_trans_y = sprites_coll[0].properties["trans_y"]
            except:
                self.player_trans_x = self.player_trans_y = 0

