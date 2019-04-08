from Party import Party
import Monster
import random
import pygame


class Combat:
    def __init__(self, party1, party2, weather, trainer, screen):
        self.is_trainer = trainer
        screen.blit(pygame.image.load("imgs/Combat_BG.png"), (0, 0))
        if party1.mons[0].shiny:
            screen.blit(pygame.image.load("imgs/" + party1.mons[0].name + "_back_shiny.png"), (150, 540))
        else:
            screen.blit(pygame.image.load("imgs/" + party1.mons[0].name + "_back_normal.png"), (150, 540))
        if party2.mons[0].shiny:
            screen.blit(pygame.image.load("imgs/" + party1.mons[0].name + "_front_shiny.png"), (1100, 200))
        else:
            screen.blit(pygame.image.load("imgs/" + party1.mons[0].name + "_front_normal.png"), (1100, 200))
        screen.blit(pygame.image.load("imgs/Textbox.png"), (0, 1080-261))
        self.battlers = {1: party1.mons[0], 2: party2.mons[0]}
        self.weather = weather
        if party1.mons[0].temp_stats[5] < party2.mons[0].temp_stats[5]:
            self.battlers = {2: party2.mons[0], 1:party1.mons[0]}
        if party1.mons[0].shiny:
            screen.blit()
        list(self.battlers.values())[0].ability.activate(list(self.battlers.values())[0], list(self.battlers.values())[1], None, "in")
        list(self.battlers.values())[1].ability.activate(list(self.battlers.values())[1], list(self.battlers.values())[0], None, "in")
        self.to_continue = True
        pygame.display.flip()
        self.turn(party1, party2, 1)
        
    def turn(self, party1, party2, amount):

        print("Your mon:")
        print(str(party1.mons[0]) + " at " + str(party1.mons[0].temp_stats[0]) + "/" + str(party1.mons[0].stats[0]))
        print("[" + str(party1.mons[0].boosts[1]) + " ATK, " + str(party1.mons[0].boosts[2]) + " DEF, "
              + str(party1.mons[0].boosts[3]) + " SPA, " + str(party1.mons[0].boosts[4]) + " SPD, "
              + str(party1.mons[0].boosts[5]) + " SPE]")
        print("Enemy mon:")
        print(str(party2.mons[0]) + " at " + str(party2.mons[0].temp_stats[0]) + "/" + str(party2.mons[0].stats[0]))
        print("[" + str(party2.mons[0].boosts[1]) + " ATK, " + str(party2.mons[0].boosts[2]) + " DEF, "
              + str(party2.mons[0].boosts[3]) + " SPA, " + str(party2.mons[0].boosts[4]) + " SPD, "
              + str(party2.mons[0].boosts[5]) + " SPE]")
        for i in range(1, 6):
            party1.mons[0].temp_stats[i] = party1.mons[0].stats[i] * party1.mons[0].boosts[i]
            party2.mons[0].temp_stats[i] = party2.mons[0].stats[i] * party2.mons[0].boosts[i]
        self.to_attack = True
        self.to_continue = True
        print("Attack(0), Switch(1), Item(2) (NYI) or Flee(3)?")
        action = int(input())
        if len(list(filter(None, party2.mons))) > 1:
            if not self.is_trainer:
                enemy_move = random.choice(self.battlers.get(2).moves + ["switch", "run"])
            else:
                print("yas")
                enemy_move = random.choice(self.battlers.get(2).moves + ["switch"])
        else:
            if not self.is_trainer:
                enemy_move = random.choice(self.battlers.get(2).moves + ["run"])
            else:
                enemy_move = random.choice(self.battlers.get(2).moves)
        if str(enemy_move) == "run":
            print("enemy ran!")
            self.to_continue = False
        elif action == 3:
            if not self.is_trainer:
                print("you ran!")
                self.to_continue = False
            else:
                print("Can't run from a trainer battle!")
        elif action == 1:
            self.player_switch(party1, party2)
            self.battlers = {1: party1.mons[0], 2: party2.mons[0]}
            if party1.mons[0].temp_stats[5] < party2.mons[0].temp_stats[5]:
                self.battlers = {2: party2.mons[0], 1: party1.mons[0]}
            if str(enemy_move) == "switch":
                self.ai_switch(party1, party2)
                self.battlers = {1: party1.mons[0], 2: party2.mons[0]}
                if party1.mons[0].temp_stats[5] < party2.mons[0].temp_stats[5]:
                    self.battlers = {2: party2.mons[0], 1: party1.mons[0]}
            else:
                print("The enemy attacks with " + str(enemy_move))
                if self.attack(party2.mons[0], enemy_move, party1.mons[0]) == "ded":
                    print("Your mon died")
                    if self.player_switch(party1, party2) == "able":
                        self.battlers = {1: party1.mons[0], 2: party2.mons[0]}
                        if party1.mons[0].temp_stats[5] < party2.mons[0].temp_stats[5]:
                            self.battlers = {2: party2.mons[0], 1: party1.mons[0]}
                    else:
                        print("you lost")
                        self.to_continue = False
        elif action == 0:
            print("Which move?")
            for i in range(len(self.battlers.get(1).moves)):
                print(self.battlers.get(1).moves[i].name + "? write " + str(i) + "!")
            num = int(input())
            player_move = self.battlers.get(1).moves[num]
            if str(enemy_move) == "switch":
                self.ai_switch(party1, party2)
                if self.attack(party1.mons[0], player_move, party2.mons[0]) == "ded":
                    print("The enemy died")
                    if self.ai_switch(party1, party2) == "able":
                        self.battlers = {1: party1.mons[0], 2: party2.mons[0]}
                        if party1.mons[0].temp_stats[5] < party2.mons[0].temp_stats[5]:
                            self.battlers = {2: party2.mons[0], 1: party1.mons[0]}
                    else:
                        print("you won!")
                        self.to_continue = False
            else:
                if list(self.battlers.keys())[0] == 2:
                    print("The enemy attacks with " + str(enemy_move))
                    if self.attack(party2.mons[0], enemy_move, party1.mons[0]) == "ded":
                        print("Your mon died")
                        if self.player_switch(party1, party2) == "able":
                            self.battlers = {1: party1.mons[0], 2: party2.mons[0]}
                            if party1.mons[0].temp_stats[5] < party2.mons[0].temp_stats[5]:
                                self.battlers = {2: party2.mons[0], 1: party1.mons[0]}
                            self.to_attack = False
                        else:
                            print("you lost")
                            self.to_continue = False
                    if self.to_continue and self.to_attack and self.attack(party1.mons[0], player_move, party2.mons[0]) == "ded":
                        print("The enemy died")
                        if self.ai_switch(party1, party2) == "able":
                            self.battlers = {1: party1.mons[0], 2: party2.mons[0]}
                            if party1.mons[0].temp_stats[5] < party2.mons[0].temp_stats[5]:
                                self.battlers = {2: party2.mons[0], 1: party1.mons[0]}
                        else:
                            print("you won!")
                            self.to_continue = False
                else:
                    if self.attack(party1.mons[0], player_move, party2.mons[0]) == "ded":
                        print("The enemy died")
                        if self.ai_switch(party1, party2) == "able":
                            self.battlers = {1: party1.mons[0], 2: party2.mons[0]}
                            if party1.mons[0].temp_stats[5] < party2.mons[0].temp_stats[5]:
                                self.battlers = {2: party2.mons[0], 1: party1.mons[0]}
                            self.to_attack = False
                        else:
                            print("you won!")
                            self.to_continue = False
                    else:
                        print("The enemy attacks with " + str(enemy_move))
                        if self.to_continue and self.to_attack and self.attack(party2.mons[0], enemy_move, party1.mons[0]) == "ded":
                            print("Your mon died")
                            if self.player_switch(party1, party2) == "able":
                                self.battlers = {1: party1.mons[0], 2: party2.mons[0]}
                                if party1.mons[0].temp_stats[5] < party2.mons[0].temp_stats[5]:
                                    self.battlers = {2: party2.mons[0], 1: party1.mons[0]}
                            else:
                                print("you lost")
                                self.to_continue = False
        if self.to_continue:
            for item in party1.mons[0].items:
                item.combat_use(party1.mons[0], "turn_end")
            for item in party2.mons[0].items:
                item.combat_use(party2.mons[0], "turn_end")
            self.turn(party1, party2, amount + 1)

    def ai_switch(self, party1, party2):
        try:
            available_mons = []
            for i in range(1, 5):
                if party2.mons[i] is not None and party2.mons[i].temp_stats[0] > 0:
                    available_mons.append(i+1)
            if available_mons is []:
                raise Exception
            party2.mons[0].ability.activate(party2.mons[0], party1.mons[0], None, "switch_out")
            party2.mons[0].boosts = [1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0]
            party2.switch(1, random.choice(available_mons))
            party2.mons[0].ability.activate(party2.mons[0], party1.mons[0], None, "switch_in")
            print("Enemy switches to " + str(party2.mons[0]))
            self.battlers = {1: party1.mons[0], 2: party2.mons[0]}
            if party1.mons[0].temp_stats[5] < party2.mons[0].temp_stats[5]:
                self.battlers = {2: party2.mons[0], 1: party1.mons[0]}
            list(self.battlers.values())[0].ability.activate(list(self.battlers.values())[0], list(self.battlers.values())[1], "switch", "in")
            return "able"
        except Exception:
            return "unable"

    def player_switch(self, party1, party2):
        try:
            print("Which number of mon do you want to switch to?")
            for i in range(2, len(list(filter(lambda x: x is not None and x.temp_stats[0] > 0, party1.mons))) + 1):
                print(str(party1.mons[i - 1]) + "? write " + str(i) + "!")
            num = int(input())
            party1.mons[0].ability.activate(party1.mons[0], party2.mons[0], None, "switch_out")
            party1.mons[0].boosts = [1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0]
            party1.switch(1, num)
            party1.mons[0].ability.activate(party1.mons[0], party2.mons[0], None, "switch_in")
            self.battlers = {1: party1.mons[0], 2: party2.mons[0]}
            if party1.mons[0].temp_stats[5] < party2.mons[0].temp_stats[5]:
                self.battlers = {2: party2.mons[0], 1: party1.mons[0]}
            print("You switch to " + str(party1.mons[0]))
            return "able"
        except Exception:
            print("couldnt switch!")
            return "unable"

    def attack(self, user, move, target):
        if random.random() <= move.accuracy * user.boosts[6] / target.boosts[7]:
            user.ability.activate(user, target, move, "attacking")
            target.ability.activate(target, user, move, "defending")
            return move.use(user, target, self.weather)
        else:
            print("but it missed!")
            return "miss"
        
        
if __name__ == "__main__":
    p1 = Party(Monster.Fravicode(100))
    p2 = Party(Monster.Larchanter(100))
    Combat(p1, p2, "normal", True)
