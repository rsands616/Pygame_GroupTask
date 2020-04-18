'''Author/s: Jackabel, Joshobel, Ryanabelle, Anni
Desc: Obstacle folder which holds all different variants of the obstacles in
    the game. This is imported into the main game file'''
import pygame, random, math

#w,h = 1024, 576
#screen.get_height()
#screen.get_width()
global MAP_UNIT_X
global MAP_UNIT_Y
MAP_UNIT_X = 25
MAP_UNIT_Y = 25

class Obstacle(pygame.sprite.Sprite):

    def __init__(self, x, y, sizex = int(2*MAP_UNIT_X), sizey = int(2*MAP_UNIT_Y), speed_x=0, speed_y=0):
        super().__init__()
        self.sizex = sizex
        self.sizey = sizey
        self.image = pygame.transform.scale(pygame.image.load(self.image),
                                            (self.sizex, self.sizey))
        self.rect = self.image.get_rect()#.inflate(-50,50)
        self.rect.x = x
        self.rect.y = y
        self.i = random.randint(1,7)
        self.seconds = 0
        self.speed_x=speed_x
        self.speed_y=speed_y

    def ob_update(self):
        ##delete method later
        pass

class Block(Obstacle):
    type = "block"
    image = 'images/wall.png'

    def collide(self, player,x_collision_vector,y_collision_vector):
        if x_collision_vector > 0:
            player.rect.right = self.rect.left
            player.on_left_wall = True
        else:
            player.on_left_wall = False
        if  x_collision_vector < 0:
            player.rect.left = self.rect.right
            player.on_right_wall = True
        else:
            player.on_right_wall = False
        if y_collision_vector > 0:
            player.rect.bottom = self.rect.top
            player.on_ground = True
            player.in_jump = False
            player.vy = 0
        else:
            player.on_ground = False
        if y_collision_vector < 0:
            player.rect.top = self.rect.bottom
            player.on_ceiling = True
            player.vy = 0
        else:
            player.on_ceiling = False

    def ob_update(self):
    ## 1/5 chance to set block to rusted variant

        if self.i == 8:
                self.background = 'images/wall1.png'
                self.image = pygame.transform.scale(pygame.image.load(self.background),
                                            (self.sizex, self.sizey))

class Block_Corner(Block):
    type = 'block'
    image = 'images/wallcorner.png'
    
class Block_Corner2(Block):
    type = 'block'
    image = 'images/wallcorner2.png'
    
class Block_Corner3(Block):
    type = 'block'
    image = 'images/wallcorner3.png'
    
class Block_Corner4(Block):
    type = 'block'
    image = 'images/wallcorner4.png'
    
class Block_Point(Block):
    type = 'block'
    image = 'images/wallpoint.png'
    
class Block_Corner_Snow(Block):
    type = 'block'
    image = 'images/wallcornerS.png'
    
class Block_Corner2_Snow(Block):
    type = 'block'
    image = 'images/wallcorner2S.png'
    
class Block_Corner3_Snow(Block):
    type = 'block'
    image = 'images/wallcorner3S.png'
    
class Block_Corner4_Snow(Block):
    type = 'block'
    image = 'images/wallcorner4S.png'
    
class Block_Snow(Block):
    type = 'block'
    image = 'images/wallS.png'


class Block_Move(Block):
    ##default class for blocks which collide with a player
    type = "block"
    image = 'images/wall.png'
    speed_x = 0.08*MAP_UNIT_X

    def ob_update(self):
        ##update movement (speed) and animation (background) of ufo
        self.seconds +=1
        if self.seconds % 100 == 0:
                self.speed_x = 0.08*MAP_UNIT_X
        elif self.seconds % 50 == 0:
            self.speed_x = -0.08*MAP_UNIT_X
            #self.background = 'images/ufo1.png'
           # self.image = pygame.transform.scale(pygame.image.load(self.background),
                                      #      (self.sizex, self.sizey))
       # elif self.seconds % 25 == 0:
            #self.background = 'images/ufo2.png'
            #self.image = pygame.transform.scale(pygame.image.load(self.background),
            #                                (self.sizex, self.sizey))
        self.rect.x += self.speed_x
        
