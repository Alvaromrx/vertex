
import pygame
import sys
import math
import copy
from random import randint
from pygame.locals import *
from settingsL import *
from math import pi
#from pygame.locals import *

# general constants
SCREEN_WIDTH = 780
SCREEN_HEIGHT = 900
FRAME_RATE = 30
# soy dos gilipollas

WALL_COLOR = {'P':(255, 255, 255), 'p': (90, 221, 228),'Q': (0, 200, 93), 'q': (179, 255, 215), 'D': (200, 0, 200), 'd': (238,206,0), 'G': (255, 255, 255), 'F': (255, 255, 255), 'f': (255, 255, 255), 'Y': (199, 248, 255), 'M': (238, 56, 24), 'm': (20, 20, 228), 'I': (255,255,255), 'i': (255,255,255), '*': (255,255,255)}

PLAYER_LEFT_TOP = pygame.image.load("images/player/playerLT.png")
PLAYER_LEFT_BOT = pygame.image.load("images/player/playerLB.png")
PLAYER_RIGHT_TOP = pygame.image.load("images/player/playerRT.png")
PLAYER_RIGHT_BOT = pygame.image.load("images/player/playerRB.png")
'''PLAYER_INV_LEFT_TOP = pygame.image.load("images/player1_l_inv.png")
PLAYER_INV_LEFT_BOT = pygame.image.load("images/player1B_l_inv.png")
PLAYER_INV_RIGHT_TOP = pygame.image.load("images/player1_r_inv.png")
PLAYER_INV_RIGHT_BOT = pygame.image.load("images/player1B_r_inv.png")'''
PLAYER_POSITION_Y = 500
PLAYER_JUMP = 20
DL = 0
DR = 1

PLATFORM_SIZE = 20
TIME_FIRE_CANNON = 12

# general variables
MAP = []
lvl = 3
platform = []
ghPlatform = []
enemies = []
spikes = []
cannons = []
blackholes = []
coins = []
arrows = []
spheres = []
lasers = []
switches = []
markers = []
trampolines = []
trapSpike = []
portal = None
checkpoint = None
total = 0
elements = [platform, ghPlatform, enemies, spikes, cannons, blackholes, coins, arrows, spheres, lasers, switches, markers, trampolines, trapSpike]
listUpdates = [platform, cannons, enemies, spikes, lasers, markers, trapSpike]

# keyboard
# use the arrow keys by default
LEFT_KEY = pygame.K_a
RIGHT_KEY = pygame.K_d
UP_KEY = pygame.K_w
DOWN_KEY = pygame.K_s

# but you can use another configuration, for example WASD:
#LEFT_KEY = pygame.K_a
#RIGHT_KEY = pygame.K_d
#UP_KEY = pygame.K_w
#DOWN_KEY = pygame.K_s

# game constants
HORIZONTAL_LEFT, HORIZONTAL_NOT, HORIZONTAL_RIGHT = ( -1, 0, 1 )
VERTICAL_UP, VERTICAL_NOT, VERTICAL_DOWN = ( -1, 0, 1 )


