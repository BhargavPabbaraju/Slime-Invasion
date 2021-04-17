  
from utility import *

class Enemy(pg.sprite.Sprite):
    def __init__(self,type=0,x=370,y=300):
        

        super().__init__()

        self.sheet = Spritesheet('Images/enemies.png')

        self.color = (0,0,0)
        self.index = 0
        self.type = 0
        self.x = x
        self.y = y

        self.imagify()
        
        
        self.last_update = pg.time.get_ticks()
        self.update_thres = 250

        self.animation_database = self.sheet.load_animation(32,32,self.color,1.5)

    def imagify(self):
        self.image = self.sheet.scale(self.index*32,self.type*32,32,32,self.color,1.5)
        self.rect = self.image.get_rect()
        self.rect.topleft = self.x,self.y
        
    
    def update(self):
        
        now = pg.time.get_ticks()
        

        if now - self.last_update > self.update_thres:
            
            self.index = (self.index+1)%4
            self.imagify()
            
            self.last_update = now

            