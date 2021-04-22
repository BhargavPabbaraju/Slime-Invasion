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
        self.offset = 0
        self.dir = 0
        if self.type in ["bushleft","treeleft","slimeblue"]:
            self.dir = 0
        else:
            self.dir = 1
        
        self.last_update = pg.time.get_ticks() + rd.randint(100,200)
        self.update_thres = 200

        self.limit = 10

    def update(self):
        return
        if self.type in ["bg","bg1","title"]:
            return

        now = pg.time.get_ticks()
        
        
        
        if now - self.last_update > self.update_thres:
            if self.offset >= self.limit:
                self.dir = 0 if self.dir==1 else 1
            elif self.offset<=0:
                self.dir = 0 if self.dir==1 else 1

            if self.dir==0:
                self.offset+=1
            
        
            else:
                self.offset-=1

            #print(self.type,self.offset)
            self.rect.x+=self.offset
            self.last_update=now
        
        
        
        

