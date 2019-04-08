import random
import math
import Type
import Attack
import Ability
import Item
import pygame


class Monster:
    possible_attacks = {}

    def __init__(self, species, main_ability, type1, base_stats, level,
                 second_ability=None, hidden_ability=None, type2=None, moves=None, item=Item.empty,
                 ability=None):
        if random.randint(1, 4096) == 1:
            self.shiny = True
        else:
            self.shiny = False
        self.name = species
        self.abilities = [main_ability, second_ability] if second_ability is not None else [main_ability]
        self.HA = hidden_ability
        self.types = [type1, type2] if type2 is not None else [type1]
        self.base_stats = base_stats
        self.IVs = [random.randint(0, 31), random.randint(0, 31), random.randint(0, 31),
                    random.randint(0, 31), random.randint(0, 31), random.randint(0, 31)]
        self.EVs = [0, 0, 0, 0, 0, 0]
        self.level = level
        self.stats = [0, 0, 0, 0, 0, 0]
        self.stat_calc()
        self.friendship = 0.4
        self.attacks = {}
        self.temp_boosts = [1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0]
        if ability is None:
            ability = random.randint(1, 150)
            if ability == 1 and self.HA is not None:
                self.ability = self.HA
            else:
                self.ability = self.abilities[ability % len(self.abilities)]
        else:
            self.ability = ability
        self.status = "OK"
        self.temp_stats = [0, 0, 0, 0, 0, 0]
        for i in range(6):
            self.temp_stats[i] = self.stats[i]
        self.boosts = [1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0]
        self.items = [item]
        if moves is None:
            self.possibles = [x[1] for x in self.possible_attacks.items() if x[0] <= level]
            self.moves = random.sample(self.possibles, 4) if len(self.possibles) > 3 else self.possibles
        else:
            self.moves = moves
        for i in range(len(self.moves)):
            self.moves[i] = self.moves[i]()
        self.ability.passive(self)

    def stat_calc(self):
        self.stats[0] = math.floor(((self.base_stats[0]+self.IVs[0])*2 + math.floor(math.ceil(math.sqrt(self.EVs[0]))/4))*self.level/100)+self.level+10
        for i in range(1, 6):
            self.stats[i] = math.floor(((self.base_stats[i]+self.IVs[i])*2 + math.floor(math.ceil(math.sqrt(self.EVs[i]))/4))*self.level/100) + 5

    def __str__(self):
        to_str = self.name + " at level " + str(self.level)
        return to_str


class Fravicode(Monster):
    possible_attacks = {1: Attack.Pounce,
                        6: Attack.Patch,
                        7: Attack.Pixelate}

    def __init__(self, level, moves=None, ability=None):
        Monster.__init__(self, species="Fravicode", main_ability=Ability.connection, type1=Type.cyber,
                         base_stats=[55, 43, 47, 50, 53, 39], level=level, hidden_ability=Ability.wireless,
                         moves=moves, ability=ability)


class Larchanter(Monster):
    possible_attacks = {1: Attack.Slap}

    def __init__(self, level, moves=None, ability=None):
        Monster.__init__(self, species="Larchanter", main_ability=Ability.essence, type1=Type.magic,
                         base_stats=[46, 44, 42, 54, 45, 57], level=level, hidden_ability=Ability.magic_hat,
                         moves=moves, ability=ability, item=Item.candy_pile)
