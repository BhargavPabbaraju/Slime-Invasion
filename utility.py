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

old_time = 0

def deltaTime(last_time):
    dt = pg.time.get_ticks() - last_time
    old_time = last_time
    return dt/1000


def findpaths(mapid):
    file = open('Maps/paths%s.txt'%(str(mapid).zfill(3)))
    lines = file.readlines()

    paths = [[],[]]
    n_paths = int(lines[1])
    curline = 2

    for line in lines[curline:curline+n_paths]:
        paths[0].append(list(map(int,line.split())))
    
    curline+=n_paths+1
    n_paths = int(lines[1])
    curline+=1

    for line in lines[curline:curline+n_paths]:
        paths[1].append(list(map(int,line.split())))
    

    return paths

