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
koopRecs = []
blockRec = []
font = pygame.font.Font('super-mario-bros-nes.ttf', 8)


grid =     [[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,'c'],
            [0,0,'c',0,0,0,0,0,0,0,0,0,'c',0,0,0,0,0,0,0,0,'c',0,0,0,0],
            [0,0,0,0,0,0,0,'c',0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,'c',0,0,0,0,0,0,0,'c'],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2,2,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2,2,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,2,2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,4,1,1,1,0,0,0,0,0,'t',0,0,0,0,0,0,2,0,0,0,0,0,0,0,4,0,0,0,0,0,4,0,0,4,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,'p',0,0,0,0,0,2,1,2,0,0,0,0,0,0,0,0,0,'t'],
            [0,0,0,0,'h',0,0,0,0,3,'d',0,0,0,0,0,'p',0,0,0,0,0,2,'h',0,0,2,3,0,'d',0,0,0,0,'p',0,0,0,1,0,0,0,0,5,0,0,0,1],
            [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]]

class ItemBlock:
    def __init__(self,item,amt,x,y,type,mario):
        self.item = item
        self.amount = amt
        self.x = x
        self.y = y
        self.tickTest = 0
        self.smackY = 0
        self.upMode = False
        self.mario = mario
        self.snd_coin = pygame.mixer.Sound('snd_coin.mp3')
        self.myHitbox = Rect(self.x, self.y, 16, 16)
        self.empty = True
        if type == 'question':
            self.mySprite = pygame.image.load('spr_block_que.png')
        if type == 'brick':
            self.mySprite = pygame.image.load('spr_brick.png')
        if self.item == 'coin':    
            self.itemSprite1 = pygame.image.load('spr_spin_coin1.png')
            self.itemSprite2 = pygame.image.load('spr_spin_coin2.png')
            self.itemSprite3 = pygame.image.load('spr_spin_coin3.png')
            self.itemSprite4 = pygame.image.load('spr_spin_coin4.png')
            self.itemSprite = [self.itemSprite1,self.itemSprite1,self.itemSprite2,self.itemSprite2,self.itemSprite3,self.itemSprite3,self.itemSprite4,self.itemSprite4,self.itemSprite4]

def updateBlocks(block):
    block.myHitbox = Rect(block.x-block.mario.screen_scroll, block.y, 16, 16)
    gameDisplay.blit(block.mySprite, ((block.x)-block.mario.screen_scroll,((block.y)+block.smackY)))
    #pygame.draw.rect(gameDisplay,(124,24,124),block.myHitbox)
    if block.upMode:
        if block.smackY > -8:
            block.smackY -= 1
        else:
            block.upMode = False    
    elif block.smackY < 0:
        block.smackY += 1
    if block.amount > 0:
        if ((block.mario.ySpeed < 0) & (pygame.Rect.colliderect(block.myHitbox, block.mario.player_hitbox_top))):
            block.snd_coin.play(0)
            block.upMode = True
            block.mario.snd_bump.play(0)
            block.mario.ySpeed = 0
            block.amount-=1
            block.mario.coins+=1
            block.mario.score+=100
    elif ((block.mario.ySpeed < 0) & (pygame.Rect.colliderect(block.myHitbox, block.mario.player_hitbox_top))):
        block.mario.ySpeed = 0
        block.mario.snd_bump.play(0)
    if block.smackY != 0:
        gameDisplay.blit(block.itemSprite[abs(block.smackY)], ((block.x)-block.mario.screen_scroll+4,((block.y)-16+(block.smackY*4))))

    

class Mario:
    def __init__(self,speed,jumpHeight,weight):
        self.spr_stand = pygame.image.load('spr_stand.png')
        self.spr_run = pygame.image.load('spr_run.gif')
        self.spr_run_1 = pygame.image.load('spr_run_1.png')
        self.spr_run_2 = pygame.image.load('spr_run_2.png')
        self.spr_run_3 = pygame.image.load('spr_run_3.png')
        self.run_ani = [self.spr_run_1,self.spr_run_2,self.spr_run_3]
        self.spr_jump = pygame.image.load('spr_jump.png')
        self.spr_dead = pygame.image.load('spr_dead.png')
        self.snd_die = pygame.mixer.Sound('snd_die.mp3')
        self.snd_bump = pygame.mixer.Sound('snd_bump.wav')
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
        self.deadTimer = 0
        self.sprite_index = 0
        self.my_ani = self.run_ani
        self.ticks = 0

