from core.constants import P_ATTACK_DAMAGE, P_HEALTH

class PlayerStats():

    def __init__(self):
        self.max_health = P_HEALTH
        self.health = P_HEALTH
        self.damage = P_ATTACK_DAMAGE
        
        # TODO: Add other player related values
        # (e.g: has_double_jump, has_wall_jump, ...)

        self.can_djump = False
        self.can_wjump = False
        self.can_dash = False

    # DEBUG: get/remove all abilities
    def getall(self):
        if not self.can_djump:
            self.can_djump = True
            self.can_wjump = True
            self.can_dash = True
            # etc
        else:
            self.can_djump = False
            self.can_wjump = False
            self.can_dash = False
            # etc