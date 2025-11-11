import arcade
import time
from entities import player, enemy
from core.constants import *
from core.player_stats import PlayerStats

# TODO: for now time is unused, likely remove import

class GameView(arcade.View):
    
    def __init__(self):
        super().__init__()

        self.physics_engine = None

        self.player_texture = None
        self.player_sprite = None
        self.player_stats = None

        self.player_trans_x = 0
        self.player_trans_y = 0

        self.tile_map = None
        self.scene = None

        self.wall_list = None

        self.camera = None
        self.gui_camera = None

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
            for enemy_spawner in self.scene["Enemy Spawn"]:
                self.enemy_sprite = enemy.EnemySprite(
                    self.scene,
                    (enemy_spawner.center_x, enemy_spawner.center_y - 20)
                )
                self.scene.add_sprite("Enemy", self.enemy_sprite)
        except: pass

        self.camera = arcade.Camera2D()
        self.gui_camera = arcade.Camera2D()

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
        self.scene.draw()
        self.gui_camera.use()

        self.draw_fading()

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
        self.camera.position = self.player_sprite.position
        
        self.change_map()
        self.update_fade()
    
    # scene change handler
    # TODO: improve horizontal transition
    # TODO: add vertical transition (up should apply force)
    def change_map(self, force = False):
        sprites_coll = None
        try:
            sprites_coll = arcade.check_for_collision_with_list(
                self.player_sprite,
                self.scene["Load Zone"]
            )
        except: pass

        if (sprites_coll or force) and (self.fade_out is None):
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