class Game():
    def __init__(self):
        pass

    def loop(self, screen, player):
        global portal, lvl, total, checkpoint
        # main loop variables
        clock = pygame.time.Clock()
        stopCamera = False
        ORIENTATION = player.orientation
        ORIENTATION = 0
        # initialize font; must be called after 'pygame.init()' to avoid 'Font not Initialized' error
        clipMask(player)
        myfont = pygame.font.SysFont("monospace", 15)
        font = pygame.font.SysFont("monospace", 70)
        # render text
        labelCoin = myfont.render("Blue: 0/3 - Red: 0/3 - Gold: 0/3", 1, (255,255,0))
        labelGameover = font.render("GAME OVER", 5, (255,255,255))
        labelNextlevel = font.render("NEXT LEVEL", 5, (255,255,255))
        timeGameOver = 100
        heart = pygame.image.load("images/heart.png")
        #fog = pygame.image.load("images/fog.png")
        #playerS = copy.copy(player)
        #playerS.alive = False
        cFireCannon = 0
        changeDim = False

        left_key_pressed = right_key_pressed = up_key_pressed = down_key_pressed = False
        horizontal_dir = HORIZONTAL_NOT
        vertical_dir = VERTICAL_NOT
        space_key_pressed = False
 
        while True:
            delta_t = clock.tick( FRAME_RATE )
            #
            #   I N P U T
            # --------------------------------------------------------------
          
            for event in pygame.event.get(): # event handling loop
    
                # handle quitting from the program
                if event.type == pygame.QUIT:
                    return # closing the window, end of the game loop
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    return # closing the window, end of the game loop

                # movement keys
                elif event.type == pygame.KEYDOWN:
                    if event.key == UP_KEY:
                        up_key_pressed = True
                        vertical_dir = VERTICAL_UP
                    elif event.key == DOWN_KEY:
                        down_key_pressed = True
                        vertical_dir = VERTICAL_DOWN
                    elif event.key == LEFT_KEY:
                        left_key_pressed = True
                        horizontal_dir = HORIZONTAL_LEFT
                    elif event.key == RIGHT_KEY:
                        right_key_pressed = True
                        horizontal_dir = HORIZONTAL_RIGHT

                    if event.key == K_SPACE:
                        space_key_pressed = True
                        for c in cannons:
                            if c == player.idCannon and not c.disable:
                                cFireCannon = 0
                                player.cannon = True
                                player.spriteSheet = 'djump'
                                player.cImage = 0
                                player.idCannon = 0
                                if c.property['dir'] == 'top':
                                    changeDimension(player, False, True, 0)
                                    player.rect.center = c.rect.center
                                    player.rect.top -= 40
                                    ORIENTATION = 0
                                    if c.property['disable']:
                                        c.image = pygame.image.load("images/cannonTD.png")
                                        c.disable = True
                                elif c.property['dir'] == 'bot':
                                    changeDimension(player, False, True, 1)
                                    player.rect.center = c.rect.center
                                    player.rect.top += 40
                                    ORIENTATION = 1
                                    if c.property['disable']:
                                        c.image = pygame.image.load("images/cannonBD.png")
                                        c.disable = True

                        if not player.impactAss:    
                            if player.jump:
                                player.cImage = 0
                                player.spriteSheet = 'djump'
                                player.djump = True
                                player.jump = False
                                player.aniJump = True
                                player.cJump = player.distJump
                                player.maxJ = False

                            else:
                                if not player.dimension:
                                    player.aniJump = True
                                    player.jump = True                           

                elif event.type == pygame.KEYUP:
                    if event.key == UP_KEY:
                        up_key_pressed = False
                        player.mov = False
                        if down_key_pressed:
                            vertical_dir = VERTICAL_DOWN
                        else:
                            vertical_dir = VERTICAL_NOT
                    elif event.key == DOWN_KEY:
                        down_key_pressed = False
                        player.mov = False
                        if up_key_pressed:
                            vertical_dir = VERTICAL_UP
                        else:
                            vertical_dir = VERTICAL_NOT
                    elif event.key == LEFT_KEY:
                        left_key_pressed = False
                        if right_key_pressed:
                            horizontal_dir = HORIZONTAL_RIGHT
                        else:
                            horizontal_dir = HORIZONTAL_NOT
                    elif event.key == RIGHT_KEY:
                        right_key_pressed = False
                        if left_key_pressed:
                            horizontal_dir = HORIZONTAL_LEFT
                        else:
                            horizontal_dir = HORIZONTAL_NOT
                    elif event.key == K_SPACE:
                        space_key_pressed = False

            #
            #   U P D A T E
            # --------------------------------------------------------------
            if player.idCannon == 0 and not player.cannon and player.alive and not player.impactAss and not player.ass:
                if not player.djump:
                    player.spriteSheet = 'walk'
                if vertical_dir == VERTICAL_UP:
                    player.mov = True            
                    if player.rect.top > 0:
                        player.change_speed(0, -4)
                    changeDimension(player, False, True, 0)
                                #changeDimension(player, False, True, 0)
                elif vertical_dir == VERTICAL_DOWN:
                    player.mov = True
                    if player.rect.top + player.rect.height < SCREEN_HEIGHT:
                        player.change_speed(0, 4)
                    changeDimension(player, False, True, 1)
                            #changeDimension(player, False, True, 1)

            # change if for elif for 4-coordinates only movement                           
            if horizontal_dir == HORIZONTAL_LEFT:       
                if (not player.jump and not player.djump and player.floor and not player.deadTime and not player.impactAss and not player.ass) or player.idCannon != 0: 
                    if player.idCannon != 0:
                        player.idCannon.change_speed(-8, 0)
                        #player.idCannon.rect.left -= 10
                    elif player.enemy != None:
                        if player.enemy.property['group'] == 'enemy02':
                            player.rect.left -= 10
                            player.enemy.rect.left -= 10
                    else: 
                        p = 0
                        if player.platform != 0:
                            p = player.platform.type
                        if p == 'D':
                            changeDimension(player, True, False)
                            changeDim = True
                            player.rect.right = player.platform.rect.left
                            left_key_pressed = False
                            horizontal_dir = HORIZONTAL_NOT
                        elif p in ('M', 'm'):
                            pass
                        elif player.dir == DR:                           
                            changeDimension(player, True, False)
                            changeDim = True

                elif (player.jump or player.djump) and not player.floor and not player.deadTime:
                    if player.dir == DL:
                        player.ass = True
                        player.jump = False
                        player.djump = False

            elif horizontal_dir == HORIZONTAL_RIGHT:   
                if (not player.jump and not player.djump and player.floor and not player.deadTime and not player.impactAss and not player.ass) or player.idCannon != 0: 
                    if player.idCannon != 0:
                        #player.idCannon.rect.left += 10
                        player.idCannon.change_speed(8, 0)
                    elif player.enemy != None:
                        if player.enemy.property['group'] == 'enemy02':
                            player.rect.left += 10
                            player.enemy.rect.left += 10
                    else:
                        p = 0
                        if player.platform != 0:
                            p = player.platform.type
                        if p == 'D':
                            changeDimension(player, True, False)
                            changeDim = True
                            player.rect.left = player.platform.rect.right
                            right_key_pressed = False
                            horizontal_dir = HORIZONTAL_NOT
                        elif p in ('M', 'm'):
                            pass
                        elif player.dir == DL: 
                            changeDimension(player, True, False)
                            changeDim = True

                elif (player.jump or player.djump) and not player.floor and not player.deadTime:
                    if player.dir == DR:
                        player.ass = True
                        player.jump = False
                        player.djump = False

            self.animationSprite(player, space_key_pressed)
            
            if player.alive:              

                # MOVEMENT PLAYER
                if not stopCamera:
                    if ORIENTATION == 0:
                        player.rect.top += player.vel
                        #player.change_speed(0, player.vel)
                    elif ORIENTATION == 1:
                        player.rect.top -= player.vel
                        #player.change_speed(0, -player.vel)

                '''if player.cannon:
                    player.rect.top += player.vel*4
                else:
                    player.rect.top += player.vel

                if player.cannon:
                    player.rect.top -= player.vel*4
                else:
                    player.rect.top -= player.vel'''

                # Check if the Player is jumping and call the function jumping()
                if player.idCannon == 0:
                    if player.aniJump:
                        player.jumping()
                    else:
                        if not player.cannon and not player.ass:          
                        # Gravity
                            if not player.trampolin:
                                if player.dir == DL:
                                    player.change_speed(-player.velGravity, 0)
                                elif player.dir == DR:
                                    player.change_speed(player.velGravity, 0)
                            
                 # Check eje X of the Player for change side
                if player.canSide:
                    limitScreen = True
                    if player.rect.left <= -(player.rect.width/2):
                        player.rect.left = SCREEN_WIDTH - (player.rect.width/2)
                    elif player.rect.left + (player.rect.width)/2 >= SCREEN_WIDTH:
                        player.rect.left = -(player.rect.width/2)
                else:
                    if (player.rect.left + player.rect.width) <= 0 or player.rect.left > SCREEN_WIDTH:
                        player.alive = False

                # Check eje Y of the Player for gameover
                if (player.rect.top + player.rect.height >= SCREEN_HEIGHT and ORIENTATION==0):
                    player.change_speed(0, -player.vel)
                    
                elif (player.rect.top <= 0 and ORIENTATION==1):
                    player.change_speed(0, player.vel)

                collisionY = False
                collisionX = False
                tempRectY = 0
                tempRectX = 0
                color = 0
                limitScreen = False
                stopCamera = False

                # Check collision between Player and another element (platform, enemies, etc)
                stopCamera = player.update([platform, ghPlatform, enemies, lasers, trampolines, trapSpike], space_key_pressed, stopCamera)

                # Player - Make the movement and check the collision with the group passed by parameter
                for i in listUpdates:
                    for u in i:
                        u.update(player)
                             
                #if not changeDim or player.cannon:
                if not stopCamera:
                    for i in elements:
                        for e in i:
                            velocity = 0.0
                            fy = e.rect.top
                            velocity = player.vel                  
                            
                            if ORIENTATION == 0:
                                fy += velocity
                            
                            elif ORIENTATION == 1:
                                fy -= velocity             

                            e.rect.top = fy
                                   
                    #Movement Portal and CheckPoint        
                    if ORIENTATION == 0:
                        portal.rect.top += player.vel 
                        checkpoint.rect.top += player.vel 
                    elif ORIENTATION == 1:
                        portal.rect.top -= player.vel
                        checkpoint.rect.top -= player.vel
                 
                # Check Collision between 1 Sprite and 1 Group Sprites (player, spikes)
                if not player.hit:
                    blocks_hit_list = pygame.sprite.spritecollide(player, spikes, False, pygame.sprite.collide_mask)
                    for block in blocks_hit_list:
                        player.dimension = False
                        if not block.hit:
                            if block.type == '<':
                                block.image = pygame.image.load("images/spikes/spikeRH.png")
                            elif block.type == '>':
                                block.image = pygame.image.load("images/spikes/spikeLH.png")
                            elif block.type == '^':
                                block.image = pygame.image.load("images/spikes/spikeTH.png")
                            elif block.type == 'v':
                                block.image = pygame.image.load("images/spikes/spikeBH.png")

                            block.hit = True                        
                        if not player.invincible:
                            player.deadTime = True
                            player.alive = False
                            player.spriteSheet = 'dead'
                            player.cImage = 0
                            #player.hit = True
                            #player.lives -= 1
                        break
                
                for a in arrows:
                    a.cImage = 0
                    a.hit = False

                blocks_hit_list = pygame.sprite.spritecollide(player, arrows, False, pygame.sprite.collide_mask)
                for block in blocks_hit_list:
                    if player.dir == DL:
                        block.cImage = 2
                    elif player.dir == DR:
                        block.cImage = 1
                            
                    if block.type == 'A':
                        ORIENTATION = 0
                    elif block.type == 'a':
                        ORIENTATION = 1

                blocks_hit_list = pygame.sprite.spritecollide(player, blackholes, False, pygame.sprite.collide_mask)
                for b in blocks_hit_list:
                    if not player.invincible and player.idCannon == 0:
                        player.alive = False
                        player.blackhole = True
                        player.cImage = 0
                        player.spriteSheet = 'blackhole'
                        if player.dir == DL:
                            player.image = pygame.image.load("images/player/playerL_blackhole.png")
                        elif player.dir == DR:
                            player.image = pygame.image.load("images/player/playerR_blackhole.png")
                        player.rect = player.image.get_rect()
                        player.rect.left = b.rect.left
                        player.rect.top = b.rect.top
                        player.rect.width = 40
                        player.rect.height = 40    

                for c in cannons:
                    if(pygame.sprite.collide_rect(player, c)):
                        if (player.dir == DR and c.property['color'] == 'red' or player.dir == DL and c.property['color'] == 'blue'):
                            if not player.cannon: 
                                player.idCannon = c
                                cFireCannon = 0
                                
                                #player.rect.center = c.rect.center  
                                
                if player.cannon:
                    if cFireCannon < TIME_FIRE_CANNON:
                        cFireCannon += 1
                    else:
                        player.cannon = False
                        cFireCannon = 0

                for c in coins:
                    if(pygame.sprite.collide_rect(player, c)):
                        getCoin = False
                        if c.type == 'o' and player.dir == DL:
                            player.coins['blue'] += 1
                            getCoin = True
                        elif c.type == 'O' and player.dir == DR:
                            player.coins['red'] += 1
                            getCoin = True
                        elif c.type == '0':
                            player.coins['gold'] += 1
                            getCoin = True

                        if getCoin:
                            labelCoin = myfont.render("Blue: "+str(player.coins['blue'])+"/3 - Red: "+str(player.coins['red'])+"/3 - Gold: "+str(player.coins['gold'])+"/3" , 1, (255,255,0))
                            coins.remove(c)
                        '''if c.type == 'O':     
                            e = elements[0][0]
                            diff = e.y - e.rect.top
                            if player.dir == DR:                    
                                if player.orientation == 0:
                                    changeDimension(player, 0, PLAYER_LEFT_TOP)
                                else:
                                    changeDimension(player, 0, PLAYER_LEFT_BOT)
                            if player.dir == DL:
                                if player.orientation == 0:
                                    changeDimension(player, 1, PLAYER_RIGHT_TOP)
                                else:
                                    changeDimension(player, 1, PLAYER_RIGHT_BOT)
                            reset(player)
                            MAP = loadLevel(lvl)                           
                            fillMap(MAP, True, diff)
                        else:'''                       

                for e in spheres:
                    if(pygame.sprite.collide_rect(player, e)):
                        player.invincible = True   
                        player.vel = 3
                        changeDimension(player, False, False)
                        spheres.remove(e)

                if pygame.sprite.collide_rect(player, portal):
                    if not portal.hit:
                        portal.hit = True
                        player.alive = False

                if pygame.sprite.collide_rect(player, checkpoint):
                    if not checkpoint.hit:
                        checkpoint.hit = True
                        player.checkpoint = checkpoint

                '''blocks_hit_list = pygame.sprite.spritecollide(player, lasers, False, pygame.sprite.collide_mask)
                for b in blocks_hit_list:
                    if not player.invincible and b.active:
                        #player.alive = False   
                        player.deadTime = True'''

                for b in switches:
                    if pygame.sprite.collide_rect(player, b) and (player.ass or player.impactAss):
                        b.active = True
                        for l in lasers:
                            for x in range(b.idLaser[0], b.idLaser[1]):
                                if l.id == x:
                                    l.active = False

            #
            #   R E N D E R
            # --------------------------------------------------------------
    
            # render game screen
            screen.fill( (0, 0, 0) ) # black background

            # game over
            if not player.alive and not player.blackhole and not player.deadTime:
                if portal.hit:
                    gameover(screen, labelNextlevel)
                else:
                    gameover(screen, labelGameover)

                if timeGameOver <= 0:
                    timeGameOver = 100
                    if portal.hit:
                        lvl += 1
                        checkpoint = None
                    portal.hit = False
                    checkpoint.hit = False
                    labelCoin = myfont.render("Blue: 0/3 - Red: 0/3 - Gold: 0/3", 1, (255,255,0))
                    #newGame(player, lvl)
                    player = reset(player)
                    clipMask(player)
                    ORIENTATION = 0
                    map = loadLevel(lvl)                           
                    fillMap(map, player, False, 0)                                       
                else:
                    timeGameOver -= 1

            # blit the graphic elements to the screen surface
            if player.alive or player.blackhole or player.deadTime: 
                portal.draw(screen)
                checkpoint.draw(screen)

                for p in ghPlatform:
                    if p.type in ('F'):
                        p.updateAlpha()        

                for i in elements:
                    for e in i:
                        e.draw(screen)

                player.draw(screen)
                
                #screen.blit(fog, (0, 0))

                '''for i in range(player.lives):
                    screen.blit(heart, ((i+1)*33, 20))'''
               
                screen.blit(labelCoin, (SCREEN_WIDTH/2+100, 10))
            
            click1, click2, click3 = pygame.mouse.get_pressed()      
        
            if click2 > 0:
                posX, posY = pygame.mouse.get_pos()
                for i in platform:                  
                    if((posX >= i.rect.left and posX <= i.rect.left+i.rect.width)
                        and (posY >= i.rect.top and posY <= i.rect.top+i.rect.height)):
                            #print "COLUMNA PLAT:" + str(i.rect.left/PLATFORM_SIZE)
                            print "ID :" + str(i.id)
                            
                if((posX >= player.rect.left and posX <= player.rect.left+player.rect.width)
                    and (posY >= player.rect.top and posY <= player.rect.top+player.rect.height)):
                        print "COLUMNA PLAYER:" + str(math.ceil((player.rect.left+player.rect.width)/PLATFORM_SIZE))

                #print pygame.mouse.get_pos()

            # update display
            pygame.display.update()

    def animationSprite(self, player, space_key):
         # SpriteSheet Animation Player
        if (player.cImage >= player.listSP[player.spriteSheet]-1):
            player.cImage = 0
            #player.spriteSheet = 'idle'
            player.blackhole = False
            player.deadTime = False
            player.impactAss = False
        else:
            if player.spriteSheet == 'walk':
                player.cImage += 1
            elif player.spriteSheet in ('blackhole', 'dead') :
                player.cImage += 0.5
            elif player.spriteSheet == 'djump':
                player.cImage += 0.6
            elif player.spriteSheet == 'ass':
                player.cImage += 0.5


        # SpriteSheet Animation BlackHole
        for b in blackholes:
            if (b.cImage >= b.numImages-1):
                b.cImage = 0
                if b.rowImage >= b.numImages-1:
                    b.rowImage = 0
                else:
                    b.rowImage += 1
            else:
                b.cImage += 0.1

        # SpriteSheet Animation Coin
        for c in coins:
            if (c.cImage >= c.numImages-1):
                c.cImage = 0
            else:
                c.cImage += 0.5

        # SpriteSheet Animation Portal       
        if (portal.cImage >= portal.numImages):
            portal.cImage = 0
        else:
            portal.cImage += 1

        # SpriteSheet Animation Enemies   
        for e in enemies:
            if e.cImage > e.frames[e.frame][1]:
                e.cImage = e.frames[e.frame][0]
            else:
                e.cImage += 0.25
      
        for t in trampolines:
            if t.active:
                if (t.cImage >= t.numImages-1):
                    t.cImage = 0
                    t.active = False
                    player.aniJump = True
                    if space_key:
                        player.distJump = 24.0
                    else:
                        player.distJump = 16.0
                    player.cJump = player.distJump
                    player.maxJ = False
                    player.trampolin = False
                else:
                    t.cImage += 1       
                    if t.type == 'T':
                        player.rect.left -= 1
                    elif t.type == 't':
                        player.rect.left += 1

        if checkpoint.hit:
            if (checkpoint.cImage >= checkpoint.numImages-1):
                checkpoint.cImage = checkpoint.numImages-1
            else:
                checkpoint.cImage += 0.5

    def quit(self):
        pass

