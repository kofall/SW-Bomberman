import math
import time
import numpy as np
import pygame
from bomb import Bomb
from powerUp import PowerUp


class Player:
    def __init__(self, screen, pos, imgSize, playerImg):
        # Config
        self.screen = screen
        self.imgSize = imgSize

        # Images
        self.playerImg = pygame.transform.scale(pygame.image.load(playerImg), self.imgSize)

        # Position
        self.pos = pos

        # Status
        self.hp = 3
        self.speed = 1
        self.bombs = np.full([1], None)
        self.bombTimer = 3
        self.force = 2
        self.gotHit = False
        self.start = None
        self.duration = 3

    def __move(self, movement):
        self.pos = tuple(self.pos + np.array(movement))

    def __placeBomb(self):
        for i, bomb in enumerate(self.bombs):
            if bomb is None and self.pos not in self.bombs:
                self.bombs[i] = self.pos
                return Bomb(self, self.pos, self.force, self.bombTimer, self.imgSize, self.screen)
        return False

    def __shift(self, x, a, b, c, d):
        return c + (d - c) / (b - a) * (x - a)

    def death(self):
        return self.hp <= 0

    def upgrade(self, powerUp):
        match powerUp.getPower():
            case "bombUp":
                self.bombs = np.append(self.bombs, None)
            case "bombDown":
                if self.bombs.size > 1:
                    self.bombs = np.delete(self.bombs, self.bombs.size - 1)
            case "fireUp":
                self.force += 1
            case "fireDown":
                if self.force > 1:
                    self.force -= 1
            case "fasterBlow":
                if self.bombTimer > 1:
                    self.bombTimer -= self.bombTimer * 0.1
            case "longerBlow":
                self.bombTimer += self.bombTimer * 0.1

    def hit(self):
        if not self.gotHit:
            self.gotHit = True
            self.start = time.time()
            self.hp -= 1

    def draw(self):
        if not self.gotHit:
            self.playerImg.set_alpha(1000)
        elif time.time() - self.start >= self.duration:
            self.gotHit = False
        else:
            self.playerImg.set_alpha(self.__shift((1 + math.sin(15 * (time.time() - self.start)))/2, 0, 1, 0, 1000))

        self.screen.blit(self.playerImg, np.multiply(self.pos, self.imgSize))

    def getPosition(self):
        return self.pos

    def bombExploded(self, bomb):
        if self.bombs is not None:
            for i, position in enumerate(self.bombs):
                if np.array_equal(np.array(position), np.array(bomb.getPosition())):
                    self.bombs[i] = None

    def update(self, action):
        if not isinstance(action, bool):
            self.__move(action[0])
            if action[1]:
                return self.__placeBomb()
        return True