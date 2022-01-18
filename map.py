import time

import numpy as np
import random
import pygame
from player import Player
from bomb import Bomb
from powerUp import PowerUp


# 0 - free field
# 1 - wall
# 2 - barrel
# 3 - bomb
# 4 - power up
# 5 - player

class Map:
    # Initilizing
    def __init__(self, screen, size):
        # Config
        self.running = True
        self.screen = screen
        self.cols = size[0]
        self.rows = size[1]
        self.height = int(screen.get_size()[1] / self.rows)
        self.width = int(screen.get_size()[0] / self.cols)
        self.events = None

        # Map
        self.map = None

        # Instances
        self.players = None
        self.bombs = None
        self.powerUps = None

        # Images
        self.wallImg = pygame.transform.scale(pygame.image.load("images/wall.png"), (self.width, self.height))
        self.barrelImg = pygame.transform.scale(pygame.image.load("images/barrel.png"), (self.width, self.height))

        # End
        self.finish = False
        self.start = None
        self.X, self.Y, self.dir = 1, 1, 1
        self.boundXL, self.boundXR, self.boundYT, self.boundYD = 1, self.cols - 2, 1, self.rows - 2
        self.fields = (self.cols - 1) * (self.rows - 1)
        self.drawTime = 2 * 1e9 / self.fields

        # Initializing functions
        self.__createMap()

    # Creating map
    def __createMap(self):
        self.map = np.zeros([self.height, self.width])
        for i, row in enumerate(self.map):
            for j, field in enumerate(row):
                if i == 0 or i == self.rows - 1:
                    self.map[i, j] = 1
                elif j == 0 or j == self.cols - 1:
                    self.map[i, j] = 1
                elif i % 2 == 0 and j % 2 == 0:
                    self.map[i, j] = 1
                elif not (
                        ((i == 1 or i == self.rows - 2) and (j <= 3 or j >= self.cols - 4)) or
                        ((j == 1 or j == self.cols - 2) and (i <= 3 or i >= self.rows - 4))
                ) and random.random() <= 0.9:
                    self.map[i, j] = 2

    # Checking if the field that player wants to move to is available
    def __playerMoveCheck(self, player, action):
        if not isinstance(action, bool):
            p = tuple(player.getPosition() + np.array(action))
            if self.map[p] != 0 and self.map[p] != 4 and self.map[p] != 5:
                return False
        return True

    # Checking player actions
    def __playerAction(self, nr):
        action = [0, 0]
        placeBomb = False
        for event in self.events:
            if event.type == pygame.QUIT:
                self.running = False
                return False
            if event.type == pygame.KEYDOWN:
                if nr == 0:
                    match event.key:
                        case pygame.K_a: action[0] = -1
                        case pygame.K_d: action[0] = 1
                        case pygame.K_w: action[1] = -1
                        case pygame.K_s: action[1] = 1
                        case pygame.K_SPACE: placeBomb = True
                        case _: pass
                if nr == 1:
                    match event.key:
                        case pygame.K_LEFT: action[0] = -1
                        case pygame.K_RIGHT: action[0] = 1
                        case pygame.K_UP: action[1] = -1
                        case pygame.K_DOWN: action[1] = 1
                        case pygame.K_RETURN: placeBomb = True
                        case _: pass
        if self.__playerMoveCheck(self.players[nr], action):
            if self.map[self.players[nr].getPosition()] != 3 and self.map[self.players[nr].getPosition()] != 1:
                self.map[self.players[nr].getPosition()] = 0
            else:
                placeBomb = False
            self.map[tuple(self.players[nr].getPosition() + np.array(action))] = 5
            return action, placeBomb
        return False

    # Find element in table by the position on the map
    def __find(self, array, field):
        if array is not None:
            for e in array:
                if np.array_equal(e.getPosition(), np.array(field)):
                    return e
        return None

    def __checkHit(self, explosionFields):
        for fields in explosionFields:
            for field in fields:
                player = self.__find(self.players, field)
                if player is not None:
                    player.hit()

    def __checkPowerUpPickUp(self):
        if self.powerUps is not None:
            for i, powerUp in enumerate(self.powerUps):
                player = self.__find(self.players, powerUp.getPosition())
                if player is not None:
                    player.upgrade(powerUp)
                    self.powerUps = np.delete(self.powerUps, i)


    # Checking the explosion fields
    # 0 - free field
    # 1 - wall
    # 2 - barrel
    # 3 - bomb
    # 4 - power up
    # 5 - player
    def __checkFields(self, dir, position, radius):
        result = []
        for i in range(1, radius+1):
            field = tuple(position + np.array(np.array(dir) * i))
            v = self.map[field]
            match v:
                case 0: result.append(field)
                case 1: break
                case 2:
                    result.append(field)
                    self.map[field] = 0
                    if random.random() < 0.25:
                        self.addInstance(PowerUp(field, self.getWidthHeight(), self.screen))
                    break
                case 3:
                    result.append(field)
                    self.__find(self.bombs, field).explode()
                case 4:
                    result.append(field)
                case 5:
                    result.append(field)
                    self.__find(self.players, field).hit()
        return result

    # Creating the explosion cross
    def __explosionFields(self, bomb):
        radius = bomb.getForce()
        center = bomb.getPosition()
        up = self.__checkFields([0, -1], center, radius)
        down = self.__checkFields([0, 1], center, radius)
        left = self.__checkFields([-1, 0], center, radius)
        right = self.__checkFields([1, 0], center, radius)
        return [center], up, down, left, right

    # Adding instance to the map's instance type list
    def __add(self, array, instance):
        if array is None:
            return np.array([instance])
        else:
            return np.append(array, [instance])

    # Checking the type of new instance
    def addInstance(self, instance):
        if isinstance(instance, Player):
            self.players = self.__add(self.players, instance)
            self.map[instance.getPosition()] = 5
        elif isinstance(instance, Bomb):
            self.bombs = self.__add(self.bombs, instance)
            self.map[instance.getPosition()] = 3
        elif isinstance(instance, PowerUp):
            self.powerUps = self.__add(self.powerUps, instance)
            self.map[instance.getPosition()] = 4

    # Updating status of the map
    def update(self):
        self.events = pygame.event.get()
        if self.bombs is not None:
            for bomb in self.bombs:
                bomb.update()
        if self.powerUps is not None:
            for powerUp in self.powerUps:
                powerUp.update()
        if self.players is not None:
            for i, player in enumerate(self.players):
                if player.death():
                    self.finish = True
                    self.start = time.time_ns()
                result = player.update(self.__playerAction(i))
                if isinstance(result, Bomb):
                    self.addInstance(result)
        self.__checkPowerUpPickUp()

    # Drawing map
    def draw(self):
        # Power ups
        if self.powerUps is not None:
            for powerUp in self.powerUps:
                powerUp.draw()

        # Bombs and explosion cross
        if self.bombs is not None:
            to_blow = []
            for i, bomb in enumerate(self.bombs):
                if bomb.draw():
                    if self.map[bomb.getPosition()] != 1:
                        self.map[bomb.getPosition()] = 0
                        end = False
                        if bomb.getExplosionFields() is None:
                            end = bomb.draw_explosion(self.__explosionFields(bomb))
                        else:
                            end = bomb.draw_explosion()
                        if end:
                            to_blow.append(i)
                        self.__checkHit(bomb.getExplosionFields())
            self.bombs = np.delete(self.bombs, to_blow)
        if self.players is not None:
            for player in self.players:
                player.draw()

        # Wall and barrels
        for i, row in enumerate(self.map):
            for j, field in enumerate(row):
                if self.map[i, j] == 1:
                    self.screen.blit(self.wallImg, (i * self.height, j * self.width))
                if self.map[i, j] == 2:
                    self.screen.blit(self.barrelImg, (i * self.height, j * self.width))

        # Finish wirl
        if self.fields == 0:
            self.running = False
        if self.finish:
            if time.time_ns() - self.start >= self.drawTime:
                self.start = time.time_ns()
                self.map[self.X, self.Y] = 1
                if self.dir == 1:
                    if self.X < self.boundXR:
                        self.X += self.dir
                    elif self.Y < self.boundYD:
                        self.Y += self.dir
                    else:
                        self.boundXR -= 1
                        self.boundYT += 1
                        self.dir *= -1
                else:
                    if self.X > self.boundXL:
                        self.X += self.dir
                    elif self.Y > self.boundYT:
                        self.Y += self.dir
                    else:
                        self.boundXL += 1
                        self.boundYD -= 1
                        self.dir *= -1
                self.fields -= 1

    def getWidthHeight(self):
        return (self.width, self.height)

    def checkRunning(self):
        return self.running