#!/usr/bin/env python3




class aniFood:
    def __init__(self, name=None, id=None, attack=None, health=None, 
                 abilType=None, abilBonus=None, level=None, tier=None):

        self.name      = name
        self.id        = id
        self.attack    = attack
        self.health    = health
        self.abilType  = abilType
        self.abilBonus = abilBonus
        self.level     = level
        self.tier      = tier
        self.pos       = None
        self.foodHeld  = None

    def get_level(self):
        return self.level
    
    def set_pos(self, pos):
        self.pos = pos
    
    def set_foodHeld(self, food):
        self.foodHeld = food
    
    def get_foodHeld(self):
        return self.foodHeld
    
    def get_food_bonus(self):
        if self.foodHeld is None:
            return 0
        else:
            return self.foodHeld.get_abilBonus()
    
    def get_id(self):
        return self.id

    def set_name(self, name):
        self.name = name
    
    def set_attack(self, attack):
        self.attack = attack
    
    def set_health(self, health):
        self.heatlh = health
    
    def set_abilType(self, abilType):
        self.abilType = abilType

    def set_abilBonus(self, abilBonus):
        self.abilBonus = abilBonus

    def set_level(self, level):
        self.level = level

    def set_tier(self, tier):
        self.tier = tier

    def get_abilBonus(self, stage=None):
        if isinstance(self.abilBonus, int):
            return self.abilBonus
    
    def get_name(self):
        return self.name
            
    
    def __repr__(self) -> str:
        return f"{self.name}(\"{self.name}\", {self.id}, {self.attack}, {self.health}, {self.abilType}, "\
               f"{self.abilBonus}, {self.level}, {self.tier})"


'''BEGIN PET STUFFS'''


class none(aniFood):
    def __init__(self, name="none", id=-1, attack=0, health=0, abilType=None, abilBonus=0, level=None, tier=None):
        super().__init__(name, id, attack, health, abilType, abilBonus, level, tier)

class empty(aniFood):
    def __init__(self, name="empty", id=0, attack=0, health=0, abilType=None, abilBonus=0, level=None, tier=None):
        super().__init__(name, id, attack, health, abilType, abilBonus, level, tier)

class ant(aniFood):
    def __init__(self, name="ant", id=1, attack=2, health=1, abilType="faint", abilBonus=3, level=1, tier=1):
        super().__init__(name, id, attack, health, abilType, abilBonus, level, tier)
    def get_abilBonus(self, stage=None):
        return self.abilBonus * self.level

class apple(aniFood):
    def __init__(self, name="apple", id=2, attack=1, health=1, abilType="buff", abilBonus=2, level=1, tier=1):
        super().__init__(name, id, attack, health, abilType, abilBonus, level, tier)

class badgr(aniFood):
    def __init__(self, name="badgr", id=3, attack=5, health=4, abilType="faint", abilBonus="badgr", level=1, tier=3):
        super().__init__(name, id, attack, health, abilType, abilBonus, level, tier)
    def get_abilBonus(self, stage=None):
        return int(self.attack * (self.level / 2))

class beavr(aniFood):
    def __init__(self, name="beavr", id=4, attack=3, health=2, abilType="sell", abilBonus=2, level=1, tier=1):
        super().__init__(name, id, attack, health, abilType, abilBonus, level, tier)
    def get_abilBonus(self, stage=None):
        return self.abilBonus * self.level

class bfish(aniFood):
    def __init__(self, name="bfish", id=5, attack=3, health=5, abilType="hurt", abilBonus=2, level=1, tier=3):
        super().__init__(name, id, attack, health, abilType, abilBonus, level, tier)
    def get_abilBonus(self, stage=None):
        return self.abilBonus * self.level

class bison(aniFood):
    def __init__(self, name="bison", id=6, attack=4, health=4, abilType="endTurn", abilBonus=4, level=1, tier=4):
        super().__init__(name, id, attack, health, abilType, abilBonus, level, tier)
    def get_abilBonus(self, stage=None):
        return self.abilBonus * self.level

