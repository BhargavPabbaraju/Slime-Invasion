import math  
from pygame.math import Vector2 as vec
from utility import *
from settings import *

class Bullet(pg.sprite.Sprite):
    def __init__(self):
        

        super().__init__()

        self.image = pg.Surface((50,100))
        self.rect = self.image.get_rect()

class Arrow(Bullet):
    def __init__(self,x,y,angle):
        super().__init__()

        #Properties
        self.speed = 12.5
        self.last_time = 0
        self.angle = angle 

        self.image = pg.image.load('Images/arrow.png')
        self.image = pg.transform.rotate(self.image,self.angle)
        self.image = pg.transform.scale(self.image,(int(self.image.get_width()*1.25),int(self.image.get_height()*1.25)))
        self.rect = self.image.get_rect()
    
        self.rect.center =x,y
        self.last_update = 300

        self.v = vec()
        self.v.from_polar((self.speed,-self.angle))
        self.rect.center = vec(self.rect.x,self.rect.y)

    def update(self):
        if pg.time.get_ticks() - self.last_update > 10:
            self.rect.center += self.v
            self.last_update = pg.time.get_ticks()
        
        #self.rect.x += self.speed * math.cos(math.radians(self.angle)) * deltaTime(self.last_time)
        #self.rect.y += self.speed * math.sin(math.radians(self.angle)) * deltaTime(self.last_time)
        self.last_time = pg.time.get_ticks()