class createPlayer(pygame.sprite.Sprite):
    def __init__(self, id, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.id = id
        self.x = x
        self.y = y     
        self.image = pygame.image.load("images/player/playerLT.png")
        self.spriteSheet = 'idle'
        self.listSP = {'idle': 0, 'walk': 16, 'blackhole': 13, 'dead': 25, 'djump': 5, 'ass': 9}
        self.rect = self.image.get_rect()
        self.rect.left = x
        self.rect.top = y
        self.rect.width = 52
        self.rect.height = 33
        self.type = None
        self.screenAlpha = pygame.Surface((52,33))  # the size of your rect    
        self.alive = True
        self.invincible = False
        self.platform = 0
        self.lives = 1
        self.mov = False
        self.hit = False
        self.changeAlpha = True
        self.timeAlpha = 5
        self.coins = {'red': 0, 'blue': 0, 'gold': 0}
        self.checkpoint = 0
        self.blackhole = False
        self.deadTime = False
        self.cImage = 0
        self.currentVel = 16
        self.vel = 2
        self.velGravity = 20
        self.dir = 0 # 0: left / 1: right
        self.orientation = 0
        self.dimension = True
        self.activateDim = False
        #self.maxJump = 6
        self.distJump = 8.0
        self.cJump = self.distJump   
        self.aniJump = False
        self.jump = False
        self.djump = False
        self.maxJ = False
        self.ass = False
        self.impactAss = False
        self.floor = False
        self.wall = False
        self.cannon = False
        self.idCannon = 0
        self.canSide = False
        self.glued = False
        self.enemy = None
        self.trampolin = False
        #self.color = (255, 255, 255)

        self.hspeed = 0
        self.vspeed = 0

    def jumping(self):

        if self.dir == 0:
            if self.maxJ:
                self.change_speed(-self.cJump, 0)
            else:
                self.change_speed(self.cJump, 0)
        elif self.dir == 1:
            if self.maxJ:
                self.change_speed(self.cJump, 0)
            else:
                self.change_speed(-self.cJump, 0)

        if self.cJump <= 0:
            self.maxJ = True
        elif self.cJump >= self.distJump:
            if self.maxJ:
                #self.jump = False
                #self.djump = False
                self.aniJump = False
            self.maxJ = False
            self.distJump = 8.0

        if self.maxJ:
            self.cJump += 1
        else:
            self.cJump -= 1
    
    def change_speed(self, hspeed, vspeed):
        self.hspeed += hspeed
        self.vspeed += vspeed

    def resetV(self):
        self.enemy = None
        self.dimension = True
        self.canSide = False
        self.platform = 0
        self.floor = False
        self.glued = False
        self.wall = False

    def update(self, collidable, space_key, stopCamera):
        self.resetV()

        if self.ass:
            if self.dir == DL:
                self.change_speed(-12, 0)
            elif self.dir == DR:
                self.change_speed(12, 0)
        # Check collision between Player and Marks list
        '''
        self.row = round(self.rect.top/PLATFORM_SIZE)
        for m in markers:
            rowPt = round(m.rect.top/PLATFORM_SIZE)
            if self.row == rowPt:
                self.vel = m.property['speed']
                break'''
        
        self.rect.x += self.hspeed    

        for c in collidable:

            if c in (enemies):          
                collision_list = pygame.sprite.spritecollide( self, c, False, pygame.sprite.collide_mask )
            else:
                collision_list = pygame.sprite.spritecollide( self, c, False )

            for co in collision_list:

                if co.type == 'E':
                    self.enemy = co
                    if co.property['lives'] <= 0:                       
                        co.frame = 'deadTimeframes'
                        co.cImage = co.frames[co.frame][0]

                    elif co.property['canDie'] and not self.hit and not co.hit:     
                        if self.jump and co.property['group'] in ('enemy01'): 
                            co.hit = True
                            self.aniJump = True
                            if space_key:
                                self.distJump = 8.0
                            self.cJump = self.distJump
                            self.maxJ = False
                            co.property['lives'] -= 1
                        elif self.djump and co.property['group'] in ('enemy01'):
                            co.hit = True
                            self.aniJump = True
                            if space_key:
                                self.distJump = 13.0
                            self.cJump = self.distJump
                            self.maxJ = False
                            co.property['lives'] -= 1
                        elif self.ass and co.property['group'] in ('enemy01', 'enemy03'):
                            co.hit = True
                            co.property['lives'] -= 1

                    elif not co.property['canDie']:
                        if co.property['group'] == 'enemy02' and not co.endPath:
                            co.property['stopped'] = False

                        if co.property['damage']:
                            if co.frame != 'hitframes':
                                co.frame = 'hitframes'
                                co.cImage = co.frames[co.frame][0]
                        else:
                            dif = math.fabs(co.rect.centerx - self.rect.centerx)
                            max = (co.rect.width+self.rect.width)/2
                            if dif > (max - 35):
                                self.floor = True    
                                self.dimension = False
                                if self.ass:
                                    self.ass = False
                                    self.impactAss = True
                                    self.spriteSheet = 'ass'
                                    self.cImage = 0

                                elif (self.jump or self.djump) and not self.impactAss: 
                                    self.cImage = 0
                                    self.spriteSheet = 'idle'
                                    self.aniJump = False
                                    self.djump = False
                                    self.jump = False
                                    self.maxJ = False
                                    self.cJump = self.distJump 

                                if ( self.hspeed > 0 ):
                                    # RIGHT DIRECTION
                                    if co.property['dir'] == 'right':
                                        self.rect.right = co.rect.left                          
                                        '''if self.dir == 1:
                                            roof = True'''

                                elif ( self.hspeed < 0 ):
                                    # LEFT DIRECTION
                                    if co.property['dir'] == 'left':
                                        self.rect.left = co.rect.right
                                        '''if self.dir == 0:
                                            roof = True'''                                                                                                        

                    else:
                        if not self.invincible and not self.hit and co.property['damage'] and not co.hit:
                            self.alive = False
                            self.deadTime = True 
                            self.spriteSheet = 'dead'
                            self.cImage = 0

                elif co.type == '#':
                    if co.cImage >= 1:
                        self.alive = False
                        self.deadTime = True 
                        self.spriteSheet = 'dead'
                        self.cImage = 0

                elif co.type == '|':
                    if not self.invincible and co.active:
                        #player.alive = False 
                        dif = math.fabs(round(co.rect.centerx - self.rect.centerx))  
                        if dif < 24: 
                            self.alive = False
                            self.deadTime = True
                            self.spriteSheet = 'dead'
                            self.cImage = 0

                elif co.type in ('T', 't'):
                    co.hit = True
                    if self.hspeed > 0:     
                        if co.type == 'T' :
                            co.active = True
                            self.trampolin = True
                            #self.rect.right = co.rect.left

                    elif self.hspeed < 0:                   
                        if co.type == 't' :                              
                            co.active = True
                            self.trampolin = True
                            #self.rect.left = co.rect.right

                # CHECK COLLISION PLATFORMS
                else:
                    if co.type in ('D', 'd', 'M', 'm'):
                        self.platform = co
                    if co.type in ('P', 'p', 'Q', 'q', 'D', 'F', 'i', 'd'):
                        if co.alpha > 70 or (co.type == 'F' and co.alpha < 200):
                            roof = False            
                            dif = math.fabs(co.rect.centery - self.rect.centery)
                            dist = (co.rect.height+self.rect.height)/2

                            if ( self.hspeed > 0 ):
                                # RIGHT DIRECTION
                                if dif <= dist:
                                    #if self.rect.right <= co.rect.left + self.velGravity:
                                    self.rect.right = co.rect.left
                                if self.dir == 0:
                                    roof = True

                            elif ( self.hspeed < 0 ):
                                # LEFT DIRECTION
                                if dif <= dist:
                                    #if self.rect.left >= co.rect.right - self.velGravity:
                                    self.rect.left = co.rect.right
                                if self.dir == 1:
                                    roof = True

                            if hasattr(co, 'glued'):
                                if co.glued:
                                    self.glued = True

                            if co.type == 'p':
                                if self.ass:
                                    id = co.property['id']
                                    for i in platform:
                                        if i.type == 'p' and i.property['id'] == id:
                                            i.beat = self.dir
                        
                            if not roof:                           
                                self.floor = True    
                                self.dimension = False
                                
                                if self.ass:
                                    self.ass = False
                                    self.impactAss = True
                                    self.spriteSheet = 'ass'
                                    self.cImage = 0
 
                                elif (self.jump or self.djump) and not self.impactAss:  
                                    self.cImage = 0
                                    self.spriteSheet = 'idle'
                                    self.aniJump = False
                                    self.djump = False
                                    self.jump = False
                                    self.maxJ = False
                                    self.cJump = self.distJump 

                            if co.type == 'Q':
                                self.floor = False
                                break
                            elif co.type == 'q':
                                self.dimension = True
                                break
                            elif co.type == 'd':
                                if dif < dist-7:
                                    stopCamera = True
                                    break

                    if co.type == 'I':
                        self.canSide = True

        if self.cannon:
            if self.orientation == 0:
                self.change_speed(0, -12)
                            
            elif self.orientation == 1:
                self.change_speed(0, 12)           

        self.rect.y += self.vspeed

        for c in collidable:

            if c == enemies:
                collision_list = pygame.sprite.spritecollide( self, c, False, pygame.sprite.collide_mask )
            else:
                collision_list = pygame.sprite.spritecollide( self, c, False )

            for co in collision_list:

                if co.type == 'E':   
                    self.enemy = co
                    if co.property['lives'] <= 0:
                        co.frame = 'deadTimeframes'
                        co.cImage = co.frames[co.frame][0] 

                    elif not self.invincible and not self.hit and co.property['damage'] and not co.hit:
                        self.alive = False
                        self.deadTime = True
                        self.spriteSheet = 'dead'
                        self.cImage = 0

                    elif not co.property['damage']:
                        if ( self.vspeed > 0 ):
                            # DOWN DIRECTION
                            self.rect.bottom = co.rect.top

                        elif ( self.vspeed < 0 ):
                            # UP DIRECTION
                            self.rect.top = co.rect.bottom

                elif co.type == '#':
                    if co.cImage >= 1:
                        self.alive = False
                        self.deadTime = True 
                        self.spriteSheet = 'dead'
                        self.cImage = 0

                elif co.type == '-':
                    if not self.invincible and co.active:
                        #player.alive = False
                        dif = math.fabs(round(co.rect.centery - self.rect.centery))  
                        if dif < 14:
                            self.alive = False
                            self.deadTime = True
                            self.spriteSheet = 'dead'
                            self.cImage = 0

                elif co.type in ('T', 't') and not self.trampolin:
                    if self.vspeed > 0:
                        self.rect.bottom = co.rect.top

                    elif self.vspeed < 0:
                        self.rect.top = co.rect.bottom

                # CHECK COLLISION PLATFORMS
                else:
                    self.wall = True
                    if co.type in ('D', 'M', 'm'):
                        self.platform = co
                    if co.type in ('P', 'i') or (co.type == 'M' and self.dir == 0) or (co.type == 'm' and self.dir == 1):
                        if co.alpha > 70 or (co.type == 'F' and co.alpha < 200):
                            if self.cannon:
                                if self.orientation == 0:
                                    self.rect.top = co.rect.bottom
                                elif self.orientation == 1:
                                    self.rect.bottom = co.rect.top

                            if ( self.vspeed > 0 ):
                                # DOWN DIRECTION
                                self.rect.bottom = co.rect.top
                                if self.rect.top < 0:
                                    self.alive = False
                                    self.deadTime = True
                                    self.spriteSheet = 'dead'
                                    self.cImage = 0

                            elif ( self.vspeed < 0 ):
                                # UP DIRECTION
                                self.rect.top = co.rect.bottom
                                if self.rect.top + self.rect.height > SCREEN_HEIGHT:
                                    self.alive = False
                                    self.deadTime = True
                                    self.spriteSheet = 'dead'
                                    self.cImage = 0

                    if co.type == 'I':
                        self.canSide = True

        self.hspeed = 0
        self.vspeed = 0

        return stopCamera

    def draw(self, surface):
        if self.idCannon == 0:
            if self.blackhole:
                surface.blit(self.image, self.rect, (math.floor(self.cImage)*self.rect.width, 0, self.rect.width, self.rect.height))    
            elif self.deadTime:
                surface.blit(self.image, self.rect, (self.rect.width*3, math.floor(self.cImage)*self.rect.height, self.rect.width, self.rect.height))
            elif self.impactAss:
                surface.blit(self.image, self.rect, (self.rect.width*4, math.floor(self.cImage)*self.rect.height, self.rect.width, self.rect.height))
            elif self.ass:
                surface.blit(self.image, self.rect, (self.rect.width, 66, self.rect.width, self.rect.height))
            elif self.jump:
                surface.blit(self.image, self.rect, (self.rect.width, self.rect.height, self.rect.width, self.rect.height))
            elif self.djump or self.cannon:
                surface.blit(self.image, self.rect, (self.rect.width*2, math.floor(self.cImage)*self.rect.height, self.rect.width, self.rect.height))
            elif self.dimension and not self.floor:
                surface.blit(self.image, self.rect, (0, 8*self.rect.height, self.rect.width, self.rect.height))
            elif not self.mov:
                surface.blit(self.image, self.rect, (self.rect.width, 0, self.rect.width, self.rect.height))       
            else:
                surface.blit(self.image, self.rect, (0, self.cImage*self.rect.height, self.rect.width, self.rect.height))

        if self.hit:
            self.updateAlpha()
            surface.blit(self.screenAlpha, self.rect)

    def updateAlpha(self):
        if self.timeAlpha > 0:
            if self.changeAlpha:
                self.alpha -= 50
            else:
                self.alpha += 50

            if self.alpha >= 255:
                self.alpha = 255
                self.changeAlpha = True
                self.timeAlpha -= 1
            elif self.alpha <= 0:
                self.alpha = 0
                self.changeAlpha = False
        else:
            self.hit = False
            self.timeAlpha = 5
            
        self.setAlpha()
        
    def setAlpha(self):
        self.screenAlpha.set_alpha(self.alpha)

class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, type):
        pygame.sprite.Sprite.__init__(self)
        self.id = id
        self.x = x
        self.y = y
        self.image = pygame.Surface( (PLATFORM_SIZE, PLATFORM_SIZE) )             
        self.image.fill (WALL_COLOR[type])       
        self.rect = self.image.get_rect()
        self.rect.left = x
        self.rect.top = y
        self.mask = pygame.mask.from_surface(self.image)
        self.type = type
        self.type2 = ''
        self.indexCoord = 0
        self.alpha = 255
        self.property = None
        self.beat = -1
        self.cBeat = 0

    def draw(self, surface):
        surface.blit(self.image, self.rect)
        #surface.blit(self.screenAlpha, self.rect)

    def getImage(self):
        if self.type in ('P', 'D', 'Q') or self.type2 in ('P', 'D', 'Q'):
            self.image = pygame.image.load("images/platform_"+self.type+".png")
        elif self.type in ('d', 'q', 'p') or self.type2 in ('d', 'q', 'p'):
            self.image = pygame.image.load("images/platform_"+self.type+self.type+".png")

    def update(self, player):          
        if self.type2 == 'G':
            #self.rect.top -= self.property['speedY']
            
            if self.coord <= 0:
                if self.indexCoord == 3:
                    self.indexCoord = 0
                else:
                    self.indexCoord += 1
                self.coord = self.property['coord'][self.indexCoord]

            elif self.indexCoord == 0:
                self.rect.top -= self.property['speedY']
                self.coord -= math.fabs(self.property['speedY'])
                if player.glued:
                    player.rect.top -= self.property['speedY']/2
                    
            elif self.indexCoord == 1:
                self.rect.left += self.property['speedX']
                self.coord -= math.fabs(self.property['speedX'])
                if player.glued:
                    player.rect.left += self.property['speedX']/2
                    
            elif self.indexCoord == 2:
                self.rect.top += self.property['speedY']
                self.coord -= math.fabs(self.property['speedY'])
                if player.glued:
                    player.rect.top += self.property['speedY']/2

            elif self.indexCoord == 3:
                self.rect.left -= self.property['speedX']
                self.coord -= math.fabs(self.property['speedX'])
                if player.glued:
                    player.rect.left -= self.property['speedX']/2

        if self.beat != -1:
            if self.cBeat >= 150:
                self.beat = -1
                self.cBeat = 0
            else:
                self.cBeat += 10

                if self.beat == 0:
                    self.rect.left -= 10
                    player.rect.left = self.rect.right
                elif self.beat == 1:
                    self.rect.left += 10
                    player.rect.right = self.rect.left

    def setProperty(self):     
        if self.type == 'G':
            self.type = self.property['t1']
            self.type2 = self.property['t2']
            self.image.fill (WALL_COLOR[self.type])
            self.coord = self.property['coord'][0]
            self.glued = self.property['glued']
        self.getImage()