def updateMario(self):
    if self.ticks < 60:
        self.ticks+=1
    else:
        self.ticks = 0
    gameDisplay.blit(self.mySprite, (self.myX,self.myY))
    #pygame.draw.rect(gameDisplay,(0,0,0),self.player_hitbox)
    pygame.draw.rect(gameDisplay,(55,55,55),self.player_hitbox_left)
    if self.ySpeed < -1 *self.jumpHeight:
        self.ySpeed = -1* self.jumpHeight

    if self.accel > self.topSpeed:
        self.accel = self.topSpeed
    elif self.accel < (-1 * self.topSpeed):
        self.accel = (-1* self.topSpeed)

    if (self.accel < .01) & (self.accel > -.01):
        self.accel = 0
    
    if self.dead:
        self.mySprite = self.spr_dead
    elif self.ySpeed is not 0:
        self.mySprite = self.spr_jump
    elif self.accel is not 0:
        self.mySprite = self.spr_run
    else:
        self.mySprite = self.spr_stand

    if self.mySprite == self.spr_run:
        self.mySprite = self.run_ani[self.sprite_index]

    if self.faceRight:
        if self.accel < 0:
            self.faceRight = False
    else:
        if self.accel > 0:
            self.faceRight = True
    
    self.mySprite_flipped = pygame.transform.flip(self.mySprite,True,False)

    if self.faceRight == False:
        self.mySprite = self.mySprite_flipped

    self.player_hitbox = Rect(self.myX, self.myY, 14, 16)
    self.player_hitbox_bot = Rect(self.myX+2, self.myY+16, 8, 8)
    self.player_hitbox_right = Rect(self.myX+14, self.myY+8, 1, 1)
    self.player_hitbox_left = Rect(self.myX, self.myY+8, 1, 1)
    self.player_hitbox_top = Rect(self.myX+4, self.myY-3, 4, 1)

    deathBox = Rect(0, 284, 999999,16)

    if (not self.dead) & (pygame.Rect.colliderect(self.player_hitbox_top, deathBox)):
        self.dead = True
        self.snd_die.play(0)

    if not self.dead:
        if (self.grounded):
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
            self.snd_bump.play(0)
            self.ySpeed = 0
    for bri in blockRec:
        if pygame.Rect.colliderect(self.player_hitbox_bot, bri.myHitbox):
            self.grounded = True
        if (self.accel > 0) & pygame.Rect.colliderect(self.player_hitbox_right, bri.myHitbox):
            self.accel = 0
        if (self.accel < 0) & pygame.Rect.colliderect(self.player_hitbox_left, bri.myHitbox):
            self.accel = 0

    self.myY += (self.ySpeed * self.weight)

    if self.myX < 150:
        self.myX += self.accel
    elif (self.screen_scroll <= 0) & (self.accel < 0):
        self.myX += self.accel
        self.screen_scroll = 0
    else:
        self.myX = 150
        self.screen_scroll += self.accel
    
    if self.dead:
        self.deadTimer+=1
        self.accel = 0
        if self.deadTimer < 20:
            self.ySpeed = 0
        elif self.deadTimer < 50:
            self.myY -=1
        else:
            self.myY +=1

def drawHud(mario):
    hud = font.render('MARIO        WORLD    TIME', True, (255,255,255))
    hud2 = font.render(f'{mario.score:06d} ()x{mario.coins:02d}  1-1      {mario.timer:03d}', True, (255,255,255))
    gameDisplay.blit(hud,(24,8))
    gameDisplay.blit(hud2,(24,16))

def setDressing(screen_scroll):
    spr_double_hill = pygame.image.load('spr_double_hill.png')
    spr_hills = pygame.image.load('spr_hills.png')
    spr_cloud = pygame.image.load('spr_cloud.png')
    for Y in range(len(grid)):
        for X in range(len(grid[Y])):
            if grid[Y][X] == 'd':
                gameDisplay.blit(spr_double_hill, ((X * 16)-screen_scroll-3,((Y *16)-17.5))) 
            if grid[Y][X] == 'h':
                gameDisplay.blit(spr_hills, ((X * 16)-screen_scroll,((Y *16)-1.1875))) 
            if grid[Y][X] == 'c':
                gameDisplay.blit(spr_cloud, ((X * 16)-screen_scroll,((Y *16)-12)))        

