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
        self.player_sprite.center_y = 128
        self.scene.add_sprite("Player", self.player_sprite)

        self.camera = arcade.Camera2D()
        self.gui_camera = arcade.Camera2D()

        self.background_color = arcade.color.AERO_BLUE

    def on_draw(self):
        self.clear()

        self.camera.use()

        self.scene.draw()

        self.gui_camera.use()

    def on_update(self, delta_time):
        self.camera.position = self.player_sprite.position
