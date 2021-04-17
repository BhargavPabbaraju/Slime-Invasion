from settings import *
from utility import *
from bullet import *
import math

class Turret(pg.sprite.Sprite):
    def __init__(self,type,r,c,game):
        super().__init__()

        self.type = type
        self.r = r -1
        self.c = c -1
        self.x = self.c*32 
        self.y = self.r*32
        self.game = game
        self.last_time = pg.time.get_ticks()


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
        self.animation_framerate = 22
        self.rect.center = self.base.rect.center
        self.shot = False

        #load animations
        self.animation_database = self.sheet.load_animation(48,32,(0,0,0),1.75)

        #animation variables
        self.action = 0
        self.animation_frame = 0


    def update(self):
        if not self.active:
            self.image = self.animation_database[self.action][self.animation_frame]
            self.rect = self.image.get_rect()
            self.rect.center = [self.base.rect.center[0],self.base.rect.center[1]]
            return

        self.animation_frame += deltaTime(self.last_time) * self.animation_framerate
        if int(self.animation_frame) >= len(self.animation_database[self.action]):
            self.animation_frame = 0

        self.mx,self.my = pg.mouse.get_pos()
        self.angle = math.degrees(math.atan2(self.mx-self.rect.center[0],self.my-self.rect.center[1])) - 90
        self.image = pg.transform.rotate(self.animation_database[self.action][int(self.animation_frame)],self.angle)
        self.rect = self.image.get_rect()
        self.rect.center = [self.base.rect.center[0],self.base.rect.center[1]]

        if(self.action == 1 and int(self.animation_frame) == 5):
            self.shot = False

        #shoot projectile
        if(self.action == 1 and int(self.animation_frame) == 6 and not self.shot):
            #shoot
            self.shot = True
            self.arrow = Arrow(*self.rect.center,self.angle)
            self.game.all_sprites.add(self.arrow)
            self.game.bullets.add(self.arrow)

            self.arrow.rect.center = self.rect.center
            #pg.draw.rect(self.game.screen,(255,0,0),[*self.rect.center,4,4])
            #pg.draw.rect(self.game.screen,(0,255,0),[*self.arrow.rect.center,4,4])
            #pg.display.flip()
            #pg.time.wait(100)

        self.last_time = pg.time.get_ticks()

    def toggle_shoot(self,val):
        if self.action == val:
            return
        self.action = val
        self.animation_frame = 0


TURRETCLASSES = {
    0 : CrossbowTurret
}
