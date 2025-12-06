import arcade
from entities.base_enemies import GroundEnemy, FlyingEnemy

class IdleGround(GroundEnemy):
    def __init__(self, scene, sprite_path,
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

class ChaserGround(GroundEnemy):
    def __init__(self, scene, sprite_path,
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


class IdleFlying(FlyingEnemy):
    def __init__(self, scene, sprite_path,
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


class ChaserFlying(FlyingEnemy):
    def __init__(self, scene, sprite_path,
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

