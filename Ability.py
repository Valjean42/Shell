import Type
import Item


class Ability:
    def __init__(self, name, desc):
        self.name = name
        self.desc = desc

    def activate(self, user, targets, move, code):
        pass

    def passive(self, user):
        pass


class Essence(Ability):
    def __init__(self):
        Ability.__init__(self, "Essence", "Powers up magic-type moves in a pinch.")

    def activate(self, user, targets, move, code):
        if code == "attacking" and user.temp_stats[0] <= user.stats[0] / 3 and move.type == Type.magic:
            user.temp_stats[1] *= 1.5
            user.temp_stats[3] *= 1.5

    def passive(self, user):
        pass


class Connection(Ability):
    def __init__(self):
        Ability.__init__(self, "Connection", "Powers up cyber-type moves in a pinch.")

    def activate(self, user, targets, move, code):
        if code == "attacking" and user.temp_stats[0] <= user.stats[0] / 3 and move.type == Type.cyber:
            user.temp_stats[1] *= 1.5
            user.temp_stats[3] *= 1.5

    def passive(self, user):
        pass


class Wireless(Ability):
    def __init__(self):
        Ability.__init__(self, "Wireless", "The user keeps stat boosts when switching out.")

    def activate(self, user, targets, move, code):
        if code == "switch_out":
            for i in range(8):
                user.temp_boosts[i] = user.boosts[i]
        if code == "switch_in":
            for i in range(8):
                user.boosts[i] = user.temp_boosts[i]

    def passive(self, user):
        pass


class MagicHat(Ability):
    def __init__(self):
        Ability.__init__(self, "Magic hat", "The user has a magic hat, giving it space to hold one more item.")

    def activate(self, user, targets, move, code):
        pass

    def passive(self, user):
        user.items = [user.items[0], Item.empty]


essence = Essence()
wireless = Wireless()
connection = Connection()
magic_hat = MagicHat()
