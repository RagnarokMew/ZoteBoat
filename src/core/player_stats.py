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
        self.unlocks = {
            "Mask_1": False,
            "Mask_2": False,
            "Mask_3": False,
            "Mask_4": False,
            "Nail_Upgrade_Kit_1": False,
            "Nail_Upgrade_Kit_2": False, # Each nail upgrade x2 DMG
            "Wall_Jump": True,
            "Double_Jump": False,
            "Dash": False
        }
        # TODO: Add other player related values
        # (e.g: has_double_jump, has_wall_jump, ...)

    def increase_max_hp(self, amount):
        self.max_health += amount
        self.health = self.max_health

    def increase_damage(self, amount):
        self.damage += amount

    def mark_unlocked(self, upgrade):
        self.unlocks[upgrade] = True

    def mark_locked(self, upgrade):
        self.unlocks[upgrade] = False

