import arcade
from entities import player
from core.constants import GRAVITY, PLAYER_MOVEMENT_SPEED, PLAYER_JUMP_SPEED, TILE_SCALING

class GameView(arcade.View):
    
    def __init__(self):
        super().__init__()

        self.physics_engine = None

        self.player_texture = None
        self.player_sprite = None

        self.tile_map = None
        self.scene = None

        self.player_list = None
        self.wall_list = None

        self.camera = None
        self.gui_camera = None

        self.up_pressed = False
        self.down_pressed = False
        self.right_pressed = False
        self.left_pressed = False

    def setup(self):
        self.player_list = arcade.SpriteList()
        
        # Temporary tile map for stub creation
        temp_map_name = ":resources:tiled_maps/map2_level_1.json"
        self.tile_map = arcade.load_tilemap(
            temp_map_name,
            scaling=TILE_SCALING
        )

        self.scene = arcade.Scene.from_tilemap(self.tile_map)

        self.scene.add_sprite_list_after("Player", "Foreground")

        # Temporary Spawn, in the future it should be based on the map
        temp_spawn = (128, 512)
        self.player_sprite = player.PlayerSprite(
            self.scene,
            temp_spawn
        )

        self.scene.add_sprite("Player", self.player_sprite)

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
        if key == arcade.key.UP:
            self.up_pressed = False

        if key == arcade.key.DOWN:
            self.up_pressed = False

        if key == arcade.key.LEFT:
            self.up_pressed = False
            self.player_sprite.change_x += PLAYER_MOVEMENT_SPEED

        if key == arcade.key.RIGHT:
            self.up_pressed = False
            self.player_sprite.change_x -= PLAYER_MOVEMENT_SPEED

    def on_key_press(self, key, modifiers):
        if key == arcade.key.UP:
            self.up_pressed = True

            if self.physics_engine.can_jump():
                self.player_sprite.change_y = PLAYER_JUMP_SPEED

        if key == arcade.key.DOWN:
            self.up_pressed = True

        if key == arcade.key.LEFT:
            self.up_pressed = True
            self.player_sprite.change_x -= PLAYER_MOVEMENT_SPEED

        if key == arcade.key.RIGHT:
            self.up_pressed = True
            self.player_sprite.change_x += PLAYER_MOVEMENT_SPEED

        if key == arcade.key.X:
            self.player_sprite.attack()

    def on_update(self, delta_time):
        self.physics_engine.update()
        self.player_sprite.update(delta_time)
        self.camera.position = self.player_sprite.position
