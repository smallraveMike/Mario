from venv import create
import pygame
from pygame.locals import *

pygame.init()
display_width = 256
display_height = 224
gameDisplay = pygame.display.set_mode((display_width,display_height))
pygame.display.set_caption('Super Mario')
clock = pygame.time.Clock()
FPS = 60
levelRecs = []

class Mario:
    def __init__(self,speed,jumpHeight,weight):
        self.spr_stand = pygame.image.load('spr_stand.png')
        self.spr_run = pygame.image.load('spr_run.gif')
        self.spr_jump = pygame.image.load('spr_jump.png')
        self.grounded = False
        self.myX = 0
        self.myY = 0
        self.player_hitbox = Rect(self.myX, self.myY, 16, 16)
        self.mySprite = self.spr_stand
        self.speed = speed
        self.jumpHeight = jumpHeight
        self.weight = weight
        self.accel = 0
        self.topSpeed = 2
        self.fric = .1
        self.ySpeed = 0
        self.faceRight = True

def updateMario(self):
    gameDisplay.blit(self.mySprite, (self.myX,self.myY))
    #pygame.draw.rect(gameDisplay,(0,0,0),self.player_hitbox)
    if (self.accel < .01) & (self.accel > -.01):
        self.accel = 0
    if self.ySpeed is not 0:
        self.mySprite = self.spr_jump
    elif self.accel is not 0:
        self.mySprite = self.spr_run
    else:
        self.mySprite = self.spr_stand

    print(f'{self.accel},{self.faceRight}')
    if self.faceRight:
        if self.accel < 0:
            self.faceRight = False
            self.mySprite = pygame.transform.flip(self.mySprite,True,False)
    else:
         if self.accel >= 0:
            self.faceRight = True
            self.mySprite = pygame.transform.flip(self.mySprite,True,False)

    self.player_hitbox = Rect(self.myX, self.myY, 16, 16)

    if self.grounded:
        self.ySpeed = 0
    else:
        if self.ySpeed < self.weight:
            self.ySpeed += .1

    self.grounded = False
    for loc in levelRecs:
        if pygame.Rect.colliderect(self.player_hitbox, loc):
            self.grounded = True
    
    self.myY += (self.ySpeed * self.weight)

    self.myX += self.accel

def levelGrid():
    spr_brick = pygame.image.load('spr_brick.png')
    grid = [[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,1,1,1,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]]
            
    for Y in range(len(grid)):
        for X in range(len(grid[Y])):
            if grid[Y][X] == 1:
                gameDisplay.blit(spr_brick, ((X * 16),((Y *16))))         
                levelRecs.append(Rect(X*16, Y*16, 16, 16))
    #for hb in levelRecs:
        #pygame.draw.rect(gameDisplay,(255,255,255),hb)


def main():
    quit = False
    sysfont = pygame.font.get_default_font()
    bgm = pygame.mixer.Sound('snd_bgm.mp3')
    bgm.play(-1)
    snd_jump = pygame.mixer.Sound('snd_jump.mp3')
    me = Mario(.2,5,2)
    while not quit:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit = True
            pygame.event.pump()
        
        pressed = pygame.key.get_pressed()
        if pressed[pygame.K_d]:
            if abs(me.accel) < me.topSpeed:
                me.accel+=me.speed  
        elif pressed[pygame.K_a]:
            if abs(me.accel) < me.topSpeed:
                me.accel-=me.speed
        else:
            if me.accel > 0:
                me.accel -= me.fric
            elif me.accel < 0:
                me.accel += me.fric
        if pressed[pygame.K_SPACE]:
            if me.grounded:
                me.grounded = False
                snd_jump.stop()
                snd_jump.play(0)
                me.ySpeed -= 1
        clock.tick(FPS)
        pygame.draw.rect(gameDisplay,(99,134,250),Rect(0,0,300,300))
        updateMario(me)
        levelGrid()
        pygame.display.update()
main()