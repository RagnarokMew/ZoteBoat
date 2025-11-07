from core.constants import P_ATTACK_DAMAGE, P_HEALTH

class PlayerStats():

    def __init__(self):
        self.max_health = P_HEALTH
        self.health = P_HEALTH
        self.damage = P_ATTACK_DAMAGE
        
        # TODO: Add other player related values
        # (e.g: has_double_jump, has_wall_jump, ...)