class GhostPlatform(pygame.sprite.Sprite):
    def __init__(self, x, y, type, alpha):
        pygame.sprite.Sprite.__init__(self)
        self.id = id
        self.x = x
        self.y = y
        #self.image = pygame.Surface( (PLATFORM_SIZE, PLATFORM_SIZE) )
        self.image = pygame.image.load("images/platform_P.png")
        self.mask = pygame.mask.from_surface(self.image)
        #self.image.fill (WALL_COLOR[type])
        self.screenAlpha = pygame.Surface((20,20))
        self.rect = self.image.get_rect()
        self.rect.left = x
        self.rect.top = y
        self.alpha = alpha
        self.timeAlpha = 0
        self.delayAlpha = False
        self.velAlpha = 0
        self.changeAlpha = None
        self.type = type
        self.color = WALL_COLOR[type]
        self.property = None

    def draw(self, surface):
        surface.blit(self.image, self.rect)
        surface.blit(self.screenAlpha, self.rect)

    def getImage(self):
        if self.type in ('F'):
            self.image = pygame.image.load("images/platform_"+self.type+".png")
        elif self.type in ('f'):
            self.image = pygame.image.load("images/platform_"+self.type+self.type+".png")

    def updateAlpha(self):
        if self.delayAlpha:
            self.timeAlpha += 1
            if self.timeAlpha >= 20:
                self.timeAlpha = 0
                self.delayAlpha = False
        else:

            if self.changeAlpha:
                self.alpha -= self.velAlpha
            else:
                self.alpha += self.velAlpha

            if self.alpha >= 255:
                self.alpha = 255
                self.changeAlpha = True
                self.delayAlpha = True
            elif self.alpha <= 0:
                self.alpha = 0
                self.changeAlpha = False
                self.delayAlpha = True
        
        self.setAlpha()

    def setAlpha(self):
        self.screenAlpha.set_alpha(self.alpha) # alpha level

    def setProperty(self):
        #self.getImage()
        self.alpha = self.property['alpha']
        if self.alpha == 255:
            changeAlpha  = True
        else:
            changeAlpha  = False
        self.velAlpha = self.property['velAlpha']