class boar(aniFood):
    def __init__(self, name="boar", id=7, attack=10, health=6, abilType="beforeAttack", abilBonus=6, level=1, tier=6):
        super().__init__(name, id, attack, health, abilType, abilBonus, level, tier)
    def get_abilBonus(self, stage=None):
        return self.abilBonus * self.level

class camel(aniFood):
    def __init__(self, name="camel", id=8, attack=2, health=6, abilType="hurt", abilBonus=4, level=1, tier=3):
        super().__init__(name, id, attack, health, abilType, abilBonus, level, tier)
    def get_abilBonus(self, stage=None):
        return self.abilBonus * self.level

class can(aniFood):
    def __init__(self, name="can", id=9, attack=2, health=1, abilType="food", abilBonus=3, level=None, tier=4):
        super().__init__(name, id, attack, health, abilType, abilBonus, level, tier)

class cat(aniFood):
    def __init__(self, name="cat", id=10, attack=4, health=5, abilType="hurt", abilBonus=4, level=1, tier=6):
        super().__init__(name, id, attack, health, abilType, abilBonus, level, tier)
    def get_abilBonus(self, stage=None):
        return self.abilBonus * self.level

class ccake(aniFood):
    def __init__(self, name="ccake", id=11, attack=3, health=3, abilType="food", abilBonus=6, level=None, tier=2):
        super().__init__(name, id, attack, health, abilType, abilBonus, level, tier)

class chili(aniFood):
    def __init__(self, name="chili", id=12, attack=5, health=0, abilType="splashAttack", abilBonus=5, level=None, tier=5):
        super().__init__(name, id, attack, health, abilType, abilBonus, level, tier)

class choco(aniFood):
    def __init__(self, name="choco", id=13, attack=1, health=1, abilType="level", abilBonus=10, level=None, tier=6):
        super().__init__(name, id, attack, health, abilType, abilBonus, level, tier)

class cow(aniFood):
    def __init__(self, name="cow", id=14, attack=4, health=6, abilType="buy", abilBonus=6, level=1, tier=5):
        super().__init__(name, id, attack, health, abilType, abilBonus, level, tier)
    def get_abilBonus(self, stage=None):
        return self.abilBonus * self.level

class crab(aniFood):
    def __init__(self, name="crab", id=15, attack=3, health=3, abilType="buy", abilBonus=3, level=1, tier=2):
        super().__init__(name, id, attack, health, abilType, abilBonus, level, tier)
    def get_abilBonus(self, stage=None):
        return self.abilBonus * self.level

class crikt(aniFood):
    def __init__(self, name="crikt", id=16, attack=1, health=2, abilType="faint", abilBonus=2, level=1, tier=1):
        super().__init__(name, id, attack, health, abilType, abilBonus, level, tier)
    def get_abilBonus(self, stage=None):
        return self.abilBonus * self.level

class croc(aniFood):
    def __init__(self, name="croc", id=17, attack=8, health=4, abilType="startOfBattle", abilBonus=8, level=1, tier=5):
        super().__init__(name, id, attack, health, abilType, abilBonus, level, tier)
    def get_abilBonus(self, stage=None):
        return self.abilBonus * self.level

class deer(aniFood):
    def __init__(self, name="deer", id=18, attack=1, health=1, abilType="faint", abilBonus=10, level=1, tier=4):
        super().__init__(name, id, attack, health, abilType, abilBonus, level, tier)
    def get_abilBonus(self, stage=None):
        return self.abilBonus * self.level

class dlphn(aniFood):
    def __init__(self, name="dlphn", id=19, attack=4, health=6, abilType="startOfBattle", abilBonus=5, level=1, tier=4):
        super().__init__(name, id, attack, health, abilType, abilBonus, level, tier)
    def get_abilBonus(self, stage=None):
        return self.abilBonus * self.level

class dodo(aniFood):
    def __init__(self, name="dodo", id=20, attack=2, health=3, abilType="startOfBattle", abilBonus=None, level=1, tier=2):
        super().__init__(name, id, attack, health, abilType, abilBonus, level, tier)
    def get_abilBonus(self, stage=None):
        return int(self.attack * (self.level / 2))

