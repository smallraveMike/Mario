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
coinRecs = []
eneRecs = []
font = pygame.font.Font('super-mario-bros-nes.ttf', 8)


grid = [[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2,2,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2,2,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,2,2,2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,3,0,0,0,0,0,0,0,0,0,0,0,0,1,0,3,0,2,2,2,2,2,2,2,2,2,2],
            [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1]]

class Mario:
    def __init__(self,speed,jumpHeight,weight):
        self.spr_stand = pygame.image.load('spr_stand.png')
        self.spr_run = pygame.image.load('spr_run.gif')
        self.spr_jump = pygame.image.load('spr_jump.png')
        self.snd_die = pygame.mixer.Sound('snd_die.mp3')
        self.grounded = False
        self.myX = 32
        self.myY = 120
        self.player_hitbox = Rect(self.myX, self.myY, 16, 16)
        self.player_hitbox_right = Rect(self.myX, self.myY, 16, 16)
        self.player_hitbox_bot = Rect(self.myX, self.myY, 16, 16)
        self.player_hitbox_left = Rect(self.myX, self.myY, 16, 16)
        self.player_hitbox_top = Rect(self.myX, self.myY, 16, 16)
        self.mySprite = self.spr_stand
        self.speed = speed
        self.jumpHeight = jumpHeight
        self.weight = weight
        self.accel = 0
        self.topSpeed = 2
        self.walkSpeed = 2
        self.runSpeed = 3.5
        self.fric = .1
        self.ySpeed = 0
        self.faceRight = True
        self.screen_scroll = 0
        self.coins = 0
        self.score = 0
        self.timer = 255
        self.dead = False

def updateMario(self):
    gameDisplay.blit(self.mySprite, (self.myX,self.myY))
    #pygame.draw.rect(gameDisplay,(0,0,0),self.player_hitbox)
    pygame.draw.rect(gameDisplay,(55,55,55),self.player_hitbox_top)

    if self.accel > self.topSpeed:
        self.accel = self.topSpeed
    elif self.accel < (-1 * self.topSpeed):
        self.accel = (-1* self.topSpeed)

    if (self.accel < .01) & (self.accel > -.01):
        self.accel = 0
    if self.ySpeed is not 0:
        self.mySprite = self.spr_jump
    elif self.accel is not 0:
        self.mySprite = self.spr_run
    else:
        self.mySprite = self.spr_stand

    print(f'{self.ySpeed},{self.grounded}')
    if self.faceRight:
        if self.accel < 0:
            self.faceRight = False
            self.mySprite = pygame.transform.flip(self.mySprite,True,False)
    else:
         if self.accel >= 0:
            self.faceRight = True
            self.mySprite = pygame.transform.flip(self.mySprite,True,False)

    self.player_hitbox = Rect(self.myX, self.myY, 16, 16)
    self.player_hitbox_bot = Rect(self.myX+2, self.myY+16, 13, 1)
    self.player_hitbox_right = Rect(self.myX+17, self.myY+8, 1, 1)
    self.player_hitbox_left = Rect(self.myX-1, self.myY+8, 1, 1)
    self.player_hitbox_top = Rect(self.myX+8, self.myY-3, 8, 1)

    deathBox = Rect(0, 224, 999999,16)

    if (not self.dead) & (pygame.Rect.colliderect(self.player_hitbox_top, deathBox)):
        self.dead = True
        self.snd_die.play(0)

    if self.dead:
        self.accel = 0

    if self.grounded:
        self.ySpeed = 0
        self.myY = round(self.myY/16) *16
    else:
        if self.ySpeed < self.weight:
            self.ySpeed += .1

    self.grounded = False
    for loc in levelRecs:
        if pygame.Rect.colliderect(self.player_hitbox_bot, loc):
            self.grounded = True
        if (self.accel > 0) & pygame.Rect.colliderect(self.player_hitbox_right, loc):
            self.accel = 0
        if (self.accel < 0) & pygame.Rect.colliderect(self.player_hitbox_left, loc):
            self.accel = 0
        if (self.ySpeed < 0) & pygame.Rect.colliderect(self.player_hitbox_top, loc):
            self.ySpeed = 0

    self.myY += (self.ySpeed * self.weight)

    if self.myX < 150:
        self.myX += self.accel
    elif (self.screen_scroll <= 0) & (self.accel < 0):
        self.myX += self.accel
        self.screen_scroll = 0
    else:
        self.myX = 150
        self.screen_scroll += self.accel

def drawHud(mario):
    hud = font.render('MARIO        WORLD    TIME', True, (255,255,255))
    hud2 = font.render(f'{mario.score:06d} ()x{mario.coins:02d}  1-1      {mario.timer:03d}', True, (255,255,255))
    gameDisplay.blit(hud,(24,8))
    gameDisplay.blit(hud2,(24,16))

