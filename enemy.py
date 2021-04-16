  
from settings import *

class Enemy(pg.sprite.Sprite):
    def __init__(self):
        

        super().__init__()

        self.image = pg.Surface((50,100))
        self.rect = self.image.get_rect()