class dog(aniFood):
    def __init__(self, name="dog", id=21, attack=3, health=3, abilType="friendSummoned", abilBonus=1, level=1, tier=2):
        super().__init__(name, id, attack, health, abilType, abilBonus, level, tier)
    def get_abilBonus(self, stage=None):
        return self.abilBonus * self.level

#TODO: WHat the hell do we do here???
class dragn(aniFood):
    def __init__(self, name="dragn", id=22, attack=6, health=8, abilType="buyTier1Pet", abilBonus=2, level=1, tier=6):
        super().__init__(name, id, attack, health, abilType, abilBonus, level, tier)
    def get_abilBonus(self, stage=None):
        return self.abilBonus * self.level

# IDS FUCKED FROM HERE ON
class duck(aniFood):
    def __init__(self, name="duck", id=23, attack=2, health=3, abilType="sell", abilBonus=1, level=1, tier=1):
        super().__init__(name, id, attack, health, abilType, abilBonus, level, tier)
    def get_abilBonus(self, stage=None):
        return self.abilBonus * self.level

class elpht(aniFood):
    def __init__(self, name="elpht", id=24, attack=3, health=5, abilType="beforeAttack", abilBonus=-1, level=1, tier=2):
        super().__init__(name, id, attack, health, abilType, abilBonus, level, tier)
    def get_abilBonus(self, stage):
        elpos = None
        otherpos = None
        otherani = None
        for i, ani in enumerate(stage):
            if ani.get_name() == "elpht":
                elpos = i 
            if ani.get_name() in ["bfish", "camel"]:
                otherpos = i 
                otherani = ani
        if elpos is not None and otherpos is not None:
            if elpos > otherpos:
                return self.abilBonus * otherani.get_abilBonus()
        else:
            return self.abilBonus * self.level

class fish(aniFood):
    def __init__(self, name="fish", id=25, attack=2, health=2, abilType="levelUp", abilBonus=2, level=1, tier=1):
        super().__init__(name, id, attack, health, abilType, abilBonus, level, tier)
    def get_abilBonus(self, stage=None):
        if self.level == 3:
            return self.abilBonus * 2
        else:
            return self.abilBonus * self.level

class fly(aniFood):
    def __init__(self, name="fly", id=26, attack=5, health=5, abilType="friendFaints", abilBonus=10, level=1, tier=6):
        super().__init__(name, id, attack, health, abilType, abilBonus, level, tier)
    def get_abilBonus(self, stage=None):
        return self.abilBonus * self.level

class garlc(aniFood):
    def __init__(self, name="garlc", id=27, attack=0, health=0, abilType="defense", abilBonus=10, level=None, tier=3):
        super().__init__(name, id, attack, health, abilType, abilBonus, level, tier)

class goril(aniFood):
    def __init__(self, name="goril", id=28, attack=6, health=9, abilType="hurt", abilBonus=100, level=1, tier=6):
        super().__init__(name, id, attack, health, abilType, abilBonus, level, tier)
    def get_abilBonus(self, stage=None):
        return self.abilBonus * (self.health / 50)

class grafe(aniFood):
    def __init__(self, name="grafe", id=29, attack=2, health=5, abilType="endTurn", abilBonus=2, level=1, tier=3):
        super().__init__(name, id, attack, health, abilType, abilBonus, level, tier)
    def get_abilBonus(self, stage=None):
        return self.abilBonus * self.level
        
class hghog(aniFood):
    def __init__(self, name="hghog", id=30, attack=3, health=2, abilType="faint", abilBonus=2, level=1, tier=2):
        super().__init__(name, id, attack, health, abilType, abilBonus, level, tier)
    def get_abilBonus(self, stage=None):
        return self.abilBonus * self.level

class hippo(aniFood):
    def __init__(self, name="hippo", id=31, attack=4, health=7, abilType="knockout", abilBonus=6, level=1, tier=4):
        super().__init__(name, id, attack, health, abilType, abilBonus, level, tier)
    def get_abilBonus(self, stage=None):
        return self.abilBonus * self.level

