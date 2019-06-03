import pygame as pygame

from gameresources import *

class Enemy(object):
    walkRightEnemy = [pygame.image.load('resources/R1E.png'), pygame.image.load('resources/R2E.png'),
                      pygame.image.load('resources/R3E.png'), pygame.image.load('resources/R4E.png'),
                      pygame.image.load('resources/R5E.png'), pygame.image.load('resources/R6E.png'),
                      pygame.image.load('resources/R7E.png'), pygame.image.load('resources/R8E.png'),
                      pygame.image.load('resources/R9E.png'), pygame.image.load('resources/R10E.png'),
                      pygame.image.load('resources/R11E.png')]
    walkLeftEnemy = [pygame.image.load('resources/L1E.png'), pygame.image.load('resources/L2E.png'),
                     pygame.image.load('resources/L3E.png'), pygame.image.load('resources/L4E.png'),
                     pygame.image.load('resources/L5E.png'), pygame.image.load('resources/L6E.png'),
                     pygame.image.load('resources/L7E.png'), pygame.image.load('resources/L8E.png'),
                     pygame.image.load('resources/L9E.png'), pygame.image.load('resources/L10E.png'),
                     pygame.image.load('resources/L11E.png')]

    def __init__(self, x, y, width, height, end):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.vel = 3
        self.end = end
        self.path = [0, self.end]
        self.walkCount = 0
        self.hitbox = (self.x + 17, self.y + 2, 31, 57)
        self.health = 10
        self.visible = True

    def draw(self,win):
        self.move()
        if self.visible:
            if self.walkCount + 1 >= 33:
                self.walkCount = 0

            if self.vel > 0:
                win.blit(self.walkRightEnemy[self.walkCount//3], (self.x, self.y))
                self.walkCount += 1
            else:
                win.blit(self.walkLeftEnemy[self.walkCount//3], (self.x, self.y))
                self.walkCount += 1

            pygame.draw.rect(win, (255, 0, 0), (self.hitbox[0], self.hitbox[1] - 20, 50, 10))
            pygame.draw.rect(win, (0, 255, 0), (self.hitbox[0], self.hitbox[1] - 20, 50 - ((50/10) * (10 - self.health)), 10))
            self.hitbox = (self.x + 17, self.y + 2, 31, 57)
            #pygame.draw.rect(win, (255, 0, 0), self.hitbox, 2)

    def move(self):
        if self.vel > 0:
            if self.x  + self.vel < self.path[1]:
                self.x += self.vel
            else:
                self.vel = self.vel * -1
                self.walkCount += 1
        else:
            if self.x - self.vel > self.path[0]:
                self.x += self.vel
            else:
                self.vel = self.vel * -1
                self.walkCount += 1

    def hit(self):
        if self.health > 0:
            self.health -=1
        else:
            self.visible = False
        hitSound.play()
        print('HIT')