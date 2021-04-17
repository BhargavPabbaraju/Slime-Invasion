from settings import *
from utility import *
import math

class Turret(pg.sprite.Sprite):
    def __init__(self,type,r,c,game):
        super().__init__()

        self.type = type
        self.r = r -1
        self.c = c -1
        self.x = self.c*32 
        self.y = self.r*32


        self.image = pg.Surface((50,100))
        self.rect = self.image.get_rect()

        self.active = False

class Base(pg.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = Spritesheet('Images/TowerBaseStone.png').scale(0,0,32,32,(0,0,0),2)
        self.rect = self.image.get_rect()

class CrossbowTurret(Turret):
    def __init__(self,type,r,c,game):
        super().__init__(type,r,c,game)

        self.base = Base()
        self.sheet = Spritesheet('Images/CrossbowSheet.png')
        self.image = self.sheet.scale(0,0,48,32,(0,0,0),1.75)
        self.spr = self.image.copy()
        self.rect = self.image.get_rect()
        self.base.rect.topleft = self.x,self.y
        self.rect.center = self.base.rect.center

        #load animations
        self.animation_database = load_animation('Images/CrossbowSheet.png',48,32,(0,0,0),1.75)

        #animation variables
        self.action = 0
        self.animation_frame = 0


    def update(self):
        if not self.active:
            return
        self.mx,self.my = pg.mouse.get_pos()
        self.angle = math.degrees(math.atan2(self.mx-self.rect.center[0],self.my-self.rect.center[1])) - 90

        self.image = pg.transform.rotate(self.animation_database[self.action][self.animation_frame],self.angle)
        self.rect = self.image.get_rect()
        self.rect.center = [self.base.rect.center[0],self.base.rect.center[1]]





TURRETCLASSES = {
    0 : CrossbowTurret
}