class honey(aniFood):
    def __init__(self, name="honey", id=32, attack=0, health=0, abilType="summon", abilBonus=2, level=None, tier=1):
        super().__init__(name, id, attack, health, abilType, abilBonus, level, tier)
    def get_abilBonus(self, stage=None):
        return self.abilBonus

class horse(aniFood):
    def __init__(self, name="horse", id=33, attack=2, health=1, abilType="friendSummoned", abilBonus=1, level=1, tier=1):
        super().__init__(name, id, attack, health, abilType, abilBonus, level, tier)
    def get_abilBonus(self, stage=None):
        return self.abilBonus * self.level

class kanga(aniFood):
    def __init__(self, name="kanga", id=34, attack=1, health=2, abilType="friendAttacks", abilBonus=4, level=1, tier=3):
        super().__init__(name, id, attack, health, abilType, abilBonus, level, tier)
    def get_abilBonus(self, stage=None):
        return self.abilBonus * self.level

class leprd(aniFood):
    def __init__(self, name="leprd", id=35, attack=10, health=4, abilType="startOfBattle", abilBonus=None, level=1, tier=6):
        super().__init__(name, id, attack, health, abilType, abilBonus, level, tier)
    def get_abilBonus(self, stage=None):
        return int((self.attack * .5) * self.level)

class mamth(aniFood):
    def __init__(self, name="mamth", id=36, attack=3, health=10, abilType="faint", abilBonus=4, level=1, tier=6):
        super().__init__(name, id, attack, health, abilType, abilBonus, level, tier)
    def get_abilBonus(self, stage=None):
        return int(self.pos * self.abilBonus * self.level)
        
class meat(aniFood):
    def __init__(self, name="meat", id=37, attack=0, health=0, abilType="attack", abilBonus=5, level=1, tier=2):
        super().__init__(name, id, attack, health, abilType, abilBonus, level, tier)
    def get_abilBonus(self, stage=None):
        return self.abilBonus * self.level

class melon(aniFood):
    def __init__(self, name="melon", id=38, attack=0, health=0, abilType="health", abilBonus=20, level=1, tier=6):
        super().__init__(name, id, attack, health, abilType, abilBonus, level, tier)
    def get_abilBonus(self, stage=None):
        return self.abilBonus * self.level

class milk(aniFood):
    def __init__(self, name="milk", id=39, attack=0, health=0, abilType="attack", abilBonus=6, level=1, tier=1):
        super().__init__(name, id, attack, health, abilType, abilBonus, level, tier)
    def get_abilBonus(self, stage=None):
        return self.abilBonus * self.level


class mingo(aniFood):
    def __init__(self, name="mingo", id=40, attack=3, health=1, abilType="faint", abilBonus=2, level=1, tier=2):
        super().__init__(name, id, attack, health, abilType, abilBonus, level, tier)
    def get_abilBonus(self, stage=None):
        return self.abilBonus * self.level

class monky(aniFood):
    def __init__(self, name="monky", id=41, attack=1, health=2, abilType="endTurn", abilBonus=5, level=1, tier=5):
        super().__init__(name, id, attack, health, abilType, abilBonus, level, tier)
    def get_abilBonus(self, stage=None):
        return self.abilBonus * self.level

class mosqt(aniFood):
    def __init__(self, name="mosqt", id=42, attack=2, health=2, abilType="startOfBattle", abilBonus=1, level=1, tier=1):
        super().__init__(name, id, attack, health, abilType, abilBonus, level, tier)
    def get_abilBonus(self, stage=None):
        return self.abilBonus * self.level

class mushm(aniFood):
    def __init__(self, name="mushm", id=43, attack=0, health=0, abilType="extraLife", abilBonus=10, level=None, tier=6):
        super().__init__(name, id, attack, health, abilType, abilBonus, level, tier)

class otter(aniFood):
    def __init__(self, name="otter", id=44, attack=1, health=2, abilType="buy", abilBonus=2, level=1, tier=1):
        super().__init__(name, id, attack, health, abilType, abilBonus, level, tier)
    def get_abilBonus(self, stage=None):
        return self.abilBonus * self.level

