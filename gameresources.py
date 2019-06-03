import pygame
pygame.init()
bg = pygame.image.load('resources/bg.jpg')
char = pygame.image.load('resources/standing.png')

walkRight = [pygame.image.load('resources/R1.png'), pygame.image.load('resources/R2.png'), pygame.image.load('resources/R3.png'), pygame.image.load('resources/R4.png'), pygame.image.load('resources/R5.png'), pygame.image.load('resources/R6.png'), pygame.image.load('resources/R7.png'), pygame.image.load('resources/R8.png'), pygame.image.load('resources/R9.png')]
walkLeft = [pygame.image.load('resources/L1.png'), pygame.image.load('resources/L2.png'), pygame.image.load('resources/L3.png'), pygame.image.load('resources/L4.png'), pygame.image.load('resources/L5.png'), pygame.image.load('resources/L6.png'), pygame.image.load('resources/L7.png'), pygame.image.load('resources/L8.png'), pygame.image.load('resources/L9.png')]


screensize_x = 500
screensize_y = 480

win = pygame.display.set_mode((screensize_x, screensize_y))
pygame.display.set_caption("My First Game")

bulletSound = pygame.mixer.Sound('resources/bullet.wav')
hitSound = pygame.mixer.Sound('resources/hit.wav')
music = pygame.mixer.music.load('resources/music.mp3')

class projectile(object):
    def __init__(self, x, y, radius, color, facing):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.facing = facing
        self.vel = 8 * facing

    def draw(self,win):
        pygame.draw.circle(win, self.color, (self.x, self.y), self.radius)