class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y, type):
        pygame.sprite.Sprite.__init__(self)
        self.id = id
        self.x = x
        self.y = y
        self.frames = {}
        self.frame = 0
        self.cImage = 0
        self.timedeadTime = 20
        self.cTimedeadTime = 0
        self.type = type
        self.hit = False
        self.property = None
        self.endPath = False
        self.cHit = 0

    def setProperty(self):
        self.setImage() 
        self.setFrames()
        clipMask(self)

    def setImage(self):
        group = self.property['group']

        self.frames.update({'left_up': pygame.image.load('images/enemies/'+group+'/TL.png')})
        self.frames.update({'left_down': pygame.image.load('images/enemies/'+group+'/BL.png')})
        self.frames.update({'right_up': pygame.image.load('images/enemies/'+group+'/TR.png')})
        self.frames.update({'right_down': pygame.image.load('images/enemies/'+group+'/BR.png')})

        if self.property['dir'] == 'left':
            if self.property['orientation'] == 'up':
               self.image = self.frames['left_up'] 
            elif self.property['orientation'] == 'down':
                self.image = self.frames['left_down']
        elif self.property['dir'] == 'right':
            if self.property['orientation'] == 'up':
                self.image = self.frames['right_up']
            elif self.property['orientation'] == 'down':
                self.image = self.frames['right_down']

        self.rect = self.image.get_rect()
        self.rect.top = self.y
        self.rect.left = self.x
        

    def update(self, player):
        hspeed = 0
        vspeed = 0

        if self.hit:
            if self.cHit >= 10:
                self.hit = False
                self.cHit = 0
            else:
                self.cHit += 1

        if self.property['lives'] > 0 or not self.property['canDie']:

            if not self.property['stopped']:
                if self.property['speedY'] > 0 and not self.hit:
                    if self.property['orientation'] == 'up':      
                        vspeed -= self.property['speedY']
                        if self == player.enemy and not self.property['damage']:
                            player.change_speed(0, -self.property['speedY'])
                    elif self.property['orientation'] == 'down':                    
                        vspeed += self.property['speedY']
                        if self == player.enemy and not self.property['damage']:
                            player.change_speed(0, self.property['speedY'])

                    self.rect.top += vspeed

                    if self.property['collision']:
                        collision_list = pygame.sprite.spritecollide( self, platform, False )
                        for c in collision_list:
                            if vspeed > 0:
                                self.rect.bottom = c.rect.top
                                self.property['orientation'] = 'up'
                                self.image = self.frames[self.property['dir']+'_'+'up']
                            elif vspeed < 0:
                                self.rect.top = c.rect.bottom
                                self.property['orientation'] = 'down'
                                self.image = self.frames[self.property['dir']+'_'+'down']

                    collision_list = pygame.sprite.spritecollide( self, ghPlatform, False )
                    for c in collision_list:              
                        if c.type in ('Y'):
                            self.property['stopped'] = True
                            self.endPath = True
                            #enemies.remove(self)
                            break

                        elif c.type in ('I'):
                            if self.property['group'] in ('enemy01', 'enemy03'):
                                if vspeed > 0:
                                    self.rect.bottom = c.rect.top
                                    self.property['orientation'] = 'up'
                                    self.image = self.frames[self.property['dir']+'_'+'up']
                                elif vspeed < 0:
                                    self.rect.top = c.rect.bottom
                                    self.property['orientation'] = 'down'
                                    self.image = self.frames[self.property['dir']+'_'+'down']

                if self.property['speedX'] > 0:   
                    if self.property['group'] in ('enemy01', 'enemy03'):
                        if self.property['dir'] == 'left':
                            '''if self.property['group'] == 'enemy02' and not self.hit:                         
                                hspeed += self.property['speedX']
                            else:'''
                            hspeed -= self.property['speedX']
                        elif self.property['dir'] == 'right':
                            '''if self.property['group'] == 'enemy02' and not self.hit:
                                hspeed -= self.property['speedX']
                            else:'''
                            hspeed += self.property['speedX']                          
                    
                    self.rect.left += hspeed

                    if self.property['collision']:
                        collision_list = pygame.sprite.spritecollide( self, platform, False )
                        for c in collision_list:
                            if hspeed > 0:
                                self.rect.right = c.rect.left
                            elif hspeed < 0:
                                self.rect.left = c.rect.right 

        else:
            if self.cTimedeadTime >= self.timedeadTime:
                enemies.remove(self)
            else:
                self.cTimedeadTime += 1

        
        if self.property['lives'] > 0:
            self.frame = 'idleframes'

    def setFrames(self):
        gp = self.property['group']
        if gp in ('enemy01', 'enemy03'):
            self.rect.width = 27
            self.rect.height = 58
            self.frames.update({'idleframes': [0, 1]})
            self.frames.update({'hitframes': [2, 2]})
            self.frames.update({'deadTimeframes': [2, 2]})            
        elif gp == 'enemy02':
            self.rect.width = 30
            self.rect.height = 67
            self.frames.update({'idleframes': [0, 1]})
            self.frames.update({'hitframes': [0, 1]})
            self.frames.update({'deadTimeframes': [0, 1]})

        self.frame = 'idleframes'
        self.cImage = self.frames[self.frame][0]
                      
    def draw(self, surface):
        surface.blit(self.image, self.rect, (0, math.floor(self.cImage)*self.rect.height, self.rect.width, self.rect.height))     