class ox(aniFood):
    def __init__(self, name="ox", id=45, attack=1, health=3, abilType="friendAheadFaints", abilBonus=20, level=1, tier=3):
        super().__init__(name, id, attack, health, abilType, abilBonus, level, tier)
    def get_abilBonus(self, stage=None):
        return self.abilBonus * self.level

class parrt(aniFood):
    def __init__(self, name="parrt", id=46, attack=4, health=2, abilType="endTurn", abilBonus=1, level=1, tier=4):
        super().__init__(name, id, attack, health, abilType, abilBonus, level, tier)
    def get_abilBonus(self, stage=None):
        if self.pos and self.pos <= 3:
            friend_bonus = stage[self.pos + 1].get_abilBonus()
            return self.level * friend_bonus
        else:
            return 0

class pcock(aniFood):
    def __init__(self, name="pcock", id=47, attack=2, health=5, abilType="hurt", abilBonus=1, level=1, tier=1):
        super().__init__(name, id, attack, health, abilType, abilBonus, level, tier)
    def get_abilBonus(self, stage=None):
        return int((self.health / 50) * (self.attack + (self.attack * .5)) * self.level)

class pear(aniFood):
    def __init__(self, name="pear", id=48, attack=0, health=0, abilType="food", abilBonus=4, level=None, tier=4):
        super().__init__(name, id, attack, health, abilType, abilBonus, level, tier)

class pguin(aniFood):
    def __init__(self, name="pguin", id=49, attack=1, health=2, abilType="endTurn", abilBonus=2, level=1, tier=4):
        super().__init__(name, id, attack, health, abilType, abilBonus, level, tier)
    def get_abilBonus(self, stage=None):
        bonus = 0
        for ani in stage:
            if ani.get_level() >= 2:
                bonus += 1
        return bonus * self.abilBonus * self.level

class pig(aniFood):
    def __init__(self, name="pig", id=50, attack=4, health=1, abilType="sell", abilBonus=1, level=1, tier=1):
        super().__init__(name, id, attack, health, abilType, abilBonus, level, tier)
    def get_abilBonus(self, stage=None):
        return self.abilBonus * self.level

class pill(aniFood):
    def __init__(self, name="pill", id=51, attack=0, health=0, abilType="kill", abilBonus=0, level=1, tier=1):
        super().__init__(name, id, attack, health, abilType, abilBonus, level, tier)


class pizza(aniFood):
    def __init__(self, name="pizza", id=52, attack=2, health=2, abilType="food", abilBonus=4, level=1, tier=6):
        super().__init__(name, id, attack, health, abilType, abilBonus, level, tier)


class rabit(aniFood):
    def __init__(self, name="rabit", id=53, attack=1, health=2, abilType="petEatsFood", abilBonus=2, level=1, tier=3):
        super().__init__(name, id, attack, health, abilType, abilBonus, level, tier)
    def get_abilBonus(self, stage=None):
        return self.abilBonus * self.level

class rat(aniFood):
    def __init__(self, name="rat", id=54, attack=4, health=5, abilType="faint", abilBonus=-2, level=1, tier=2):
        super().__init__(name, id, attack, health, abilType, abilBonus, level, tier)
    def get_abilBonus(self, stage=None):
        return self.abilBonus * self.level

class rhino(aniFood):
    def __init__(self, name="rhino", id=55, attack=5, health=8, abilType="knockout", abilBonus=4, level=1, tier=5):
        super().__init__(name, id, attack, health, abilType, abilBonus, level, tier)
    def get_abilBonus(self, stage=None):
        return self.abilBonus * self.level

class roost(aniFood):
    def __init__(self, name="roost", id=56, attack=5, health=3, abilType="faint", abilBonus=1, level=1, tier=4):
        super().__init__(name, id, attack, health, abilType, abilBonus, level, tier)
    def get_abilBonus(self, stage=None):
        return int(self.attack * .5 * self.level + self.level)