def levelGrid(screen_scroll):
    spr_brick = pygame.image.load('spr_brick.png')
    spr_pipe_top = pygame.image.load('spr_pipe_top.png')
    spr_pipe_bod = pygame.image.load('spr_pipe_bod.png')
    levelRecs.clear()
    levelRecs.append(Rect(0,0,1,300))
    for Y in range(len(grid)):
        for X in range(len(grid[Y])):
            if grid[Y][X] == 1:
                gameDisplay.blit(spr_brick, ((X * 16)-screen_scroll,((Y *16))))         
                levelRecs.append(Rect((X*16)-screen_scroll, Y*16, 16, 16))
            if grid[Y][X] == 't':
                gameDisplay.blit(spr_pipe_top, ((X * 16)-screen_scroll-16,((Y *16))))         
                levelRecs.append(Rect((X*16)-screen_scroll-16, Y*16, 32, 16))
            if grid[Y][X] == 'p':
                gameDisplay.blit(spr_pipe_bod, ((X * 16)-screen_scroll-16,((Y *16))))         
                levelRecs.append(Rect((X*16)-screen_scroll-16, Y*16, 32, 16))
    #for hb in levelRecs:
        #pygame.draw.rect(gameDisplay,(255,255,255),hb)


def coinGrid(mario):
    snd_coin = pygame.mixer.Sound('snd_coin.mp3')
    spr_coin1 = pygame.image.load('spr_coin1.png')
    spr_coin2 = pygame.image.load('spr_coin2.png')
    spr_coin3 = pygame.image.load('spr_coin3.png')
    spr_coin = [spr_coin1,spr_coin2,spr_coin3]
    if int(mario.ticks/20) <=2:
        sprite = spr_coin[int(mario.ticks/20)]
    else:
       sprite = spr_coin[2] 
    coinRecs.clear()
    for Y in range(len(grid)):
        for X in range(len(grid[Y])):
            if grid[Y][X] == 2:
                if pygame.Rect.colliderect(mario.player_hitbox, Rect((X*16)-mario.screen_scroll, Y*16, 8, 8)):
                    grid[Y][X] = 0
                    snd_coin.stop()
                    snd_coin.play(0)
                    mario.coins +=1
                    mario.score+=100
                gameDisplay.blit(sprite, ((X * 16)-mario.screen_scroll+3,((Y *16)-1)))         
                coinRecs.append(Rect((X*16)-mario.screen_scroll, Y*16, 16, 16))

class koopa:
    def __init__(self,X,Y,mario):
        self.squished = False
        self.snd_squish = pygame.mixer.Sound('smb_stomp.wav')
        self.snd_bump = pygame.mixer.Sound('snd_bump.wav')
        self.snd_kick = pygame.mixer.Sound('snd_kick.wav')
        self.spr_koop = pygame.image.load('spr_koopa1.png')
        self.spr_koop_flipped = pygame.transform.flip(self.spr_koop,True,False)
        self.spr_koop2 = pygame.image.load('spr_koopa2.png')
        self.spr_koop_flipped2 = pygame.transform.flip(self.spr_koop2,True,False)
        self.spr_koop_shell = pygame.image.load('spr_goom_squish.gif')
        self.spr_koop_shell = pygame.image.load('spr_koop_shell.png')
        self.mario = mario
        self.X = X
        self.Y = Y
        self.moveLeft = True
        self.kickSpeed = 0
        self.ticks = 1
        self.sprite = self.spr_koop
        self.squishTimer = 0
        self.kickTimer = 0
        self.moveSpeed = .02
        self.ySpeed = 0
        self.gravity = 1

