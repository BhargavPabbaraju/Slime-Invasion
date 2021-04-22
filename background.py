from settings import *
from utility import *
from text import *



class Bgsprite(pg.sprite.Sprite):
    def __init__(self,menu,typ,x=0,y=0):
        super().__init__()
        self.menu = menu
        self.type = typ
        self.image = pg.image.load('Images/background/%s.png'%self.type).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.topleft = x,y
        self.offset = 0
        self.speed = 0.25
        self.dir = 0
        self.speed_thres = 1
        if self.type in ["bushleft","treeleft","slimeblue"]:
            self.dir = -1
        else:
            self.dir = 1
        
        self.last_update = pg.time.get_ticks() + rd.randint(100,200)
        self.update_thres = 50
        self.pos_offset = 0 -self.offset

        self.limit = 10

    def update(self):
        if self.type in ["bg","bg1","title"]:
            return

        now = pg.time.get_ticks()
        
        self.pos_offset = 0 - self.rect.x

        if now - self.last_update >= self.update_thres:
            self.offset += self.speed
            if abs(self.offset) > self.speed_thres:
                if self.offset < 0:
                    self.offset = -self.speed_thres
                else :
                    self.offset = self.speed_thres
            if abs(self.pos_offset) > self.limit:
                self.dir = -self.dir
                self.rect.x += self.speed_thres * self.dir
                self.offset = 0
            self.rect.x += self.offset* self.dir

            self.last_update = now