class salad(aniFood):
    def __init__(self, name="salad", id=57, attack=0, health=0, abilType="food", abilBonus=4, level=1, tier=3):
        super().__init__(name, id, attack, health, abilType, abilBonus, level, tier)
    def get_abilBonus(self, stage=None):
        return self.abilBonus * self.level

class scorp(aniFood):
    def __init__(self, name="scorp", id=58, attack=1, health=1, abilType="death", abilBonus=50, level=1, tier=5):
        super().__init__(name, id, attack, health, abilType, abilBonus, level, tier)


class seal(aniFood):
    def __init__(self, name="seal", id=59, attack=3, health=8, abilType="knockout", abilBonus=4, level=1, tier=5):
        super().__init__(name, id, attack, health, abilType, abilBonus, level, tier)
    def get_abilBonus(self, stage=None):
        return self.abilBonus * self.level

class shark(aniFood):
    def __init__(self, name="shark", id=60, attack=4, health=4, abilType="friendFaints", abilBonus=4, level=1, tier=5):
        super().__init__(name, id, attack, health, abilType, abilBonus, level, tier)
    def get_abilBonus(self, stage=None):
        try:
            return int((4 - self.pos) * self.abilBonus)
        except:
            return int(4 * self.abilBonus)

class sheep(aniFood):
    def __init__(self, name="sheep", id=61, attack=2, health=2, abilType="faint", abilBonus=4, level=1, tier=3):
        super().__init__(name, id, attack, health, abilType, abilBonus, level, tier)
    def get_abilBonus(self, stage=None):
        return self.abilBonus * self.level

class shrmp(aniFood):
    def __init__(self, name="shrmp", id=62, attack=2, health=3, abilType="friendSold", abilBonus=1, level=1, tier=2):
        super().__init__(name, id, attack, health, abilType, abilBonus, level, tier)
    def get_abilBonus(self, stage=None):
        return self.abilBonus * self.level

class skunk(aniFood):
    def __init__(self, name="skunk", id=63, attack=3, health=6, abilType="startOfBattle", abilBonus=15, level=1, tier=4):
        super().__init__(name, id, attack, health, abilType, abilBonus, level, tier)
    def get_abilBonus(self, stage=None):
        return self.abilBonus * self.level

class snail(aniFood):
    def __init__(self, name="snail", id=64, attack=2, health=3, abilType="friendSold", abilBonus=1, level=1, tier=3):
        super().__init__(name, id, attack, health, abilType, abilBonus, level, tier)
    def get_abilBonus(self, stage=None):
        bonus = 0
        for ani in stage:
            if ani.get_name() not in ["none", "empty"]:
                bonus += 2

        return bonus

class snake(aniFood):
    def __init__(self, name="snake", id=65, attack=6, health=6, abilType="friendAheadAttacks", abilBonus=5, level=1, tier=1):
        super().__init__(name, id, attack, health, abilType, abilBonus, level, tier)
    def get_abilBonus(self, stage=None):
        return self.abilBonus * self.level

class spidr(aniFood):
    def __init__(self, name="spidr", id=66, attack=2, health=2, abilType="summon", abilBonus=2, level=1, tier=2):
        super().__init__(name, id, attack, health, abilType, abilBonus, level, tier)
    def get_abilBonus(self, stage=None):
        return self.abilBonus * self.level

class sqrrl(aniFood):
    def __init__(self, name="sqrrl", id=67, attack=2, health=5, abilType="startOfTurn", abilBonus=1, level=1, tier=4):
        super().__init__(name, id, attack, health, abilType, abilBonus, level, tier)
    def get_abilBonus(self, stage=None):
        return self.abilBonus * self.level

class steak(aniFood):
    def __init__(self, name="steak", id=68, attack=0, health=0, abilType="attack", abilBonus=20, level=1, tier=6):
        super().__init__(name, id, attack, health, abilType, abilBonus, level, tier)
    def get_abilBonus(self, stage=None):
        return self.abilBonus * self.level

