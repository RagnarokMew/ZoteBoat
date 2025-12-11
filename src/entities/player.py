import arcade
from core.constants import RIGHT_FACING, LEFT_FACING, UP_FACING, DOWN_FACING, SIDE_FACING, P_ATTACK_COOLDOWN, P_WJUMP_SPEED, P_WJUMP_TIME, P_DASH_SPEED, P_DASH_TIME, P_DASH_COOLDOWN, PLAYER_JUMP_SPEED

def load_texture_pair_h(path):
    return [
        arcade.load_texture(path),
        arcade.load_texture(path).flip_horizontally()
    ]

class PlayerSprite(arcade.Sprite):

    def __init__(self, scene, position = (0, 0), scale = 1.0):
        # TODO: Change temp asset to one of our own towards the end of development
        self._load_textures(":resources:images/animated_characters/robot/robot")

        super().__init__(
            self.animations["idle"][0][0],
            scale=scale
        )

        self.scene = scene
        self.center_x, self.center_y = position
        self.player_attack = None
        self.attack_cooldown = 0.0
        self.direction = RIGHT_FACING
        self.facing_direction = SIDE_FACING

        self.current_state = "idle"
        self.cur_textures = self.animations["idle"]
        self.cur_tex_index = 0
        self.frame_duration = 60
        self.cur_frame_duration = 0

        self.wjump_timer = 0.0
        self.wj_x = 0

        self.dash_timer = 0.0
        self.dash_cooldown = 0.0
        self.dash_dir = 0

        self.stats = None

    def attack(self):
        if(self.attack_cooldown > 0):
            return

        self.player_attack = PlayerAttack(
            self.scene,
            self
        )

        self.attack_cooldown = P_ATTACK_COOLDOWN

    def is_on_wall(self):
        try: return arcade.check_for_collision_with_list(
            self, self.scene["Wall Jump"], method = 1
        )
        except: return None

    def jump(self, phys):
        wj = self.is_on_wall()

        if self.stats.unlocks["Wall_Jump"] and wj:
            self.wj_x = wj[0].properties["side"]
            self.change_y = PLAYER_JUMP_SPEED
            self.wjump_timer = P_WJUMP_TIME

            if self.stats.unlocks["Double_Jump"]:
                phys.jumps_since_ground = max(
                    1, phys.jumps_since_ground - 1
                )

        elif phys.can_jump():
            phys.jump(PLAYER_JUMP_SPEED)

    def dash(self):
        if self.stats.unlocks["Dash"] and self.dash_cooldown <= 0:
            wj = self.is_on_wall()

            if self.stats.unlocks["Wall_Jump"] and wj:
                self.dash_dir = wj[0].properties["side"]
            else:
                self.dash_dir = self.direction

            self.dash_timer = P_DASH_TIME
            self.dash_cooldown = P_DASH_COOLDOWN

    def pogo(self, phys):
        # pogo :3
        if self.facing_direction == DOWN_FACING:
            # don't use phys.jump(), since pogos don't count as jumps
            self.change_y = PLAYER_JUMP_SPEED

            # after pogo, add a double jump
            # the max disallows multiple pogos per pogo
            if self.stats.unlocks["Double_Jump"]:
                phys.jumps_since_ground = max(
                    1, phys.jumps_since_ground - 1
                )

    def update(self, delta_time):
        # TODO: is this check necessary?
        # the attack already has a remaining_duration
        if self.attack_cooldown > 0:
            self.attack_cooldown -= delta_time

        self.wjump_timer = max(
            0.0, self.wjump_timer - delta_time
        )
        if self.wjump_timer <= 0: self.wj_x = 0

        self.dash_timer = max(
            0.0, self.dash_timer - delta_time
        )
        if self.dash_timer <= 0: self.dash_dir = 0
        if self.dash_dir == 0:
            self.dash_cooldown = max(
                0.0, self.dash_cooldown - delta_time 
            )

        if self.player_attack is not None:
            self.player_attack.position = self.position
            self.player_attack.update(delta_time)

        self.update_animation(delta_time)

        return self.wj_x * P_WJUMP_SPEED + self.dash_dir * P_DASH_SPEED


    def update_animation(self, delta_time):
        if self.change_y > 0:
            self.current_state = "jump"
        elif self.change_y < 0:
            self.current_state = "fall"
        elif self.change_x != 0:
            self.current_state = "walk"
        else:
            self.current_state = "idle"

        self.cur_textures = self.animations[self.current_state]

        self._next_texture(delta_time)

    def _next_texture(self, delta_time):
        self.cur_frame_duration += delta_time

        if self.cur_frame_duration * 1000 < self.frame_duration:
            return

        self.cur_frame_duration = 0

        self.cur_tex_index += 1
        self.cur_tex_index %= len(self.cur_textures)

        if self.direction == LEFT_FACING:
            self.texture = self.cur_textures[self.cur_tex_index][1]
        else:
            self.texture = self.cur_textures[self.cur_tex_index][0]


    def _load_textures(self, base_path):
        # TODO: add temp animations for the following (if needed):
        # taking damage
        # dying
        # double jump
        # dashing
        # wall climbing

        idle_textures = [
            load_texture_pair_h(f"{base_path}_idle.png")
        ]
        walk_textures = [
            load_texture_pair_h(f"{base_path}_walk{i}.png") for i in range(0,8)
        ]
        jump_textures = [
            load_texture_pair_h(f"{base_path}_jump.png")
        ]
        fall_textures = [
            load_texture_pair_h(f"{base_path}_fall.png")
        ]

        self.animations = {
            "idle": idle_textures,
            "walk": walk_textures,
            "jump": jump_textures,
            "fall": fall_textures
        }

class PlayerAttack(arcade.Sprite):

    def __init__(self, scene, parent, scale=1.0):
        self.attack_textures = self._load_textures("../assets/player/attack/")
        self.cur_tex_index = 0
        super().__init__(
            self.attack_textures[self.cur_tex_index],
            scale=scale
        )

        self.base_scale_x = self.scale_x
        self.base_scale_y = self.scale_y
        self.offset_x = 48
        self.offset_y = -24
        self.parent = parent
        self.scene = scene
        self.remaining_duration = P_ATTACK_COOLDOWN

        self.scene.add_sprite("PlayerAttack", self)

    def update(self, delta_time):
        self.remaining_duration -= delta_time

        self.update_animation(delta_time)

        self.angle = 90 * self.parent.facing_direction

        if self.parent.facing_direction == SIDE_FACING:
            self.scale_x = self.base_scale_x * self.parent.direction
            self.center_x = self.parent.center_x + self.offset_x * self.parent.direction
        else:
            self.scale_x = self.base_scale_x
            self.scale_y = self.base_scale_y * -1


        self.center_y = self.parent.center_y + self.offset_y * self.parent.facing_direction

        if self.parent.facing_direction == DOWN_FACING:
            self.center_y = self.center_y + self.offset_y

        if self.remaining_duration <= 0:
            self.remove_from_sprite_lists()
            self.parent.player_attack = None

    def update_animation(self, delta_time):
        # TODO: Tweak this if necessary
        if self.remaining_duration < P_ATTACK_COOLDOWN / 3:
            self.cur_tex_index = 1
        else:
            self.cur_tex_index = 0

        self.texture = self.attack_textures[self.cur_tex_index]


    def _load_textures(self, base_path):
        textures = [
            arcade.load_texture(f"{base_path}attack{i}.png") for i in range(2,4)
        ]

        return textures

