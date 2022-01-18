import numpy as np
import pygame
import random

class PowerUp:
    def __init__(self, pos, imgSize, screen):
        # Config
        self.screen = screen
        self.imgSize = imgSize

        # Position
        self.pos = pos

        # Power
        self.power = self.powerType()

        # Images
        self.bombUp = pygame.transform.scale(pygame.image.load("images/powerUp_BombUp.png"), self.imgSize)
        self.bombDown = pygame.transform.scale(pygame.image.load("images/powerUp_BombDown.png"), self.imgSize)
        self.fireUp = pygame.transform.scale(pygame.image.load("images/powerUp_FireUp.png"), self.imgSize)
        self.fireDown = pygame.transform.scale(pygame.image.load("images/powerUp_FireDown.png"), self.imgSize)
        self.fasterBlow = pygame.transform.scale(pygame.image.load("images/powerUp_FasterBlow.png"), self.imgSize)
        self.longerBlow = pygame.transform.scale(pygame.image.load("images/powerUp_LongerBlow.png"), self.imgSize)

    def powerType(self):
        powers = ["bombUp", "bombDown", "fireUp", "fireDown", "fasterBlow", "longerBlow"]
        chance = random.random()
        if chance <= 0.1: return powers[0]
        elif chance <= 0.2: return powers[1]
        elif chance <= 0.4: return powers[2]
        elif chance <= 0.6: return powers[3]
        elif chance <= 0.8: return powers[4]
        else: return powers[5]

    def draw(self):
        match self.power:
            case "bombUp":
                self.screen.blit(self.bombUp, np.multiply(self.pos, self.imgSize))
            case "bombDown":
                self.screen.blit(self.bombDown, np.multiply(self.pos, self.imgSize))
            case "fireUp":
                self.screen.blit(self.fireUp, np.multiply(self.pos, self.imgSize))
            case "fireDown":
                self.screen.blit(self.fireDown, np.multiply(self.pos, self.imgSize))
            case "fasterBlow":
                self.screen.blit(self.fasterBlow, np.multiply(self.pos, self.imgSize))
            case "longerBlow":
                self.screen.blit(self.longerBlow, np.multiply(self.pos, self.imgSize))

    def getPosition(self):
        return self.pos

    def getPower(self):
        return self.power

    def update(self):
        pass