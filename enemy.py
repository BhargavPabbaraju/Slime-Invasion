  
from utility import *
from enemypaths import * 

class Enemy(pg.sprite.Sprite):
    def __init__(self,file,x,y,game,speed,lane):
        

        super().__init__()

        self.game = game
        self.lane = lane

        self.sheet = Spritesheet(file)

        self.color = (0,0,0)
        self.index = 0
        self.x = x
        self.y = y

        self.imagify()
        
        
        self.last_update = pg.time.get_ticks()
        self.update_thres = 250

        self.last_moved = pg.time.get_ticks()
        self.move_thres = 100

        self.animation_database = self.sheet.load_animation(32,32,self.color,1)

        self.speed = speed 

        self.vel = vec()
        self.vel.from_polar((self.speed,0))

        self.vel2 = vec()
        self.vel.from_polar((self.speed,90))


    def imagify(self):
        self.image = self.sheet.scale(self.index*32,0*32,32,32,self.color,1)
        self.rect = self.image.get_rect()
        self.rect.topleft = self.x,self.y
    


    
    def update(self):
        
        now = pg.time.get_ticks()
        

        if now - self.last_update > self.update_thres:
            
            self.index = (self.index+1)%4
            self.imagify()
            
            self.last_update = now
        
       
        




class GreenSlime(Enemy):
    
    def __init__(self,x,y,game,lane):
        super().__init__('Images/slime0.png',x,y,game,5,lane)
        
        



class BlueSlime(Enemy):

    def __init__(self,x,y,game,lane):
        super().__init__('Images/slime1.png',x,y,game,10,lane)





ENEMYCLASSES = {
    0 : GreenSlime,
    1 : BlueSlime
}
