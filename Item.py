import math


class Item:
    def __init__(self, name, desc, effect):
        self.name = name
        self.desc = desc
        self.effect = effect

    def give(self, monster):
        if monster.items[0] is empty:
            monster.items[0] = self
        elif len(monster.items) == 2 and monster.items[1] is empty:
            monster.items[1] = self


class HeldItem(Item):
    def __init__(self, name, desc, effect, combat_effect):
        Item.__init__(self, name, desc, effect)
        self.combat_effect = combat_effect

    def combat_use(self, holder, code):
        if self.effect is not None:
            self.effect(holder, code)

    def __str__(self):
        return self.name


def candy_pile(holder, code):
    if code == "turn_end":
        print(holder.name + "'s candy pile healed a bit of HP!")
        holder.temp_stats[0] += math.floor(holder.stats[0] / 16)
        if holder.temp_stats[0] > holder.stats[0]:
            holder.temp_stats[0] = holder.stats[0]


candy_pile = HeldItem("candy pile", "The user holds a big candy pile, to restore a bit of hp each turn!", None, candy_pile)
empty = HeldItem("nothing", "The user has nothing in its hands!", None, None)
