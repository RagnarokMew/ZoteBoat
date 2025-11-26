import arcade
from core.constants import RIGHT_FACING, LEFT_FACING, UP_FACING, DOWN_FACING, SIDE_FACING, P_ATTACK_COOLDOWN, P_WJUMP_SPEED, P_WJUMP_TIME, P_DASH_SPEED, P_DASH_TIME, P_DASH_COOLDOWN, PLAYER_JUMP_SPEED

class PlayerSprite(arcade.Sprite):

    def __init__(self, scene, position = (0, 0), scale = 1.0):
        # TODO: Change temp asset to one of our own towards the end of development
        super().__init__(
            ":resources:images/animated_characters/robot/robot_idle.png",
            scale = scale
        )

        self.scene = scene
        self.center_x, self.center_y = position
        self.player_attack = None
        self.attack_cooldown = 0.0
        self.direction = RIGHT_FACING
        self.facing_direction = SIDE_FACING

        self.wjump_timer = 0.0
        self.wj_x = 0

        self.dash_timer = 0.0
        self.dash_cooldown = 0.0
        self.dash_dir = 0

        self.stats = None
        self.has_pogo = True
        # TODO: Add textures for player (idle, walk, etc)
        # TODO: Should also work on logic to handle direction facing etc
        # The implementation of these features can be done later on

    def attack(self):
        if(self.attack_cooldown > 0):
            return

        self.player_attack = PlayerAttack(
            self.scene,
            self
        )

        self.attack_cooldown = P_ATTACK_COOLDOWN
    
    def jump(self, phys):
        wj = False

        if self.stats.can_wjump:
            try: wj = arcade.check_for_collision_with_list(
                    self, self.scene["Wall Jump"], method = 1
                )
            except: pass
        
            if wj:
                self.wj_x = wj[0].properties["side"]
                self.change_y = PLAYER_JUMP_SPEED
                self.wjump_timer = P_WJUMP_TIME
    
        if (not wj or not self.stats.can_wjump) and phys.can_jump():
            phys.jump(PLAYER_JUMP_SPEED)
    
    def dash(self):
        if self.stats.can_dash and self.dash_cooldown <= 0:
            self.dash_dir = self.direction
            self.dash_timer = P_DASH_TIME
            self.dash_cooldown = P_DASH_COOLDOWN

    def pogo(self, phys):
        # pogo :3
        if self.facing_direction == DOWN_FACING:
            # don't use phys.jump(), since pogos don't count as jumps
            self.change_y = PLAYER_JUMP_SPEED
            
            # after pogo, add a double jump
            if self.stats.can_djump and self.has_pogo:
                self.has_pogo = False
                phys.jumps_since_ground = max(
                    1, phys.jumps_since_ground - 1
                )

        # this is necessary to prevent multiple pogos per pogo
        else: self.has_pogo = True

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
        
        return self.wj_x * P_WJUMP_SPEED + self.dash_dir * P_DASH_SPEED

class PlayerAttack(arcade.Sprite):

    def __init__(self, scene, parent, scale=1.0):
        super().__init__(
            # TODO: Change temp sprite with one of our own
            ":resources:/onscreen_controls/flat_dark/right.png",
            scale = scale
        )

        self.base_scale_x = self.scale_x
        self.base_scale_y = self.scale_y
        self.offset_x = 48
        self.offset_y = -48
        self.parent = parent
        self.scene = scene
        self.remaining_duration = P_ATTACK_COOLDOWN

        self.scene.add_sprite("PlayerAttack", self)

    def update(self, delta_time):
        self.remaining_duration -= delta_time

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

