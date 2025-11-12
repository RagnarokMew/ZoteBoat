import arcade
from entities import player
from core.constants import GRAVITY, LEFT_FACING, PLAYER_MOVEMENT_SPEED, PLAYER_JUMP_SPEED, RIGHT_FACING, TILE_SCALING, UP_FACING, DOWN_FACING, SIDE_FACING, SCREEN_HEIGHT, DEFAULT_MAP, DEFAULT_SPAWN
from core.player_stats import PlayerStats
from entities.base_enemies import GroundEnemy

# TODO: for now time is unused, likely remove import

class GameView(arcade.View):

    def __init__(self):
        super().__init__()

        # Temp Value for setting to show enemy hp:
        self.show_enemy_hp = True

        self.physics_engine = None

        self.player_texture = None
        self.player_sprite = None
        self.player_stats = None

        self.player_trans_x = 0
        self.player_trans_y = 0

        self.tile_map = None
        self.scene = None

        self.wall_list = None
        self.enemy_list = None

        self.camera = None
        self.gui_camera = None
        self.health_text = None

        self.jump_pressed = False
        self.up_pressed = False
        self.down_pressed = False
        self.right_pressed = False
        self.left_pressed = False

        self.map_id = DEFAULT_MAP
        (self.sp_x, self.sp_y) = DEFAULT_SPAWN

        self.fade_out = None
        self.fade_in = None

    def setup(self):
        # DEBUG: make sure map is correct
        # print(f"changed to {map_id}")

        self.player_list = arcade.SpriteList()
        self.enemy_list = arcade.SpriteList()

        self.tile_map = arcade.load_tilemap(
            f"../assets/tilemaps/{self.map_id}.tmx",
            scaling = TILE_SCALING
        )

        self.scene = arcade.Scene.from_tilemap(self.tile_map)
        self.scene.add_sprite_list_after("Enemy", "Foreground")
        self.scene.add_sprite_list_after("Player", "Enemy")
        self.player_stats = PlayerStats()

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

        self.camera = arcade.Camera2D()
        self.gui_camera = arcade.Camera2D()

        self.health_text = arcade.Text(
            f"HP: {self.player_stats.health} / {self.player_stats.max_health}",
            x = 5,
            y = SCREEN_HEIGHT - 30,
            color=arcade.color.BLACK,
            font_size=20
        )

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

    def on_key_release(self, key, modifiers):
        if key == arcade.key.Z:
            self.jump_pressed = False

        if key == arcade.key.UP:
            self.up_pressed = False
            self.player_sprite.facing_direction = SIDE_FACING

        if key == arcade.key.DOWN:
            self.down_pressed = False
            self.player_sprite.facing_direction = SIDE_FACING

        if key == arcade.key.LEFT:
            self.left_pressed = False
            self.player_sprite.change_x += PLAYER_MOVEMENT_SPEED

        if key == arcade.key.RIGHT:
            self.right_pressed = False
            self.player_sprite.change_x -= PLAYER_MOVEMENT_SPEED

        # manual reset switch (debug)
        if key == arcade.key.R:
            self.change_map(force = True)

    def on_key_press(self, key, modifiers):
        if key == arcade.key.Z:
            self.jump_pressed = True

            if self.physics_engine.can_jump():
                self.player_sprite.change_y = PLAYER_JUMP_SPEED

        if key == arcade.key.UP:
            self.up_pressed = True
            self.player_sprite.facing_direction = UP_FACING

        if key == arcade.key.DOWN:
            self.down_pressed = True
            self.player_sprite.facing_direction = DOWN_FACING

        if key == arcade.key.LEFT:
            self.left_pressed = True
            self.player_sprite.direction = LEFT_FACING
            self.player_sprite.change_x -= PLAYER_MOVEMENT_SPEED

        if key == arcade.key.RIGHT:
            self.right_pressed = True
            self.player_sprite.direction = RIGHT_FACING
            self.player_sprite.change_x += PLAYER_MOVEMENT_SPEED

        if key == arcade.key.X:
            self.player_sprite.attack()

        if key == arcade.key.F5:
            arcade.window_commands.close_window()

        # movement reset hotkeu
        # TODO: automate this to prevent slide bug
        if key == arcade.key.Q:
            self.player_sprite.change_x = 0

    def on_update(self, delta_time):
        self.physics_engine.update()
        self.player_sprite.update(delta_time)
        self.enemy_list.update(delta_time)
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

        if self.player_stats.health <= 0:
            # TODO: Add respawning logic once level loader is fully implemented
            # Once more features are added, more logic would be included here
            # Temporarily setup will be called again
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
            finally:
                self.player_trans_x += self.player_sprite.change_x

