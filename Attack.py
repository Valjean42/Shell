import random
import Type
import math
STATS = ["HP", "ATK", "DEF", "SPA", "SPD", "SPE", "ACC", "EVA"]


def stat_change(mon, stat, change):
    if stat < 6:
        if change>0:
            for i in range(change):
                if mon.boosts[stat] == 4.0:
                    print(mon.name + "'s " + STATS[stat] + " can't go any higher!")
                    break
                elif mon.boosts[stat] < 1.0:
                    mon.boosts[stat] = 1.0/((1.0/mon.boosts[stat]) + 0.5)
                    print("Raised " + mon.name + "'s " + STATS[stat])
                else:
                    mon.boosts[stat] += 0.5
                    print("Raised " + mon.name + "'s " + STATS[stat])
        else:
            for i in range((-1)*change):
                if mon.boosts[stat] == 0.25:
                    print(mon.name + "'s " + STATS[stat] + " can't go any lower!")
                    break
                elif mon.boosts[stat] < 1.0:
                    mon.boosts[stat] = 1.0/((1.0/mon.boosts[stat]) - 0.5)
                    print("Lowered " + mon.name + "'s " + STATS[stat])
                else:
                    mon.boosts[stat] -= 0.5
                    print("Lowered " + mon.name + "'s " + STATS[stat])
    else:
        if change>0:
            for i in range(change):
                if mon.boosts[stat] == 3.0:
                    print(mon.name + "'s " + STATS[stat] + " can't go any higher!")
                    break
                elif mon.boosts[stat] < 1.0:
                    mon.boosts[stat] = 3.0/(((1.0/mon.boosts[stat]) * 3.0) + 1.0)
                    print("Raised " + mon.name + "'s " + STATS[stat])
                else:
                    mon.boosts[stat] += 1.0/3.0
                    print("Raised " + mon.name + "'s " + STATS[stat])
        else:
            for i in range((-1)*change):
                if mon.boosts[stat] == 1.0/3.0:
                    print(mon.name + "'s " + STATS[stat] + " can't go any lower!")
                    break
                elif mon.boosts[stat] < 1.0:
                    mon.boosts[stat] = 3.0/(((1.0/mon.boosts[stat]) * 3.0) - 1.0)
                    print("Lowered " + mon.name + "'s " + STATS[stat])
                else:
                    mon.boosts[stat] -= 1.0/3.0
                    print("Lowered " + mon.name + "'s " + STATS[stat])


class Attack:
    def __init__(self, name, type1, power, accuracy, desc, additions, targets, priority, kind, max_pp):
        self.name = name
        self.type = type1
        self.power = power
        self.accuracy = accuracy
        self.desc = desc
        self.additions = additions
        self.priority = priority
        self.targets = targets
        self.kind = kind
        self.max_pp = max_pp
        self.current_pp = max_pp

    def calc_eff(self, defender):
        modifier = 1
        if self.type in defender.types[0].weaknesses:
            modifier *= 2
        if self.type in defender.types[0].strengths:
            modifier /= 2
        if self.type in defender.types[0].immunities:
            modifier = 0
        if len(defender.types) == 2:
            if self.type in defender.types[1].weaknesses:
                modifier *= 2
            if self.type in defender.types[1].strengths:
                modifier /= 2
            if self.type in defender.types[1].immunities:
                modifier = 0
        return modifier

    def use(self, user, target,  weather):
        self.current_pp -= 1
        if random.randint(1, 100) <= self.accuracy:
            return self.dmg_calc(user, target, weather)
        else:
            print("The attack missed!")

    def dmg_calc(self, attacker, defender, weather):
        crit = random.randint(1, 24)
        modifier = 1.0
        if crit == 1 or (crit == 2 and attacker.friendship == 1):
            print("It's a critical hit!")
            modifier *= 1.5
        if self.targets > 1:
            modifier *= 0.75
        modifier *= random.randint(85, 100)/100
        if self.type in attacker.types:
            modifier *= 1.5
        if defender.status == "Symphonized":
            modifier /= 0.75
        if attacker.status == "Symphonized":
            modifier *= 0.75
        effectiveness = self.calc_eff(defender)
        modifier *= effectiveness
        if effectiveness < 1:
            print("It's not very effective")
        elif effectiveness > 1:
            print("It's super effective")
        if self.kind == "physical":
            damage = (((2 * attacker.level / 5) + 2) * self.power * attacker.temp_stats[1] / (defender.temp_stats[2] * 50)) * modifier
        else:
            damage = (((2 * attacker.level / 5) + 2) * self.power * attacker.temp_stats[3] / (defender.temp_stats[4] * 50)) * modifier
        damage = math.floor(damage) + 1
        print(str(attacker) + " attacks for " + str(damage) + " damage!")
        defender.temp_stats[0] -= damage
        if self.additions is not None:
            self.additions(damage, attacker, defender, weather)
        if defender.temp_stats[0] <= 0:
            defender.temp_stats[0] = 0
            return "ded"
        else:
            return "not"

    def __str__(self):
        return self.name


class StatusAttack(Attack):
    def __init__(self, name, type1, accuracy, desc, additions, targets, priority, max_pp):
        Attack.__init__(self, name, type1, 0, accuracy, desc, additions, targets, priority, "status", max_pp)

    def use(self, user, target,  weather):
        self.current_pp -= 1
        if target == 0 or random.randint(1, 100) <= 100:
            self.additions(0, user, target, weather)
        else:
            print("But it failed!")


class Pounce(Attack):
    def __init__(self):
        Attack.__init__(self, "Pounce", Type.basic, 40, 100, "The user pounces on the enemy", None, 1, 0, "physical", 35)


class Patch(StatusAttack):
    def patch(self, damage, user, target, weather):
        stat_change(user, 4, 1)

    def __init__(self):
        StatusAttack.__init__(self, "Patch", Type.cyber, 100, "The user downloads a patch, which lowers incoming damage.", self.patch, 0, 0, 40)


class Pixelate(Attack):
    def __init__(self):
        Attack.__init__(self, "Pixelate", Type.cyber, 45, 100, "The user makes the opponent lose their 3rd dimension.", None, 1, 0, "special", 25)


class Slap(Attack):
    def __init__(self):
        Attack.__init__(self, "Slap", Type.basic, 40, 100, "The user slaps the enemy", None, 1, 0, "physical", 35)