def updateKoopa(self):
    if self.ticks <= 60:
        self.ticks+=1
    else:
        self.ticks = 1
    #print(self.ticks)

    self.hb_left = Rect((16* self.X)-1-self.mario.screen_scroll, (16* self.Y)+16,1,1)
    self.hb_right = Rect((16*self.X)+17-self.mario.screen_scroll, (16*self.Y)+16, 1,1)
    self.hb_leftside = Rect((16* self.X)-1-self.mario.screen_scroll, (16* self.Y)+8,3,1)
    self.hb_rightside = Rect((16*self.X)+17-self.mario.screen_scroll, (16*self.Y)+8,3,1)

    for loc in levelRecs:
            if ((pygame.Rect.colliderect(self.hb_rightside,loc)) | (pygame.Rect.colliderect(self.hb_leftside,loc))):
                self.moveLeft = not self.moveLeft
                self.kickSpeed = self.kickSpeed * -1
                self.kickTimer = 60
                if self.squished:
                    self.snd_bump.play(0)

    if self.moveLeft:
        canCont = False
        for loc in levelRecs:
            if pygame.Rect.colliderect(self.hb_left,loc):
                canCont = True
        if not canCont:
            self.moveLeft = False

    if not self.moveLeft:
        canCont = False
        for loc in levelRecs:
            if pygame.Rect.colliderect(self.hb_right,loc):
                canCont = True
        if not canCont:
            self.moveLeft = True

    if not self.squished:
        if self.ticks > 29:
            if self.moveLeft:
                self.sprite = self.spr_koop
            else:
                self.sprite = self.spr_koop_flipped    
        else:
            if self.moveLeft:
                self.sprite = self.spr_koop2
            else:
                self.sprite = self.spr_koop_flipped2
    
    self.kickTimer+=2
    if self.kickTimer == 60:
        print("kickTimer Click!")

    if (self.mario.ySpeed > 0) & pygame.Rect.colliderect(self.mario.player_hitbox_bot, Rect((self.X*16)-self.mario.screen_scroll, self.Y*16, 16, 16)):
                        if not self.squished:
                            self.snd_squish.stop()
                            self.snd_squish.play(0)
                            self.mario.score+=300
                            self.squished = True
                            self.mario.grounded = False
                        elif self.kickTimer > 30:
                            self.snd_kick.play(0)
                            self.kickTimer = 0
                            if self.kickSpeed == 0:
                                if self.mario.faceRight:
                                    self.kickSpeed = .15
                                else:
                                    self.kickSpeed = -.15
                            else:
                                self.kickSpeed = 0
                        self.mario.ySpeed = abs(self.mario.ySpeed) * -200
    if (pygame.Rect.colliderect(self.mario.player_hitbox_right, self.hb_leftside)) | (pygame.Rect.colliderect(self.mario.player_hitbox_left,self.hb_rightside)):
                        if (not self.squished):
                            if not self.mario.dead:
                                self.mario.dead = True
                                self.mario.snd_die.play(0)
                        elif ((not self.mario.dead) & (self.kickSpeed == 0)):
                            print("kick!")
                            if self.mario.accel > 0:
                                self.kickSpeed = .15
                            elif self.mario.accel < 0:
                                self.kickSpeed = -.15
                            self.kickTimer = 0
    if self.mario.grounded:
        if ((self.kickSpeed < 0) & (pygame.Rect.colliderect(self.mario.player_hitbox_right, self.hb_leftside))): 
                        if not self.mario.dead:
                            if self.kickTimer > 60:
                                self.mario.dead = True
                                self.mario.snd_die.play(0)
        elif ((self.kickSpeed > 0) & (pygame.Rect.colliderect(self.mario.player_hitbox_left, self.hb_rightside))):   
                        if not self.mario.dead:
                            if self.kickTimer > 60:
                                self.mario.dead = True
                                self.mario.snd_die.play(0)

    if not self.mario.dead:
        self.X += self.kickSpeed
        if not self.squished:
            if self.moveLeft:
                self.X += -.02
            else:
                self.X += .02
        
    if self.squishTimer < 60:
        if self.squished:
            gameDisplay.blit(self.spr_koop_shell, ((self.X * 16)-self.mario.screen_scroll,((self.Y *16)-8))) 
        else:
            gameDisplay.blit(self.sprite, ((self.X * 16)-self.mario.screen_scroll,((self.Y *16)-8)))

class goomba:
    def __init__(self,X,Y,mario):
        self.squished = False
        self.snd_squish = pygame.mixer.Sound('smb_stomp.wav')
        self.spr_goom = pygame.image.load('spr_goom.gif')
        self.spr_goom_squish = pygame.image.load('spr_goom_squish.gif')
        self.mario = mario
        self.X = X
        self.Y = Y
        self.moveLeft = True
        self.ticks = 1
        self.sprite = self.spr_goom
        self.squishTimer = 0
        self.moveSpeed = .02
        self.hb_left = Rect(self.X-1, self.Y+16, 1,0)
        self.hb_right = Rect(self.X+17, self.Y+16, 1,0)


