import arcade
import time
from entities import player, enemy
from core.constants import GRAVITY, LEFT_FACING, PLAYER_MOVEMENT_SPEED, PLAYER_JUMP_SPEED, RIGHT_FACING, TILE_SCALING, UP_FACING, DOWN_FACING, SIDE_FACING
from core.player_stats import PlayerStats
from core.maps import map_array

class GameView(arcade.View):
    
    def __init__(self):
        super().__init__()

        self.physics_engine = None

        self.player_texture = None
        self.player_sprite = None
        self.player_stats = None
        self.player_trans_x = 0

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

    def setup(self, map_index):
        # Temporary tile map for stub creation
        self.map_index = map_index
        self.tile_map = arcade.load_tilemap(
            map_array[self.map_index],
            scaling = TILE_SCALING
        )

        self.scene = arcade.Scene.from_tilemap(self.tile_map)
        self.scene.add_sprite_list_after("Enemy", "Foreground")
        self.scene.add_sprite_list_after("Player", "Enemy")
        self.player_stats = PlayerStats()

        # optimise collision detection for load zone
        try:    self.scene["Load Zone"].enable_spatial_hashing()
        except: pass

        # Temporary Spawn, in the future it should be based on the map
        temp_spawn = (128, 512)
        self.player_sprite = player.PlayerSprite(
            self.scene,
            temp_spawn
        )

        self.scene.add_sprite("Player", self.player_sprite)

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

        # restore player speed after transition
        # TODO: change movement based on transition type
        self.player_sprite.change_x = self.player_trans_x

    def on_draw(self):
        self.clear()

        self.camera.use()

        self.scene.draw()

        self.gui_camera.use()

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
        
        # temp manual map switch (debug)
        if key == arcade.key.W:
            self.change_map()

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

    def on_update(self, delta_time):
        self.physics_engine.update()
        self.player_sprite.update(delta_time)
        self.camera.position = self.player_sprite.position

        # (all scenes should have a load zone, for now use try if it doesn't)
        # if a loadzone was collided with, change scene
        try:
            if arcade.check_for_collision_with_list(
                self.player_sprite,
                self.scene["Load Zone"]
            ):  self.change_map()
        except: pass
    
    # scene change handler
    # TODO: improve for specific types of transitions
    # currently only works properly for horizontals
    def change_map(self):
        self.player_trans_x = self.player_sprite.change_x
        self.setup(1 - self.map_index)