class Spike(pygame.sprite.Sprite):
    def __init__(self, x, y, type):
        pygame.sprite.Sprite.__init__(self)
        self.id = id
        self.x = x
        self.y = y
        self.width = PLATFORM_SIZE
        self.height = PLATFORM_SIZE
        self.image = ""
        self.hit = False
        self.type = type
        #self.color = WALL_COLOR[0]

    def getImage(self):
        if self.type == "<":
            self.image = pygame.image.load("images/spikes/spikeR.png")
        elif self.type == ">":
            self.image = pygame.image.load("images/spikes/spikeL.png")
        elif self.type == "^":
            self.image = pygame.image.load("images/spikes/spikeT.png")
        elif self.type == "v":
            self.image = pygame.image.load("images/spikes/spikeB.png")
        self.rect = self.image.get_rect()
        self.rect.top = self.y
        self.rect.left = self.x
        self.mask = pygame.mask.from_surface(self.image)

    def draw(self, surface):
        surface.blit(self.image, self.rect)

class Cannon(pygame.sprite.Sprite):
    def __init__(self, x, y, type):
        pygame.sprite.Sprite.__init__(self)
        self.id = id
        self.x = x
        self.y = y
        self.width = 40
        self.height = 40
        #self.tFire = 20
        self.image = ''
        self.type = type
        self.hit = False
        self.disable = False
        self.property = None
        #self.color = WALL_COLOR[0]
        self.hspeed = 0
        self.vspeed = 0
        
    def setProperty(self):
        img = ''
        if self.property['color'] == 'blue':
            img = 'images/cannonL.png'
        elif self.property['color'] == 'red':
            img = 'images/cannonR.png'
        self.image = pygame.image.load(img)
        self.rect = self.image.get_rect()
        self.rect.top = self.y
        self.rect.left = self.x
        self.rect.width = self.width
        self.rect.height = self.height
        self.mask = pygame.mask.from_surface(self.image)
        self.image = self.rotateImage(self.image)

    def change_speed(self, hspeed, vspeed):
        self.hspeed = hspeed
        self.vspeed = vspeed

    def update(self, player):

        self.rect.left += self.hspeed

        collision_list = pygame.sprite.spritecollide( self, platform, False )
        for c in collision_list:
            if self.hspeed > 0:
                self.rect.right = c.rect.left
            elif self.hspeed < 0:
                self.rect.left = c.rect.right

        self.hspeed = 0
        self.vspeed = 0

    def rotateImage(self, image):
        if self.property['dir'] == 'top':
            pass
        elif self.property['dir'] == 'bot':
            image, self.rect = rot_center(image, self.rect, 180)

        return image

    def draw(self, surface):
        surface.blit(self.image, self.rect)

class Blackhole(pygame.sprite.Sprite):
    def __init__(self, x, y, type):
        pygame.sprite.Sprite.__init__(self)
        self.id = id
        #self.pID = pID
        self.x = x
        self.y = y
        self.width = 40
        self.height = 40
        self.rowImage = 0
        self.cImage = 0
        self.numImages = 4
        self.image = pygame.image.load("images/blackhole.png")
        self.rect = self.image.get_rect()
        self.rect.top = self.y
        self.rect.left = self.x
        self.mask = pygame.mask.from_surface(self.image)
        #self.hit = False
        self.type = type
        self.angle = 0
        
    def draw(self, surface):
        #surface.blit(self.image, self.rect, (math.floor(self.cImage)*self.width, self.rowImage*self.height, self.width, self.height))
        v1, v2 = rot_center(self.image, self.rect, self.angle)
        surface.blit(v1, v2)
        self.angle += 20
        self.angle %= 360 

class Coin(pygame.sprite.Sprite):
    def __init__(self, x, y, type):
        pygame.sprite.Sprite.__init__(self)
        self.id = id
        self.x = x
        self.y = y
        self.width = 20
        self.height = 20
        self.cImage = 0
        self.numImages = 8
        self.type = type

    def getImage(self):
        if self.type == "o":
            self.image = pygame.image.load("images/coins/coinL.png")
        elif self.type == "O":
            self.image = pygame.image.load("images/coins/coinR.png")
        elif self.type == "0":
            self.image = pygame.image.load("images/coins/coinG.png")

        self.rect = self.image.get_rect()
        self.rect.top = self.y
        self.rect.left = self.x
        self.rect.width = 20
        self.rect.height = 20
        #self.mask = pygame.mask.from_surface(self.image)
                
    def draw(self, surface):
        surface.blit(self.image, self.rect, (math.floor(self.cImage)*self.width, 0, self.width, self.height))

class Arrow(pygame.sprite.Sprite):
    def __init__(self, x, y, type):
        pygame.sprite.Sprite.__init__(self)
        self.id = id
        self.x = x
        self.y = y
        self.width = 20
        self.height = 20
        self.cImage = 0
        self.numImages = 3
        self.hit = False
        self.type = type

    def getImage(self):
        if self.type == "A":
            self.image = pygame.image.load("images/arrowT.png")
        elif self.type == "a":
            self.image = pygame.image.load("images/arrowB.png")

        self.rect = self.image.get_rect()
        self.rect.top = self.y
        self.rect.left = self.x
        self.rect.width = self.width
        self.rect.height = self.height
        self.mask = pygame.mask.from_surface(self.image)
                
    def draw(self, surface):
        surface.blit(self.image, self.rect, (self.cImage*self.width, 0, self.width, self.height))

class Sphere(pygame.sprite.Sprite):
    def __init__(self, x, y, type):
        pygame.sprite.Sprite.__init__(self)
        self.id = id
        self.x = x
        self.y = y
        self.width = 30
        self.height = 30
        self.image = pygame.image.load("images/green_sphere.png")
        self.rect = self.image.get_rect()
        self.rect.top = self.y
        self.rect.left = self.x
        self.rect.width = self.width
        self.rect.height = self.height
        self.mask = pygame.mask.from_surface(self.image)
        self.type = type
                
    def draw(self, surface):
        surface.blit(self.image, self.rect)

