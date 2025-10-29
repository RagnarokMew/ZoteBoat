from typing import override
import arcade

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

        self.left_pressed = False
        self.right_pressed = False
        self.up_pressed = False
        self.down_pressed = False

    def setup(self):
        self.player_list = arcade.SpriteList()
        
        # Temporary tile map for stub creation
        temp_map_name = ":resources:tiled_maps/map2_level_1.json"
        self.tile_map = arcade.load_tilemap(temp_map_name)

        self.scene = arcade.Scene.from_tilemap(self.tile_map)

        # Temporary player texture for stub
        # To be moved to a specific entity/ file
        self.player_texture = arcade.load_texture(
            ':resources:/images/alien/alienBlue_front.png'
        )

        self.scene.add_sprite_list_after("Player", "Foreground")

        # Coords are temporary, in the future they should be done
        # using sprite sizes and aligning to a grid
        # The sprite should be created in a entity/ file
        # where most player logic would reside
        self.player_sprite = arcade.Sprite(self.player_texture)
        self.player_sprite.center_x = 128
        self.player_sprite.center_y = 512
        self.scene.add_sprite("Player", self.player_sprite)

        self.wall_list = self.tile_map.sprite_lists["Platforms"]

        self.camera = arcade.Camera2D()
        self.gui_camera = arcade.Camera2D()

        self.background_color = arcade.color.AERO_BLUE

        # Physics' constants would be defined later in constants
        # Later we could probably move all the physics logic in
        # another file, but for a base this works
        self.physics_engine = arcade.PymunkPhysicsEngine(damping = 1, gravity = (0, -10))

        self.physics_engine.add_sprite(
            self.player_sprite,
            friction=1,
            mass=1,
            moment_of_inertia=arcade.PymunkPhysicsEngine.MOMENT_INF,
            collision_type="player",
            max_horizontal_velocity=500,
            max_vertical_velocity=500,
        )

        self.physics_engine.add_sprite_list(
            self.wall_list,
            friction=3,
            collision_type="wall",
            body_type=arcade.PymunkPhysicsEngine.STATIC,
        )

    def on_key_press(self, key, modifiers):
        # The keys will be changed later to match HK controls
        if key == arcade.key.LEFT:
            self.left_pressed = True

        if key == arcade.key.RIGHT:
            self.right_pressed = True

        if key == arcade.key.UP:
            self.up_pressed = True

        if key == arcade.key.DOWN:
            self.down_pressed = True

    def on_key_release(self, key, modifiers):
        # The keys will be changed later to match HK controls
        if key == arcade.key.LEFT:
            self.left_pressed = False

        if key == arcade.key.RIGHT:
            self.right_pressed = False

        if key == arcade.key.UP:
            self.up_pressed = False

        if key == arcade.key.DOWN:
            self.down_pressed = False

    def on_draw(self):
        self.clear()

        self.camera.use()

        self.scene.draw()

        self.gui_camera.use()

    def on_update(self, delta_time):
        is_on_ground = self.physics_engine.is_on_ground(self.player_sprite)

        # Values will be replaced with constants later
        # These values are random and do not represent how the constants should be
        if self.left_pressed and not self.right_pressed:
            force = (-500, 0)
            self.physics_engine.apply_force(self.player_sprite, force)

        elif self.right_pressed and not self.left_pressed:
            force = (500, 0)
            self.physics_engine.apply_force(self.player_sprite, force)
 
        elif self.up_pressed and not self.down_pressed and is_on_ground:
            force = (0, 1000)
            self.physics_engine.apply_force(self.player_sprite, force)
 
        elif self.down_pressed and not self.up_pressed and not is_on_ground:
            force = (0, -500)
            self.physics_engine.apply_force(self.player_sprite, force)
 
        self.physics_engine.step()
        self.camera.position = self.player_sprite.position