def updateGoomb(self):
    if self.ticks <= 60:
        self.ticks+=1
    else:
        self.ticks = 1
    #print(self.ticks)

    self.hb_left = Rect((16* self.X)-1-self.mario.screen_scroll, (16* self.Y)+16,1,1)
    self.hb_right = Rect((16*self.X)+17-self.mario.screen_scroll, (16*self.Y)+16, 1,1)
    self.hb_leftside = Rect((16* self.X)-1-self.mario.screen_scroll, (16* self.Y)+8,1,1)
    self.hb_rightside = Rect((16*self.X)+17-self.mario.screen_scroll, (16*self.Y)+8, 1,1)
    #pygame.draw.rect(gameDisplay,(255,255,255),self.hb_left)
    #pygame.draw.rect(gameDisplay,(0,255,0),self.hb_right)

    for loc in levelRecs:
            if ((pygame.Rect.colliderect(self.hb_rightside,loc)) | (pygame.Rect.colliderect(self.hb_leftside,loc))):
                self.moveLeft = not self.moveLeft

    if self.moveLeft:
        canCont = False
        for loc in levelRecs:
            if pygame.Rect.colliderect(self.hb_left,loc):
                canCont = True
        if not canCont:
            self.moveLeft = False

    if not self.moveLeft:
        canCont = False
        for loc in levelRecs:
            if pygame.Rect.colliderect(self.hb_right,loc):
                canCont = True
        if not canCont:
            self.moveLeft = True

    if not self.squished:
        if self.ticks % 30 == 0:
            self.sprite = pygame.transform.flip(self.sprite,True,False)

    if (self.mario.ySpeed > 0) & pygame.Rect.colliderect(self.mario.player_hitbox_bot, Rect((self.X*16)-self.mario.screen_scroll, self.Y*16, 16, 16)):
                        if not self.squished:
                            self.snd_squish.stop()
                            self.snd_squish.play(0)
                            self.mario.score+=300
                            self.squished = True
                            self.mario.grounded = False
                            self.mario.ySpeed = abs(self.mario.ySpeed) * -3
    elif (pygame.Rect.colliderect(self.mario.player_hitbox, Rect((self.X*16)-self.mario.screen_scroll, self.Y*16, 14, 16))) | (pygame.Rect.colliderect(self.mario.player_hitbox, Rect((self.X*16)-self.mario.screen_scroll, self.Y*16, 14, 16))):
                        if not self.squished:
                            if not self.mario.dead:
                                self.mario.dead = True
                                self.mario.snd_die.play(0)

    if self.squished:
        if self.squishTimer < 60:
            self.squishTimer+=1

    if not self.squished:
        if self.moveLeft:
            self.X += -.02
        else:
            self.X += .02
    
    if self.squishTimer < 60:
        if self.squished:
            gameDisplay.blit(self.spr_goom_squish, ((self.X * 16)-self.mario.screen_scroll,((self.Y *16)))) 
        else:
            gameDisplay.blit(self.sprite, ((self.X * 16)-self.mario.screen_scroll,((self.Y *16)))) 

def initalizeEnemies(mario):
    eneRecs.clear()
    for Y in range(len(grid)):
        for X in range(len(grid[Y])):
            if grid[Y][X] == 3:        
                eneRecs.append(goomba(X,Y,mario))
            if grid[Y][X] == 5:        
                koopRecs.append(koopa(X,Y,mario))

def initalizeBlocks(mario):
    blockRec.clear()
    for Y in range(len(grid)):
        for X in range(len(grid[Y])):
            if grid[Y][X] == 4:        
                blockRec.append(ItemBlock('coin',5,X*16,Y*16,'brick',mario))

def main():
    tickDown = 0
    quit = False
    sysfont = pygame.font.get_default_font()
    bgm = pygame.mixer.Sound('snd_bgm.mp3')
    bgm.play(-1)
    snd_jump = pygame.mixer.Sound('snd_jump.mp3')
    me = Mario(.2,2.9,2)
    ene = initalizeEnemies(me)
    bri = initalizeBlocks(me)
    while not quit:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit = True
            pygame.event.pump()
        
        pressed = pygame.key.get_pressed()
        if pressed[pygame.K_d]:
            if not me.dead:
                me.accel+=me.speed  
        elif pressed[pygame.K_a]:
            if not me.dead:
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
        if not pressed[pygame.K_SPACE]:
            if me.ySpeed < 0:
                me.ySpeed = 0
        if (me.grounded & pressed[pygame.K_LSHIFT]):
            me.topSpeed = me.runSpeed
        elif me.grounded:
            me.topSpeed = me.walkSpeed
        if me.dead:
            bgm.stop()
        clock.tick(FPS)
        if tickDown < FPS:
            tickDown+=1
        elif not me.dead:
            me.timer-=1
            tickDown = 0
        
        if tickDown % (7-abs(round(me.accel) )) == 0:
            if me.sprite_index < len(me.my_ani)-1:
                me.sprite_index+=1
            else:
                me.sprite_index= 0

        pygame.draw.rect(gameDisplay,(99,134,250),Rect(0,0,300,300))
        setDressing(me.screen_scroll)
        levelGrid(me.screen_scroll)
        coinGrid(me)
        for e in eneRecs:
            updateGoomb(e)
        for k in koopRecs:
            updateKoopa(k)
        for b in blockRec:
            updateBlocks(b)
        updateMario(me)
        drawHud(me)
        pygame.display.update()
main()