class Portal(pygame.sprite.Sprite):
    def __init__(self, x, y, type):
        pygame.sprite.Sprite.__init__(self)
        self.id = id
        self.x = x
        self.y = y
        self.width = 60
        self.height = 60
        self.image = ''
        self.cImage = 0
        self.numImages = 23
        self.type = type
        self.hit = False

    def getImage(self):
        if self.type == "H":
            self.image = pygame.image.load("images/portalR.png")
        elif self.type == "h":
            self.image = pygame.image.load("images/portalL.png")
        self.rect = self.image.get_rect()
        self.rect.top = self.y
        self.rect.left = self.x
        self.rect.width = self.width
        self.rect.height = self.height
                
    def draw(self, surface):
        surface.blit(self.image, self.rect, (0, self.cImage*self.height, self.width, self.height))

class Laser(pygame.sprite.Sprite):
    def __init__(self, x, y, type):
        pygame.sprite.Sprite.__init__(self)
        self.id = id
        self.x = x
        self.y = y
        self.width = 20
        self.height = 20
        self.cImage = 0
        self.active = True
        self.timeActive = 20
        self.cTime = 0
        self.indexCoord = 0
        #self.numImages = 23
        self.type = type
        self.hit = False
        self.property = None
        self.coord = 0
        self.timeD = 0

    def setProperty(self):
        if len(self.property['coord']) > 0:
            self.coord = self.property['coord'][0]
            self.timeD = self.property['timeDelay']
        img = ''
        if self.property['color'] == 'yellow':
            img = 'images/laser/laser_yellow.png'
        elif self.property['color'] == 'red':
            img = 'images/laser/laser_red.png'
        elif self.property['color'] == 'blue':
            img = 'images/laser/laser_blue.png'
        elif self.property['color'] == 'green':
            img = 'images/laser/laser_green.png'
        self.image = pygame.image.load(img)
        self.rect = self.image.get_rect()
        self.rect.top = self.y
        self.rect.left = self.x
        self.rect.width = self.width
        self.rect.height = self.height
        self.mask = pygame.mask.from_surface(self.image)
        if self.type == '-':
            self.image, self.rect = rot_center(self.image, self.rect, 90)
            self.mask = pygame.mask.from_surface(self.image)

    def update(self, player):          
        if len(self.property['coord']) > 0:
            #self.rect.top -= self.property['speedY']          
            if self.coord <= 0:
                if self.timeD > 0:
                    self.timeD -= 1
                else:
                    if self.indexCoord == 1:
                        self.indexCoord = 0
                    else:
                        self.indexCoord = 1

                    self.coord = self.property['coord'][self.indexCoord]
                    self.timeD = self.property['timeDelay']

            else:
                if self.indexCoord == 0:
                    if self.type == '-':
                        self.rect.top -= self.property['speedUp']
                        self.coord -= math.fabs(self.property['speedUp'])
                    elif self.type == '|':
                        self.rect.left -= self.property['speedLeft']
                        self.coord -= math.fabs(self.property['speedLeft'])
                    
                elif self.indexCoord == 1:
                    if self.type == '-':
                        self.rect.top += self.property['speedDown']
                        self.coord -= math.fabs(self.property['speedDown'])
                    elif self.type == '|':
                        self.rect.left += self.property['speedRight']
                        self.coord -= math.fabs(self.property['speedRight'])              
               
    def draw(self, surface):
        if self.active:
            surface.blit(self.image, self.rect, (0, self.cImage*self.height, self.width, self.height))

class Switch(pygame.sprite.Sprite):
    def __init__(self, x, y, type):
        pygame.sprite.Sprite.__init__(self)
        self.id = id
        self.x = x
        self.y = y
        self.width = 20
        self.height = 20
        self.cImage = 0
        self.active = False
        self.timeActive = 20
        self.cTime = 0
        self.idLaser = 0
        #self.numImages = 23
        self.type = type
        self.hit = False
        self.property = None

    def setProperty(self):
        img = ''
        if self.property['color'] == 'yellow':
            img = 'images/switch/switch_yellow.png'
        elif self.property['color'] == 'red':
            img = 'images/switch/switch_red.png'
        elif self.property['color'] == 'blue':
            img = 'images/switch/switch_blue.png'
        elif self.property['color'] == 'green':
            img = 'images/switch/switch_green.png'
        self.image = pygame.image.load(img)
        self.rect = self.image.get_rect()
        self.rect.top = self.y
        self.rect.left = self.x
        self.rect.width = self.width
        self.rect.height = self.height
        #self.mask = pygame.mask.from_surface(self.image)

        sheet = self.image 
        sheet.set_clip(pygame.Rect(0, 0, self.width, self.height))
        self.frame1 = sheet.subsurface(sheet.get_clip())
        self.frame1 = self.rotateImage(self.frame1)

        sheet = self.image 
        sheet.set_clip(pygame.Rect(self.width, 0, self.width, self.height))
        self.frame2 = sheet.subsurface(sheet.get_clip())       
        self.frame2 = self.rotateImage(self.frame2)

        self.rect.top = self.y
        self.rect.left = self.x        
        
        self.mask = pygame.mask.from_surface(self.frame1)
                      
    def draw(self, surface):
        if self.active:
            surface.blit(self.frame2, self.rect)
        else:
            surface.blit(self.frame1, self.rect)


    def rotateImage(self, image):
        if self.property['dir'] == 'left':
            image, self.rect = rot_center(image, self.rect, 270)
        elif self.property['dir'] == 'right':
            image, self.rect = rot_center(image, self.rect, 90)
        elif self.property['dir'] == 'up':
            image, self.rect = rot_center(image, self.rect, 180)
        elif self.property['dir'] == 'down':
            pass

        return image

class Marker(pygame.sprite.Sprite):
    def __init__(self, x, y, type):
        pygame.sprite.Sprite.__init__(self)
        self.id = id
        self.x = x
        self.y = y
        self.image = pygame.Surface( (PLATFORM_SIZE, PLATFORM_SIZE) )
        self.rect = self.image.get_rect()
        self.rect.left = x
        self.rect.top = y
        self.type = type

    def update(self, player):
        if self.type == '@':
            rowMarker = math.fabs(round(self.rect.top/PLATFORM_SIZE))
            if rowMarker == 0:
                player.vel = self.property['speed']
        elif self.type == '*':
            if self.rect.colliderect(player.rect):
                player.vel = self.property['speed']

    def setProperty(self):
        pass

    def draw(self, surface):
        pass 

class Checkpoint(pygame.sprite.Sprite):
    def __init__(self, x, y, type):
        pygame.sprite.Sprite.__init__(self)
        self.id = id
        self.x = x
        self.y = y
        self.width = 60
        self.height = 40
        self.cImage = 0
        self.numImages = 6
        self.type = type
        self.hit = False       

    def getImage(self):
        if self.type == "X":
            self.image = pygame.image.load("images/checkpointFlagR.png")
        elif self.type == "x":
            self.image = pygame.image.load("images/checkpointFlagL.png")
        self.rect = self.image.get_rect()
        self.rect.top = self.y
        self.rect.left = self.x
        self.rect.width = self.width
        self.rect.height = self.height
                
    def draw(self, surface):
        surface.blit(self.image, self.rect, (0, math.floor(self.cImage)*self.height, self.width, self.height))

class Trampoline(pygame.sprite.Sprite):
    def __init__(self, x, y, type):
        pygame.sprite.Sprite.__init__(self)
        self.id = id
        self.x = x
        self.y = y
        self.width = 30
        self.height = 30
        self.cImage = 0
        self.numImages = 6
        self.type = type
        self.hit = False
        self.active = False

    def getImage(self):
        if self.type == "T":
            self.image = pygame.image.load("images/trampolineR.png")
        elif self.type == "t":
            self.image = pygame.image.load("images/trampolineL.png")
        self.rect = self.image.get_rect()
        self.rect.top = self.y
        self.rect.left = self.x
        self.rect.width = self.width
        self.rect.height = self.height
                
    def draw(self, surface):
        surface.blit(self.image, self.rect, (0, math.floor(self.cImage)*self.height, self.width, self.height))

class Trap(pygame.sprite.Sprite):
    def __init__(self, x, y, type):
        pygame.sprite.Sprite.__init__(self)
        self.id = id
        self.x = x
        self.y = y
        self.width = 20
        self.height = 20
        self.cImage = 0
        self.numImages = 5
        self.count = 0
        self.property = None
        self.out = False
        self.stop = False
        self.type = type
        self.hit = False

    def getImage(self):     
        if self.property['dir'] == "top":
            self.image = pygame.image.load("images/spikes/spikeTA.png")
        elif self.property['dir'] == "bot":
            self.image = pygame.image.load("images/spikes/spikeBA.png")
        elif self.property['dir'] == "left":
            self.image = pygame.image.load("images/spikes/spikeLA.png")
        elif self.property['dir'] == "right":
            self.image = pygame.image.load("images/spikes/spikeRA.png")
        self.rect = self.image.get_rect()
        self.rect.top = self.y
        self.rect.left = self.x
        self.rect.width = self.width
        self.rect.height = self.height

        clipMask(self)

    def setProperty(self):
        self.getImage()   
        
    def update(self, player):
        if self.stop:
            if self.count >= self.property['time']:
                self.count = 0
                self.stop = False
                self.out = not self.out
            else:
                self.count += 1
        else:
            if self.out:
                self.cImage -= 1
            else:
               self.cImage += 1

            if self.cImage >= self.numImages-1 or self.cImage <= 0:
                self.stop = True

    def draw(self, surface):
        print self.cImage
        surface.blit(self.image, self.rect, (math.floor(self.cImage)*self.width, 0, self.width, self.height))