class sushi(aniFood):
    def __init__(self, name="sushi", id=69, attack=0, health=0, abilType="attack", abilBonus=6, level=1, tier=5):
        super().__init__(name, id, attack, health, abilType, abilBonus, level, tier)
    def get_abilBonus(self, stage=None):
        return self.abilBonus * self.level

class swan(aniFood):
    def __init__(self, name="swan", id=70, attack=1, health=3, abilType="attack", abilBonus=6, level=1, tier=2):
        super().__init__(name, id, attack, health, abilType, abilBonus, level, tier)
    def get_abilBonus(self, stage=None):
        return self.abilBonus * self.level

class tiger(aniFood):
    def __init__(self, name="tiger", id=71, attack=4, health=3, abilType="friendAheadRepeats", abilBonus=6, level=1, tier=6):
        super().__init__(name, id, attack, health, abilType, abilBonus, level, tier)
    def get_abilBonus(self, stage=None):
        if self.pos and self.pos <= 3:
            return self.level * stage[self.pos + 1].get_abilBonus()
        else:
            return 0

class turky(aniFood):
    def __init__(self, name="turky", id=72, attack=3, health=4, abilType="friendSummoned", abilBonus=5, level=1, tier=6):
        super().__init__(name, id, attack, health, abilType, abilBonus, level, tier)
    def get_abilBonus(self, stage=None):
        try:
            return int(( 4 - self.pos )* self.abilBonus)
        except:
            return int(4 * self.abilBonus)

class turtl(aniFood):
    def __init__(self, name="turtl", id=73, attack=1, health=2, abilType="faint", abilBonus=20, level=1, tier=3):
        super().__init__(name, id, attack, health, abilType, abilBonus, level, tier)
    def get_abilBonus(self, stage=None):
        return self.abilBonus * self.level

# TODO: FIX MOST OF THEST!!!!!

class whale(aniFood):
    def __init__(self, name="whale", id=74, attack=3, health=8, abilType="faint", abilBonus=10, level=1, tier=4):
        super().__init__(name, id, attack, health, abilType, abilBonus, level, tier)
    def get_abilBonus(self, stage=None):
        return self.abilBonus * self.level

class worm(aniFood):
    def __init__(self, name="worm", id=75, attack=3, health=3, abilType="eatsFood", abilBonus=4, level=1, tier=4):
        super().__init__(name, id, attack, health, abilType, abilBonus, level, tier)
    def get_abilBonus(self, stage=None):
        return self.abilBonus * self.level


aniFoodMap = {
-1: empty,
 0: none,
 1: ant,
 2: apple,
 3: badgr,
 4: beavr,
 5: bfish,
 6: bison,
 7: boar,
 8:camel,
 9: can,
 10: cat,
 11: ccake,
 12: chili,
 13: choco,
 14: cow,
 15: crab,
 16: crikt,
 17: croc,
 18: deer,
 19: dlphn,
 20: dodo,
 21: dog,
 22: dragn,
 23: duck,
 24: elpht,
 25: fish,
 26: fly,
 27: garlc,
 28: goril,
 29: grafe,
 30: hghog,
 31: hippo,
 32: honey,
 33: horse,
 34: kanga,
 35: leprd,
 36: mamth,
 37: meat,
 38: melon,
 39: milk,
 40: mingo,
 41: monky,
 42: mosqt,
 43: mushm,
 44: otter,
 45: ox,
 46: parrt,
 47: pcock,
 48: pear,
 49: pguin,
 50: pig,
 51: pill,
 52: pizza,
 53: rabit,
 54: rat,
 55: rhino,
 56: roost,
 57: salad,
 58: scorp,
 59: seal,
 60: shark,
 61: sheep,
 62: shrmp,
 63: skunk,
 64: snail,
 65: snake,
 66: spidr,
 67: sqrrl,
 68: steak,
 69: sushi,
 70: swan,
 71: tiger,
 72: turky,
 73: turtl,
 74: whale,
 75: worm
}

def main():
    print("hello world")

    

    for k, v in aniFoodMap.items():
        ani = v()
        print(f"{ani}: {ani.get_name()}")


if __name__ == "__main__":
    main()