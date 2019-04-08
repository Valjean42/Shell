import pygame
import os


class Type:
    def __init__(self, name, num):
        self.name = name
        self.strengths = []
        self.weaknesses = []
        self.immunities = []
        self.num = num

    def add_weaknesses(self, weaknesses):
        '''
        Adds the type's weaknesses: if a monster has this type,
        it will receive X2 damage from attacks with one of these types.
        '''
        for weakness in weaknesses:
            self.weaknesses.append(weakness)

    def add_strengths(self, strengths):
        '''
        Adds the type's strengths: if a monster has this type,
        it will receive /2 damage from attacks with one of these types.
        '''
        for strength in strengths:
            self.strengths.append(strength)

    def add_immunities(self, immunities):
        '''
        Adds the type's immunities: if a monster has this type,
        it will receive NO damage from attacks with one of these types.
        '''
        for immunity in immunities:
            self.immunities.append(immunity)

    def get_sprite(self):
        return pygame.Surface.subsurface(types, pygame.Rect(0, 24*(self.num-1), 64, 24))


types = pygame.image.load(os.path.join('imgs', 'types.png'))
cyber = Type("Cyber", 1)
magic = Type("Magic", 2)
beast = Type("Beast", 3)
light = Type("Light", 4)
sweet = Type("Sweet", 5)
music = Type("Music", 6)
energy = Type("Energy", 7)
void = Type("Void", 8)
luck = Type("Luck", 9)
mind = Type("Mind", 10)
gem = Type("Gem", 11)
alien = Type("Alien", 12)
color = Type("Color", 13)
basic = Type("Basic", 14)
cyber.add_strengths([cyber, magic, beast, mind, color])
cyber.add_weaknesses([music, energy, luck, gem, alien])
magic.add_strengths([beast, luck, gem, alien])
magic.add_weaknesses([cyber, light, mind])
beast.add_strengths([sweet, mind, color])
beast.add_weaknesses([cyber, magic, beast, light, alien])
beast.add_immunities([music])
light.add_strengths([beast, energy, alien])
light.add_weaknesses([music, mind, gem, color])
sweet.add_strengths([sweet])
sweet.add_weaknesses([beast, gem])
music.add_strengths([music, gem])
music.add_weaknesses([energy, luck, mind, color])
energy.add_strengths([cyber, luck, alien])
energy.add_weaknesses([light, sweet, energy])
void.add_strengths([energy])
void.add_weaknesses([magic, light, music, alien])
void.add_immunities([beast, sweet, gem, color, basic])
luck.add_strengths([magic])
luck.add_weaknesses([sweet, luck, mind, alien])
mind.add_strengths([music, energy, luck, mind])
mind.add_weaknesses([cyber, magic, light, alien, color])
gem.add_strengths([magic, light, sweet, luck, mind, color])
gem.add_weaknesses([music, energy, gem, alien])
alien.add_strengths([cyber, light, mind])
alien.add_weaknesses([magic, beast, sweet, energy, luck, color])
color.add_strengths([mind, alien, color])
color.add_weaknesses([light, sweet, music, gem])
basic.add_weaknesses([beast])