def clipMask(obj):
    sheet = obj.image #Load the sheet
    sheet.set_clip(pygame.Rect(0, 0, obj.rect.width, obj.rect.height)) #Locate the sprite you want
    draw_me = sheet.subsurface(sheet.get_clip()) #Extract the sprite you want
    obj.mask = pygame.mask.from_surface(draw_me)

def rot_center(image, rect, angle):
        """rotate an image while keeping its center"""
        rot_image = pygame.transform.rotate(image, angle)
        rot_rect = rot_image.get_rect(center=rect.center)
        return rot_image,rot_rect    

def changeDimension(player, cDir, cDim, ori=0):
    image = ''
    if cDim:
        player.orientation = ori
    if player.dir == DL:  
        if cDir:
            player.dir = 1
            if player.orientation == 0:
                if player.invincible:
                    image = PLAYER_INV_RIGHT_TOP
                else:
                    image = PLAYER_RIGHT_TOP
            else:
                if player.invincible:
                    image = PLAYER_INV_RIGHT_BOT
                else:
                    image = PLAYER_RIGHT_BOT
        else:
            if player.orientation == 0:
                if player.invincible:
                    image = PLAYER_INV_LEFT_TOP
                else:
                    image = PLAYER_LEFT_TOP
            else:
                if player.invincible:
                    image = PLAYER_INV_LEFT_BOT
                else:
                    image = PLAYER_LEFT_BOT

    elif player.dir == DR:
        if cDir:
            player.dir = 0
            if player.orientation == 0:
                if player.invincible:
                    image = PLAYER_INV_LEFT_TOP
                else:
                    image = PLAYER_LEFT_TOP
            else:
                if player.invincible:
                    image = PLAYER_INV_LEFT_BOT
                else:
                    image = PLAYER_LEFT_BOT
        else:
            if player.orientation == 0:
                if player.invincible:
                    image = PLAYER_INV_RIGHT_TOP
                else:
                    image = PLAYER_RIGHT_TOP
            else:
                if player.invincible:
                    image = PLAYER_INV_RIGHT_BOT
                else:
                    image = PLAYER_RIGHT_BOT
   
    player.dimension = True
    player.image = image

def setId(list):
    id = 1
       
    for p in reversed(list):
        if p.type in ('P', 'Q', 'q', 'M', 'm', 'D', 'd', 'f', 'I', 'i', 'Y'):
            continue
        p.id = id
        id += 1

def setProperty(list, settings):
    for i in settings:
        for y in list:
            if i['t'] == y.type:
                setID = False
                if y.type in ('-', '|', '*', 'F', '#'):
                    for x in range(i['id'][0], i['id'][1]):
                        if x == y.id:
                            setID = True
                else:     
                    for x in i['id']:
                        if x == y.id:
                            setID = True
                            if y.type in ('S'):
                                y.idLaser = i['idLaser']
                                
                if setID:
                    y.property = i['property']
                    y.setProperty()

def fillMap(prop, player, r, diff):
    global portal, total, checkpoint
    total = 0
    x = y = 0
    numRow = 0
    numColumn = 0
    map = prop[0]
    settings = prop[1]
    
    for row in map:
        if r:
            row = reversed(row)
        for col in row:
            size = PLATFORM_SIZE
            if col in ('K', 'k'):
                player.type = col
                if player.checkpoint == 0:
                    player.rect.left = x
                    player.rect.top = y
                else:                    
                    player.rect.left = player.checkpoint.x
                    player.rect.top = player.checkpoint.y
                
                if col == 'K':
                    player.dir = 0
                elif col == 'k':
                    player.dir = 1
                    player.image = pygame.image.load("images/player/playerRT.png")

                if player.rect.top < SCREEN_HEIGHT:
                    player.orientation = 1
                else:
                    player.orientation = 0

            if col in ('P', 'p', 'D', 'd', 'Q', 'q', 'M', 'm', 'G'):
                P = Platform(x, y, col)
                P.getImage()
                platform.append(P)
            elif col in ('F', 'f', 'I', 'i', 'Y'):
                changeAlp = True
                alpha = 0
                if col in ('I', 'i', '*'):
                    alpha = 255
                    changeAlp = False
                if col in ('Y'):
                    alpha = 230
                    changeAlp = False
                P = GhostPlatform(x, y, col, alpha)
                P.setAlpha()
                P.changeAlpha = changeAlp
                ghPlatform.append(P)
            elif col in ('<', '>', '^', 'v'):
                S = Spike(x, y, col)
                S.getImage()
                spikes.append(S)
            elif col in ('#'):
                T = Trap(x, y, col)
                trapSpike.append(T)
            elif col in ('C'):
                C = Cannon(x, y, col)
                cannons.append(C)
            elif col in ('B'):
                B = Blackhole(x, y, col)
                blackholes.append(B)
                size = 20
            elif col in ('o', 'O', '0'):
                O = Coin(x, y, col)
                O.getImage()
                coins.append(O)
            elif col in ('A', 'a'):
                A = Arrow(x, y, col)
                A.getImage()
                clipMask(A)
                arrows.append(A)
            elif col in ('e'):
                E = Sphere(x, y, col)
                spheres.append(E)
            elif col in ('H', 'h'):
                portal = Portal(x, y, col)
                portal.getImage()
                clipMask(portal)               
            elif col in ('|', '-'):
                EP = Laser(x, y, col)
                lasers.append(EP)
            elif col in ('S', 's'):
                S = Switch(x, y, col)
                switches.append(S)
            elif col in ('E'):
                E = Enemy(x, y, col)               
                enemies.append(E)
            elif col in ('@', '*'):
                M = Marker(x, y, col)               
                markers.append(M)
            elif col in ('X', 'x'):
                checkpoint = Checkpoint(x, y, col)
                checkpoint.getImage()
                clipMask(checkpoint)
            elif col in ('T', 't'):
                T = Trampoline(x, y, col)
                T.getImage()
                clipMask(T)
                trampolines.append(T)
            x += 20
            numColumn += 1
        y += 20
        numRow += 1
        x = 0

    for e in elements:
        setId(e)
        setProperty(e, settings)
        if diff != 0:
            for i in e:
                i.rect.top += (diff/2)

    total = numRow*PLATFORM_SIZE
    moveScreen = 0

    if total < SCREEN_HEIGHT:
        if r:
            moveScreen = (SCREEN_HEIGHT - total) - (SCREEN_HEIGHT - player.rect.top - PLATFORM_SIZE)
        else:
            moveScreen = (SCREEN_HEIGHT - total) - (SCREEN_HEIGHT - PLAYER_POSITION_Y - PLATFORM_SIZE)
        for i in elements:
            for e in i:
                e.rect.top += moveScreen
                #e.y += moveScreen
        portal.rect.top += moveScreen
        checkpoint.rect.top += moveScreen
        player.rect.top += moveScreen 
    else:
        #moveScreen = math.fabs(SCREEN_HEIGHT + ((total - SCREEN_HEIGHT) - SCREEN_HEIGHT)) + (SCREEN_HEIGHT - PLAYER_POSITION_Y - PLATFORM_SIZE)
        if player.rect.top < (total - SCREEN_HEIGHT):
            moveScreen = (total - SCREEN_HEIGHT) - ((total - player.rect.top) - SCREEN_HEIGHT/2)
        else:
            moveScreen = (total - SCREEN_HEIGHT)
        for i in elements:
            for e in i:
                e.rect.top -= moveScreen
                #e.y -= moveScreen
        portal.rect.top -= moveScreen
        checkpoint.rect.top -= moveScreen
        player.rect.top -= moveScreen 

def reset(player):
    for e in elements:
        del e[:]
    portal = None
    if not player.alive:
        tempCP = player.checkpoint
        player = createPlayer(1, 0, 0)
        player.checkpoint = tempCP
        return player

def gameover(screen, labelGameOver):
    screen.blit(labelGameOver, ((SCREEN_WIDTH/2)-180, (SCREEN_HEIGHT/2)-100))
    
def main():
    pygame.init()
    screen = pygame.display.set_mode( (SCREEN_WIDTH, SCREEN_HEIGHT) )
    player = createPlayer(1, 0, 0)
    map = loadLevel(lvl)
    pygame.display.set_caption( 'VERTEX' )
    #pygame.mouse.set_visible( False )
    fillMap(map, player, False, 0)
    
    game = Game()
    game.loop( screen, player )

    game.quit()

    pygame.quit()

if __name__ == '__main__':
    main()

