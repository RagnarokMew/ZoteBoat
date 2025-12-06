import arcade
from entities.base_enemies import GroundEnemy, FlyingEnemy

class IdleGround(GroundEnemy):
    def __init__(self, scene, sprite_path, target, speed, wander_range,
                 position=(128, 128),
                 scale=1,
                 damage=1,
                 max_health=1,
                 drop_curr1=1,
                 drop_curr2=1,
                 drop_curr3=1,
                 drop_curr4=1,
                 frame_duration=100):
        super().__init__(
                    scene,
                    sprite_path,
                    scale=scale,
                    max_health=max_health,
                    position=position,
                    damage=damage,
                    drop_curr1=drop_curr1,
                    drop_curr2=drop_curr2,
                    drop_curr3=drop_curr3,
                    drop_curr4=drop_curr4,
                    frame_duration=frame_duration
                )
        self.target = target
        self.movement_speed = speed
        self.change_x = self.movement_speed
        self.wander_range = wander_range

    def update(self, delta_time):
        if self.center_x > self.spawn_x + self.wander_range and self.change_x >= 0:
            self.change_x = -self.movement_speed
        elif self.center_x < self.spawn_x - self.wander_range and self.change_x <= 0:
            self.change_x = self.movement_speed

        super().update(delta_time)

class ChaserGround(GroundEnemy):
    def __init__(self, scene, sprite_path, target, speed, wander_range,
                 position=(128, 128),
                 scale=1,
                 damage=1,
                 max_health=1,
                 drop_curr1=1,
                 drop_curr2=1,
                 drop_curr3=1,
                 drop_curr4=1,
                 frame_duration=100):
        super().__init__(
                    scene,
                    sprite_path,
                    scale=scale,
                    max_health=max_health,
                    position=position,
                    damage=damage,
                    drop_curr1=drop_curr1,
                    drop_curr2=drop_curr2,
                    drop_curr3=drop_curr3,
                    drop_curr4=drop_curr4,
                    frame_duration=frame_duration
                )
        self.target = target
        self.movement_speed = speed
        self.change_x = self.movement_speed
        self.wander_range = wander_range

    def update(self, delta_time):
        self.update_ai()

        if self.ai_state == "chase":
            if self.center_x < self.target.center_x:
                self.change_x = self.movement_speed
            else:
                self.change_x = -self.movement_speed

        elif self.ai_state == "idle":
            if self.center_x > self.spawn_x + self.wander_range and self.change_x >= 0:
                self.change_x = -self.movement_speed
            elif self.center_x < self.spawn_x - self.wander_range and self.change_x <= 0:
                self.change_x = self.movement_speed

        super().update(delta_time)

    def update_ai(self):
        if self.target == None:
            self.ai_state == "idle"
            return

        target_distance = abs(self.target.center_x - self.center_x)

        # Aggro range is currently set to the wander_range
        if target_distance < self.wander_range * 2:
            self.ai_state = "chase"
        else:
            self.ai_state = "idle"

class IdleFlying(FlyingEnemy):
    def __init__(self, scene, sprite_path, target, speed, wander_range,
                 position=(128, 128),
                 scale=1,
                 damage=1,
                 max_health=1,
                 drop_curr1=1,
                 drop_curr2=1,
                 drop_curr3=1,
                 drop_curr4=1,
                 frame_duration=100):
        super().__init__(
                    scene,
                    sprite_path,
                    scale=scale,
                    max_health=max_health,
                    position=position,
                    damage=damage,
                    drop_curr1=drop_curr1,
                    drop_curr2=drop_curr2,
                    drop_curr3=drop_curr3,
                    drop_curr4=drop_curr4,
                    frame_duration=frame_duration
                )
        self.target = target
        self.movement_speed = speed
        self.change_x = self.movement_speed
        self.wander_range = wander_range

    def update(self, delta_time):
        if self.center_x > self.spawn_x + self.wander_range and self.change_x >= 0:
            self.change_x = -self.movement_speed
        elif self.center_x < self.spawn_x - self.wander_range and self.change_x <= 0:
            self.change_x = self.movement_speed

        super().update(delta_time)

class ChaserFlying(FlyingEnemy):
    def __init__(self, scene, sprite_path, target, speed, wander_range,
                 position=(128, 128),
                 scale=1,
                 damage=1,
                 max_health=1,
                 drop_curr1=1,
                 drop_curr2=1,
                 drop_curr3=1,
                 drop_curr4=1,
                 frame_duration=100):
        super().__init__(
                    scene,
                    sprite_path,
                    scale=scale,
                    max_health=max_health,
                    position=position,
                    damage=damage,
                    drop_curr1=drop_curr1,
                    drop_curr2=drop_curr2,
                    drop_curr3=drop_curr3,
                    drop_curr4=drop_curr4,
                    frame_duration=frame_duration
                )

