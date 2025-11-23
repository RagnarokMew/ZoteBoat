from core.constants import P_ATTACK_DAMAGE, P_HEALTH, P_INV_TIME

class PlayerStats():

    def __init__(self):
        self.max_health = P_HEALTH
        self.health = P_HEALTH
        self.damage = P_ATTACK_DAMAGE
        self.max_inv_time = P_INV_TIME
        self.inv_time = P_INV_TIME
        self.currency_1 = 0
        self.currency_2 = 0
        self.currency_3 = 0
        self.currency_4 = 0
        # TODO: Add other player related values
        # (e.g: has_double_jump, has_wall_jump, ...)

