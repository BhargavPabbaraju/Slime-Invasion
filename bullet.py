import math
from utility import *
from settings import *

class Bullet(pg.sprite.Sprite):
    def __init__(self,x,y,angle,spread):
        

        super().__init__()

        #Properties
        self.speed = 20
        self.last_time = 0
        self.deviation = (rd.random()-0.5) * spread
        self.angle = angle + self.deviation

        self.image = pg.image.load('Images/arrow.png')
        self.setImage()
        self.rect = self.image.get_rect()
    
        self.rect.center =x,y
        self.last_update = 300

        self.formVel()
        self.rect.center = vec(self.rect.x,self.rect.y)

    def formVel(self):
        self.v = vec()
        self.v.from_polar((self.speed,-self.angle))

    def setImage(self):
        self.image = pg.transform.rotate(self.image,self.angle)
        self.image = pg.transform.scale(self.image,(int(self.image.get_width()*1.25),int(self.image.get_height()*1.25)))

    def update(self):
        if pg.time.get_ticks() - self.last_update > 10:
            self.rect.center += self.v
            self.last_update = pg.time.get_ticks()
        
        #self.rect.x += self.speed * math.cos(math.radians(self.angle)) * deltaTime(self.last_time)
        #self.rect.y += self.speed * math.sin(math.radians(self.angle)) * deltaTime(self.last_time)
        self.last_time = pg.time.get_ticks()

class Arrow(Bullet):
    def __init__(self,x,y,angle,spread):
        super().__init__(x,y,angle,spread)

class Bolt(Bullet):
    def __init__(self,x,y,angle,spread):
        super().__init__(x,y,angle,spread)
        self.image = pg.image.load('Images/arrow2.png')
        self.setImage()
        self.speed = 15
        self.formVel()
        self.damage = TRIPLECROSSBOWDAMAGE

class Cannonball(Bullet):
    def __init__(self,x,y,angle,spread):
        super().__init__(x,y,angle,spread)
        self.image = pg.image.load('Images/Cannonball.png')
        self.setImage()
        self.speed = 30
        self.formVel()
        self.damage = CANNONDAMAGE

class Shot(Bullet):
    def __init__(self,x,y,angle,spread):
        super().__init__(x,y,angle,spread)
        self.image = pg.transform.scale(pg.image.load('Images/shot.png'),(6,6))
        self.setImage()
        self.speed = 15
        self.formVel()
        self.damage = SCATTERSHOTDAMAGE