import numpy as np
import pygame
from pygame.time import Clock
from player import Player
from map import Map

# Title and icon
pygame.display.set_caption("Bomberman")
# icon = pygame.image.load()
# pygame.display.set_icon(icon)

##################### SETUP #####################
mapSize = (15, 15)
screenSize = (800, 800)
screenSize = (mapSize[0] * int(screenSize[0]/mapSize[0]), mapSize[1] * int(screenSize[1]/mapSize[1]))
#################################################

def play():
    # Initialize
    pygame.init()

    # Screen
    screen = pygame.display.set_mode(screenSize)

    # FPS
    FPS = 30
    clock = Clock()

    # Map
    map = Map(screen, mapSize)

    # Players
    map.addInstance(Player(screen, (1, 1), map.getWidthHeight(), "images/blue.png"))
    map.addInstance(Player(screen, (13, 13), map.getWidthHeight(), "images/red.png"))

    # Play loop
    while map.checkRunning():
        map.update()

        screen.fill((150, 150, 150))
        map.draw()

        pygame.display.update()
        clock.tick(FPS)

if __name__ == "__main__":
    play()