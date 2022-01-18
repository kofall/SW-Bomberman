import time
import numpy as np
import pygame


class Bomb:
    def __init__(self, owner, pos, force, bombTimer, imgSize, screen):
        # Config
        self.owner = owner
        self.screen = screen
        self.imgSize = imgSize
        self.force = force

        # Images
        self.bombImg = pygame.transform.scale(pygame.image.load("images/bomb.png"), self.imgSize)
        blowCenter = pygame.transform.scale(pygame.image.load("images/blow_center.png"), self.imgSize)
        blowUp = pygame.transform.scale(pygame.image.load("images/blow_up.png"), self.imgSize)
        blowDown = pygame.transform.scale(pygame.image.load("images/blow_down.png"), self.imgSize)
        blowLeft = pygame.transform.scale(pygame.image.load("images/blow_left.png"), self.imgSize)
        blowRight = pygame.transform.scale(pygame.image.load("images/blow_right.png"), self.imgSize)
        self.blowImages = [blowCenter, blowUp, blowDown, blowLeft, blowRight]
        # Position
        self.pos = pos

        # Status
        self.start = time.time()
        self.timer = bombTimer
        self.explosion_time = 2
        self.explosion = False
        self.explosionFields = None

    def draw(self):
        if self.explosion:
            return True
        self.screen.blit(self.bombImg, np.multiply(self.pos, self.imgSize))
        return False

    def draw_explosion(self, fields=True):
        if self.explosionFields is None:
            self.explosionFields = fields

        for i, fields in enumerate(self.explosionFields):
            for field in fields:
                self.screen.blit(self.blowImages[i], np.multiply(field, self.imgSize))

        if time.time() - self.start >= self.explosion_time:
            return True
        return False

    def getPosition(self):
        return self.pos

    def getForce(self):
        return self.force

    def getOwner(self):
        return self.owenr

    def getExplosionFields(self):
        return self.explosionFields

    def explode(self):
        self.owner.bombExploded(self)
        self.start = time.time()
        self.explosion = True

    def update(self):
        if not self.explosion and time.time() - self.start >= self.timer:
            self.explode()