class UFO_Steal(Block):
    ##default class for blocks which collide with a player
    type = "block"
    image = 'images/ufo2.png'
    speed_x = 0.08*MAP_UNIT_X

    def ob_update(self):
        ##update movement (speed) and animation (background) of ufo
        self.seconds +=1
        self.speed_x = 10
        self.rect.x += self.speed_x

class Text_Graphic_1(Block):
    ##default class for blocks which collide with a player
    type = "block"
    image = 'images/textGraphic1.png'
    
class Text_Graphic_2(Block):
    ##default class for blocks which collide with a player
    type = "block"
    image = 'images/textGraphic2.png'

class Text_Graphic_3(Block):
    ##default class for blocks which collide with a player
    type = "block"
    image = 'images/textGraphic3.png'
    

class Flame_UFO(Block):
    ##ufo that travels up and down a length of time (seconds)
    type = "flameufo"
    image = 'images/flame3.png'
    sizex = 0.8*MAP_UNIT_X
    sizey = 0.8*MAP_UNIT_Y

    def collide(self, player,x_collision_vector,y_collision_vector):
        player.die()

    def ob_update(self):
        ##update movement (speed) and animation (background) of ufo
        self.seconds +=1

        if self.seconds % 20 == 0:
                self.background = 'images/flame1.png'
                self.image = pygame.transform.scale(pygame.image.load(self.background),
                                            (self.sizex, self.sizey))
        elif self.seconds % 10 == 0:
            self.background = 'images/flame2.png'
            self.image = pygame.transform.scale(pygame.image.load(self.background),
                                            (self.sizex, self.sizey))

        if self.seconds % 50 == 0:
                self.speed_y = self.speed_y*(-1)

        self.rect.y += self.speed_y

class Flame_Move(Block):
    ##ufo that travels up and down a length of time (seconds)
    type = "flameufo"
    image = 'images/flame3.png'
    sizex = 0.8*MAP_UNIT_X
    sizey = 0.8*MAP_UNIT_Y

    def collide(self, player,x_collision_vector,y_collision_vector):
        player.die()

    def ob_update(self):
        ##update movement (speed) and animation (background) of ufo
        self.seconds +=1

        if self.seconds % 20 == 0:
                self.background = 'images/flame1.png'
                self.image = pygame.transform.scale(pygame.image.load(self.background),
                                            (self.sizex, self.sizey))
        elif self.seconds % 10 == 0:
            self.background = 'images/flame2.png'
            self.image = pygame.transform.scale(pygame.image.load(self.background),
                                            (self.sizex, self.sizey))

        if self.seconds % 100 == 0:
                self.speed_x = self.speed_x*(-1)

        self.rect.x += self.speed_x



class Block_Fall(Obstacle):
    ##default class for blocks which collide with a player
    type = "block"
    image = 'images/wallFall.png'
    falling = False
    speed_y = 0.02*MAP_UNIT_Y

    def collide(self, player,x_collision_vector,y_collision_vector):
        if x_collision_vector > 0:
            player.rect.right = self.rect.left
            player.on_left_wall = True
        else:
            player.on_left_wall = False
        if  x_collision_vector < 0:
            player.rect.left = self.rect.right
            player.on_right_wall = True
        else:
            player.on_right_wall = False
        if y_collision_vector > 0:
            player.rect.bottom = self.rect.top
            player.on_ground = True
            player.in_jump = False
            player.vy = 0
            self.falling = True
        else:
            player.on_ceiling = False
        if y_collision_vector < 0:
            player.rect.top = self.rect.bottom
            player.on_ceiling = True
            player.vy = 0
            self.falling = True


    def ob_update(self):
        ##update movement (speed) of falling block
        self.speed_y = 2
        if self.falling == True:
            self.rect.y += self.speed_y

class Floor(Block):
    type = "block"
    image = 'images/floor.png'

    def ob_update(self):
        pass

