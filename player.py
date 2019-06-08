import pygame
from gameresources import *

class Player(object):

    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.vel = 5
        self.isJump = False
        self.jumpCount = 10
        self.left = False
        self.right = False
        self.walkCount = 0
        self.standing = True
        self.hitbox = (self.x + 17, self.y + 11, 29, 52)

    def draw(self,win):
        if self.walkCount + 1 >= 27:
            self.walkCount = 0

        if not self.standing:
            if self.left:
                win.blit(walkLeft[self.walkCount // 3], (self.x, self.y))
                self.walkCount += 1
            elif self.right:
                win.blit(walkRight[self.walkCount // 3], (self.x, self.y))
                self.walkCount += 1
        else:
            #win.blit(char, (self.x, self.y))
            if self.left:
                win.blit(walkLeft[0], (self.x, self.y))
            else:
                win.blit(walkRight[0], (self.x, self.y))

        self.hitbox = (self.x + 17, self.y + 11, 29, 52)
        #pygame.draw.rect(win, (255,0,0), self.hitbox, 2)

    def hit(self, x):
        self.x = x
        self.y = 410
        self.walkCount = 0
        self.isJump = False
        self.jumpCount = 10
        font1 = pygame.font.SysFont('comicsans', 100)
        text = font1.render('-5', 1, (255, 0, 0))
        win.blit(text, ((screensize_x/2) - (text.get_width()/2), (screensize_y/2) - (text.get_height()/2)))
        pygame.display.update()
        i=0
        while i < 300:
            pygame.time.delay(10)
            i+=1
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    i = 301
                    pygame.quit()