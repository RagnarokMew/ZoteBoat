from core.constants import P_ATTACK_DAMAGE, P_HEALTH, P_INV_TIME
import time

class PlayerStats():

    def __init__(self):
        self.max_health = P_HEALTH
        self.max_inv_time = P_INV_TIME
        self.health = P_HEALTH
        self.inv_time = P_INV_TIME
        self.damage = P_ATTACK_DAMAGE

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
            "Wall_Jump": False,
            "Double_Jump": False,
            "Dash": False
        }
        
        self.parkour_start = None
        self.parkour_score = {
            "hrs": 0,
            "min": 0,
            "sec": 0
        }
        self.parkour_break = False  # if previous high score has been broken
        self.parkour_hiscore = {
            "hrs": -1,              # default value: no attempts
            "min": 0,
            "sec": 0
        }

        self.arena_start = False
        self.arena_timer = 0
        self.new_kill = 0
        self.forfeit = False
        self.arena_score = {
            "kill": 0,
            "time": 0
        }
        self.arena_break = False    # if previous high score has been broken
        self.arena_hiscore = {
            "kill": -1,             # default value: no attempts
            "time": 0
        }
    
    def load_powers(self, powers):
        self.unlocks["Mask_1"] = powers["mask_1"]
        self.unlocks["Mask_2"] = powers["mask_2"]
        self.unlocks["Mask_3"] = powers["mask_3"]
        self.unlocks["Mask_4"] = powers["mask_4"]
        self.health = self.max_health = powers["hp"]

        self.unlocks["Nail_Upgrade_Kit_1"] = powers["nail_1"]
        self.unlocks["Nail_Upgrade_Kit_2"] = powers["nail_2"]
        self.damage = powers["dmg"]
        
        self.unlocks["Wall_Jump"] = powers["wall"]
        self.unlocks["Double_Jump"] = powers["dblj"]
        self.unlocks["Dash"] = powers["dash"]

        self.currency_1 = powers["curr_1"]
        self.currency_2 = powers["curr_2"]
        self.currency_3 = powers["curr_3"]
        self.currency_4 = powers["curr_4"]
    
    def save_powers(self):
        return {
            "mask_1": self.unlocks["Mask_1"],
            "mask_2": self.unlocks["Mask_2"],
            "mask_3": self.unlocks["Mask_3"],
            "mask_4": self.unlocks["Mask_4"],
            "hp": self.max_health,
            
            "nail_1": self.unlocks["Nail_Upgrade_Kit_1"],
            "nail_2": self.unlocks["Nail_Upgrade_Kit_2"],
            "dmg": self.damage,
            
            "wall": self.unlocks["Wall_Jump"],
            "dblj": self.unlocks["Double_Jump"],
            "dash": self.unlocks["Dash"],
            
            "curr_1": self.currency_1,
            "curr_2": self.currency_2,
            "curr_3": self.currency_3,
            "curr_4": self.currency_4
        }
    
    def load_scores(self, scores):
        self.parkour_hiscore = {
            "hrs": scores["parkour"][0],
            "min": scores["parkour"][1],
            "sec": scores["parkour"][2]
        }
        self.arena_hiscore = {
            "kill": scores["arena"][0],
            "time": scores["arena"][1]
        }
    
    def save_scores(self):
        return {
            "arena": [
                self.arena_hiscore["kill"],
                self.arena_hiscore["time"]
            ],
            "parkour": [
                self.parkour_hiscore["hrs"],
                self.parkour_hiscore["min"],
                self.parkour_hiscore["sec"]
            ]
        }

    # DEBUG: get all stats in console
    def print(self):
        print(self.unlocks["Mask_1"])
        print(self.unlocks["Mask_2"])
        print(self.unlocks["Mask_3"])
        print(self.unlocks["Mask_4"])

        print(self.unlocks["Nail_Upgrade_Kit_1"])
        print(self.unlocks["Nail_Upgrade_Kit_2"])
        
        print(self.unlocks["Wall_Jump"])
        print(self.unlocks["Double_Jump"])
        print(self.unlocks["Dash"])

        print(self.currency_1)
        print(self.currency_2)
        print(self.currency_3)
        print(self.currency_4)

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
        if minigame == "parkour_00" and self.parkour_start is None:
            self.parkour_start = time.time()
            self.parkour_break = False
        if minigame == "hub_01":
            self.end_parkour()
        
        if minigame == "arena_01":
            self.arena_start = True
            self.arena_timer = 0
            self.new_kill = 0
            self.arena_break = False
    
    def end_parkour(self):
        if self.parkour_start is None:
            print(f"\033[91mParkour not started!\033[0m")
            return

        parkour_end = time.gmtime(time.time() - self.parkour_start)

        self.parkour_score["hrs"] = parkour_end.tm_hour
        self.parkour_score["min"] = parkour_end.tm_min
        self.parkour_score["sec"] = parkour_end.tm_sec

        self.parkour_start = None

        self.parkour_break = (
            self.parkour_score["hrs"] <= self.parkour_hiscore["hrs"] and
            self.parkour_score["min"] <= self.parkour_hiscore["min"] and
            self.parkour_score["sec"] <  self.parkour_hiscore["sec"]
        )
        
        if self.parkour_break or self.parkour_hiscore["hrs"] == -1:
            self.parkour_break = True
            self.parkour_hiscore["hrs"] = self.parkour_score["hrs"]
            self.parkour_hiscore["min"] = self.parkour_score["min"]
            self.parkour_hiscore["sec"] = self.parkour_score["sec"]
    
    def arena_kill(self):
        if self.arena_start: self.new_kill += 1

    def end_arena(self, forfeit = False):
        if not self.arena_start:
            print(f"\033[91mArena not started!\033[0m")
            return
        
        self.arena_start = False
        
        if forfeit:
            self.forfeit = True
            return
        
        self.forfeit = False
        self.arena_score["kill"] = self.new_kill
        self.arena_score["time"] = round(self.arena_timer, 2)

        self.arena_break = (
            self.arena_score["kill"] > self.arena_hiscore["kill"] or
            self.arena_score["time"] > self.arena_hiscore["time"]
        )

        if self.arena_break or self.arena_hiscore["kill"] == -1:
            self.arena_break = True
            self.arena_hiscore["kill"] = self.arena_score["kill"]
            self.arena_hiscore["time"] = self.arena_score["time"]

    def update_arena(self, delta_time):
        self.arena_timer = min(self.arena_timer + delta_time, 60)
        if self.arena_start and self.arena_timer >= 60:
            self.end_arena()
            return True
        return False