class Flame(Block):
    type = "flame"
    image = 'images/flame3.png'
    sizex = 0.8*MAP_UNIT_X
    sizey = 0.8*MAP_UNIT_Y

    def collide(self, player,x_collision_vector,y_collision_vector):
        player.die()

    def ob_update(self):
        self.seconds +=1

        '''if self.seconds % 150 == 0:
                self.background = 'images/flame3.png'
                self.image = pygame.transform.scale(pygame.image.load(self.background),
                                            (self.sizex, self.sizey))'''
        if self.seconds % 30 == 0:
                self.background = 'images/flame1.png'
                self.image = pygame.transform.scale(pygame.image.load(self.background),
                                            (self.sizex, self.sizey))
        elif self.seconds % 15 == 0:
            self.background = 'images/flame2.png'
            self.image = pygame.transform.scale(pygame.image.load(self.background),
                                            (self.sizex, self.sizey))

        # Instant death
        # Account for the size of the image and walking into it

class Ufo_Y2Y(Block):
    ##ufo that travels up and down a length of time (seconds)
    type = "ufoy2y"
    image = 'images/ufo1.png'
    sizex = 0.8*MAP_UNIT_X
    sizey = 0.8*MAP_UNIT_Y
    speed_y = 0.08*MAP_UNIT_Y

    def ob_update(self):
        ##update movement (speed) and animation (background) of ufo
        self.seconds +=1
        if self.seconds % 100 == 0:
                self.speed_y = 0.08*MAP_UNIT_Y
        elif self.seconds % 50 == 0:
            self.speed_y = -0.08*MAP_UNIT_Y
            self.background = 'images/ufo1.png'
            self.image = pygame.transform.scale(pygame.image.load(self.background),
                                            (self.sizex, self.sizey))
        elif self.seconds % 25 == 0:
            self.background = 'images/ufo2.png'
            self.image = pygame.transform.scale(pygame.image.load(self.background),
                                            (self.sizex, self.sizey))
        self.rect.y += self.speed_y

class Back_Ground_Object(Obstacle):
    ##ufo that travels up and down a length of time (seconds)
    type = "ufoy2y"
    image = 'images/ufo1.png'
    sizex = 0.8*MAP_UNIT_X
    sizey = 0.8*MAP_UNIT_Y
    speed_y = 0.08*MAP_UNIT_Y

    def ob_update(self):
        ##update movement (speed) and animation (background) of ufo
        self.seconds +=1
        if self.seconds % 100 == 0:
                self.speed_y = 0.08*MAP_UNIT_Y
        elif self.seconds % 50 == 0:
            self.speed_y = -0.08*MAP_UNIT_Y
            self.background = 'images/ufo1.png'
            self.image = pygame.transform.scale(pygame.image.load(self.background),
                                            (self.sizex, self.sizey))
        elif self.seconds % 25 == 0:
            self.background = 'images/ufo2.png'
            self.image = pygame.transform.scale(pygame.image.load(self.background),
                                            (self.sizex, self.sizey))
        self.rect.y += self.speed_y


class Glue(Block):
    type = "glue"
    image = 'images/glue.jpg'
    burst_image = 'images/splatter.jpg'
    sizex = 0.8*MAP_UNIT_X
    sizey = 0.8*MAP_UNIT_Y
    slow_vx = 0.04*MAP_UNIT_X
    timer = 5
    active = False

    def collide(self, player, x_collision_vector, y_collision_vector):
        Block.collide(self, player, x_collision_vector, y_collision_vector)
        player.in_glue = True


class Coin(Obstacle):
    type="coin"
    image='images/coin.png'
    sizex = int(0.8 * MAP_UNIT_X)
    sizey = int(0.8 * MAP_UNIT_Y)
    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self)
        self.image=pygame.transform.scale(pygame.image.load(self.image),
                                          (self.sizex,self.sizey))
        self.rect=self.image.get_rect()
        self.rect.x=x
        self.rect.y=y

    def collide(self,player,vx,vy):
        player.score+=50
        self.kill()
