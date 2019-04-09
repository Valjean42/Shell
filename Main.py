import pygame
from Party import Party
import Monster
from Combat import Combat
import threading


def wait(mili):
    pygame.time.wait(mili)


def main():
    pygame.init()
    run = True
    bg = pygame.image.load("imgs/BG1.png")

    screen = pygame.display.set_mode((1920, 1080), flags=pygame.FULLSCREEN)

    screen.blit(bg, (0, 0))
    pygame.display.flip()
    while run:
        wait(20)
        keys = pygame.key.get_pressed()
        if keys[pygame.K_ESCAPE]:
            run = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                p1 = Party(Monster.Larchanter(100))
                p2 = Party(Monster.Larchanter(100))
                Combat(p1, p2, "normal", True, screen)
                screen.blit(bg, (0, 0))
                pygame.display.flip()



if __name__ == "__main__":
    main()
