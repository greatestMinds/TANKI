from pygame import *
from win32api import GetSystemMetrics
from random import random

class Basic(sprite.Sprite):

    def __init__(self,x,y,width,height,speed,image,face="up"):
        super().__init__()

        self.upimage = image
        self.image = image
        self.image = transform.scale(self.image,(width,height))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.x = x
        self.y = y
        self.speed = speed

    def resetxy(self):
        self.rect.x = self.x
        self.rect.y = self.y

    def reset(self):
        win.blit( self.image, (self.x,self.y) )
    
    def update(self):
        self.reset()

class Bullet(Basic):

    def __init__(self,x,y,width,height,speed=20,image=image.load("circ.png")):
        super().__init__(x,y,width,height,speed,image)
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.speed = speed
        self.image = transform.scale(image,(width,height))
        self.face = player.face

    def update(self):
        if self.face == "left":
            self.x -= self.speed
        elif self.face == "right":
            self.x += self.speed
        elif self.face == "up":
            self.y -= self.speed
        elif self.face == "down":
            self.y += self.speed
        self.reset()
        self.resetxy()

        

class Hero(Basic):
    def update(self):
        keys = key.get_pressed()
        if keys.count(True)==1:
            if keys[K_a]:
                self.face = "left"
                self.x -= self.speed
                self.image = transform.rotate(self.upimage,90)
            if keys[K_d]:
                self.face = "right"
                self.x += self.speed
                self.image = transform.rotate(self.upimage,-90)
            if keys[K_w]:
                self.face = "up"
                self.y -= self.speed
                self.image = self.upimage
            if keys[K_s]:
                self.face = "down"
                self.y += self.speed
                self.image = transform.rotate(self.upimage,180)
        
        if keys[K_SPACE]:
            self.fire()
        self.resetxy()
        self.reset()
    
    def fire(self):
        NewBullet = Bullet(self.x,self.y,25,25)
        bullets.add(NewBullet)


width = GetSystemMetrics(0)
height = GetSystemMetrics(1)
win = display.set_mode((width,height),flags=FULLSCREEN)

def cutImage(NEED_LEFTCOR,NEED_RIGHTCOR,PIC_NAME="sprites.png"):

    IMAGE = image.load(PIC_NAME)
    Height = NEED_RIGHTCOR[1] - NEED_LEFTCOR[1]
    Width = NEED_RIGHTCOR[0] - NEED_LEFTCOR[0]

    return IMAGE.subsurface(Rect(NEED_LEFTCOR,(Width,Height)))

PlayerImage = cutImage((0,0),(35,38))
EnemyImage = cutImage((320,0),(355,38))
BricksImage = cutImage((640,0),(675,38))
EagleImage = cutImage((761,81),(761+41,81+38)) #ширина спрайта(37-38) + расстояние меж ними = 41

player = Hero(x=500,y=500,width=40,height=40,speed=4,image=PlayerImage,face="up")

def control():
    for i in event.get():
        if i.type == QUIT:
            exit()
        elif i.type == KEYDOWN:
            if i.key == K_ESCAPE:
                exit()

timer = time.Clock()

class Wall(Basic):
    def update(self):
        if sprite.collide_rect(self,player):
            walls.remove(self)
        self.reset()
        
walls = sprite.Group()
bullets = sprite.Group()
lvl_pool = []

def generate_line():
    lvl = []
    for i in range(int(width/40)):
        if random() > 0.7:
            lvl.append("кирпич")
        else:
            lvl.append("пустота")
    lvl_pool.append(lvl)

for i in range(int(height/40)):
    generate_line()

for n in range(len(lvl_pool)):
    for i in range(len(lvl_pool[n])):
        if lvl_pool[n][i] == "кирпич":
            walls.add(Wall(x=i*40,y=n*40,width=40,height=40,speed=0,image=BricksImage))

while True:

    control()
    win.fill((0,0,0))
    walls.update()
    bullets.update()
    sprite.groupcollide(bullets,walls,True,True)
    player.update()
    timer.tick(60)
    display.update()
