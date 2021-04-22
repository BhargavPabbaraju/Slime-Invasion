from settings import *
from text import *



class Bgsprite(pg.sprite.Sprite):
    def __init__(self,menu,typ,x=0,y=0):
        super().__init__()
        self.menu = menu
        self.type = typ
        self.image = pg.image.load('Images/background/%s.png'%self.type).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.topleft = x,y
