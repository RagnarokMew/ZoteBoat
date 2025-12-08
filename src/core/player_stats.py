from core.constants import P_ATTACK_DAMAGE, P_HEALTH, P_INV_TIME
import time

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
            "Double_Jump": True,
            "Dash": True
        }
        
        self.parkour_start = None
        self.parkour_break = False  # autosave: see if player quit before finishing (shown on LB)
        self.parkour_score = {
            "hrs": 0,
            "min": 0,
            "sec": 0
        }

        self.arena_start = False
        self.arena_timer = 0
        self.arena_score = {
            "kill": 0,
            "time": 0
        }

    def increase_max_hp(self, amount):
        self.max_health += amount
        self.health = self.max_health

    def increase_damage(self, amount):
        self.damage += amount

    def mark_unlocked(self, upgrade):
        self.unlocks[upgrade] = True

    def mark_locked(self, upgrade):
        self.unlocks[upgrade] = False
    
    def init_minigame(self, minigame):
        if minigame == "MG_1" and self.parkour_start is None:
            self.parkour_start = time.time()
        
        if minigame == "MG_2":
            self.arena_start = True
            self.arena_timer = 60
    
    def end_parkour(self):
        if self.parkour_start is None:
            print(f"\033[91mParkour not started!\033[0m")
            return

        parkour_end = time.gmtime(time.time() - self.parkour_start)

        self.parkour_score["hrs"] = parkour_end.tm_hour
        self.parkour_score["min"] = parkour_end.tm_min
        self.parkour_score["sec"] = parkour_end.tm_sec

        self.parkour_start = None

    def update(self, delta_time):
        self.arena_timer = max(0, self.arena_timer - delta_time)
        if self.arena_start and self.arena_timer <= 0:
            self.arena_start = False