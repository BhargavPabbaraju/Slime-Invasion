from settings import *

class Spritesheet(pg.sprite.Sprite):
    def __init__(self,file):
        super().__init__()
        self.file =  pg.image.load(file).convert()
        
    
    def get(self,x,y,w,h,color = (0,0,0)):
        #self.file.set_colorkey()
        surf = pg.Surface((w,h))
        surf.set_colorkey(color)
        surf.blit(self.file,(0,0),[x,y,w,h])
        return surf
    
    def scale(self,x,y,w,h,color,scale=1):
        surf = self.get(x,y,w,h,color)
        surf = pg.transform.scale(surf,(int(w*scale),int(h*scale)))
        return surf
    
    def load_animation(self,sprite_width,sprite_height,colorkey,scale):
        animation_database  = []
        for yindex in range(int(self.file.get_height()/sprite_height)):
            animation_database.append([])
            for xindex in range(int(self.file.get_width()/sprite_width)):
                animation_database[yindex].append(self.scale(sprite_width*xindex,sprite_height*yindex,sprite_width,sprite_height,colorkey,scale))

        return animation_database
