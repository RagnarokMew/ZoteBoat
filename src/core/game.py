import arcade
from entities import player, enemy
from core.constants import GRAVITY, LEFT_FACING, PLAYER_MOVEMENT_SPEED, PLAYER_JUMP_SPEED, RIGHT_FACING, TILE_SCALING, UP_FACING, DOWN_FACING, SIDE_FACING
from core.player_stats import PlayerStats

class GameView(arcade.View):
    
    def __init__(self):
        super().__init__()

        self.physics_engine = None

        self.player_texture = None
        self.player_sprite = None
        self.player_stats = PlayerStats()

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

    def setup(self):
        # Temporary tile map for stub creation
        temp_map_name = ":resources:tiled_maps/map2_level_1.json"
        self.tile_map = arcade.load_tilemap(
            temp_map_name,
            scaling = TILE_SCALING
        )

        self.scene = arcade.Scene.from_tilemap(self.tile_map)

        self.scene.add_sprite_list_after("Enemy", "Foreground")
        self.scene.add_sprite_list_after("Player", "Enemy")

        try:    self.scene["Wall Jump"].enable_spatial_hashing()
        except: pass

        # Temporary Spawn, in the future it should be based on the map
        temp_spawn = (128, 400)
        self.player_sprite = player.PlayerSprite(
            self.scene,
            temp_spawn
        )
        self.player_sprite.stats = self.player_stats
        self.scene.add_sprite("Player", self.player_sprite)
        
        # add single enemy to test pogo
        enemy_sprite = enemy.EnemySprite(
            self.scene,
            temp_spawn
        )
        self.scene.add_sprite("Enemy", enemy_sprite)

        self.camera = arcade.Camera2D()
        self.gui_camera = arcade.Camera2D()

        self.background_color = arcade.color.AERO_BLUE

        self.physics_engine = arcade.PhysicsEnginePlatformer(
            self.player_sprite, walls=self.scene["Platforms"], gravity_constant=GRAVITY
        )

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

    def on_key_press(self, key, modifiers):
        if key == arcade.key.Z:
            self.jump_pressed = True

            self.player_sprite.jump(self.physics_engine)

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
        
        # DEBUG: enable/disable all abilities
        if key == arcade.key.W:
            self.player_stats.getall()
            self.player_sprite.stats = self.player_stats
            if self.player_stats.can_double_jump:
                self.physics_engine.enable_multi_jump(2)
            else:
                self.physics_engine.disable_multi_jump()

    def on_update(self, delta_time):
        self.physics_engine.update()
        self.player_sprite.update(
            delta_time, self.physics_engine
        )
        self.camera.position = self.player_sprite.position