def levelGrid(screen_scroll):
    spr_brick = pygame.image.load('spr_brick.png')
    levelRecs.clear()
    levelRecs.append(Rect(0,0,1,300))
    for Y in range(len(grid)):
        for X in range(len(grid[Y])):
            if grid[Y][X] == 1:
                gameDisplay.blit(spr_brick, ((X * 16)-screen_scroll,((Y *16))))         
                levelRecs.append(Rect((X*16)-screen_scroll, Y*16, 16, 16))
    #for hb in levelRecs:
       # pygame.draw.rect(gameDisplay,(255,255,255),hb)


def coinGrid(mario):
    snd_coin = pygame.mixer.Sound('snd_coin.mp3')
    spr_coin = pygame.image.load('spr_coin.gif')
    coinRecs.clear()
    for Y in range(len(grid)):
        for X in range(len(grid[Y])):
            if grid[Y][X] == 2:
                if pygame.Rect.colliderect(mario.player_hitbox, Rect((X*16)-mario.screen_scroll, Y*16, 16, 16)):
                    grid[Y][X] = 0
                    snd_coin.stop()
                    snd_coin.play(0)
                    mario.coins +=1
                    mario.score+=100
                gameDisplay.blit(spr_coin, ((X * 16)-mario.screen_scroll+3,((Y *16)-1)))         
                coinRecs.append(Rect((X*16)-mario.screen_scroll, Y*16, 16, 16))

class goomba:
    def __init__(self,X,Y,mario):
        self.squished = False
        self.snd_squish = pygame.mixer.Sound('smb_stomp.wav')
        self.spr_goom = pygame.image.load('spr_goom.gif')
        self.spr_goom_squish = pygame.image.load('spr_goom_squish.gif')
        self.mario = mario
        self.X = X
        self.Y = Y
        self.squishTimer = 0
        self.moveSpeed = .02

def updateGoomb(self):
    if pygame.Rect.colliderect(self.mario.player_hitbox_bot, Rect((self.X*16)-self.mario.screen_scroll, self.Y*16, 16, 16)):
                        if not self.squished:
                            self.snd_squish.stop()
                            self.snd_squish.play(0)
                            self.mario.score+=300
                            self.squished = True
                            self.mario.grounded = False
                            self.mario.ySpeed = abs(self.mario.ySpeed) * -3
    elif (pygame.Rect.colliderect(self.mario.player_hitbox_right, Rect((self.X*16)-self.mario.screen_scroll, self.Y*16, 16, 16))) | (pygame.Rect.colliderect(self.mario.player_hitbox_left, Rect((self.X*16)-self.mario.screen_scroll, self.Y*16, 16, 16))):
                        if not self.squished:
                            if not self.mario.dead:
                                self.mario.dead = True
                                self.mario.snd_die.play(0)

    if self.squished:
        if self.squishTimer < 60:
            self.squishTimer+=1

    if not self.squished:
        self.X += -.02
    
    if self.squishTimer < 60:
        if self.squished:
            gameDisplay.blit(self.spr_goom_squish, ((self.X * 16)-self.mario.screen_scroll,((self.Y *16)))) 
        else:
            gameDisplay.blit(self.spr_goom, ((self.X * 16)-self.mario.screen_scroll,((self.Y *16)))) 
    
        



def initalizeEnemies(mario):
    eneRecs.clear()
    for Y in range(len(grid)):
        for X in range(len(grid[Y])):
            if grid[Y][X] == 3:        
                eneRecs.append(goomba(X,Y,mario))

def main():
    tickDown = 0
    quit = False
    sysfont = pygame.font.get_default_font()
    bgm = pygame.mixer.Sound('snd_bgm.mp3')
    bgm.play(-1)
    snd_jump = pygame.mixer.Sound('snd_jump.mp3')
    me = Mario(.2,1.6,2)
    ene = initalizeEnemies(me)
    while not quit:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit = True
            pygame.event.pump()
        
        pressed = pygame.key.get_pressed()
        if pressed[pygame.K_d]:
                me.accel+=me.speed  
        elif pressed[pygame.K_a]:
                me.accel-=me.speed
        else:
            if me.accel > 0:
                me.accel -= me.fric
            elif me.accel < 0:
                me.accel += me.fric
        if (not me.dead) & pressed[pygame.K_SPACE]:
            if me.grounded:
                me.grounded = False
                snd_jump.stop()
                snd_jump.play(0)
                me.ySpeed -= me.jumpHeight
            print("held")
        if not pressed[pygame.K_SPACE]:
            if me.ySpeed < 0:
                me.ySpeed = 0
        if pressed[pygame.K_LSHIFT]:
            me.topSpeed = me.runSpeed
        else:
            me.topSpeed = me.walkSpeed
        if me.dead:
            bgm.stop()
        clock.tick(FPS)
        if tickDown < FPS:
            tickDown+=1
        else:
            me.timer-=1
            tickDown = 0
        pygame.draw.rect(gameDisplay,(99,134,250),Rect(0,0,300,300))
        levelGrid(me.screen_scroll)
        coinGrid(me)
        for e in eneRecs:
            updateGoomb(e)
        updateMario(me)
        drawHud(me)
        pygame.display.update()
main()