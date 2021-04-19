from bullet import *
from turret import *
from enemy import *
from utility import *
from settings import *
from life import *

class Tile(pg.sprite.Sprite):
    def __init__(self,type,row,column,game):
        super().__init__()
        self.game = game
        self.type = type

        self.row = row
        self.column = column

        self.sheet = Spritesheet('Images/tiles%s.png'%(str(self.game.mapid).zfill(3)))

        self.size = 32

        self.bgcolor = (37,52,49)

        self.imagify()
    
    def letters_to_numbers(self):
        '''
        Get the spritsheet row index based on tile type
        '''

        if self.type in ['g','s']:
            return 0
        
        elif self.type in ['d','i']:
            return 1
        
        elif self.type == "0":
            return 2


    def imagify(self):
    
        self.frame = rd.choice([0,1,2])

        self.index = self.letters_to_numbers()

        self.image = self.sheet.get(self.frame*self.size,self.size*self.index,self.size,self.size,self.bgcolor)
        self.rect = self.image.get_rect()

        self.rect.topleft = self.column*self.size , self.row*self.size
    

    def passable(self):
        if self.type == '0':
            return False
        
        return True
        


class Map(pg.sprite.Sprite):
    def __init__(self,game):
        super().__init__()
        self.rows = 17
        self.columns = 30
        self.size = 32
        self.game = game
        self.mapid = self.game.mapid

        self.create_map()
    

    def create_map(self):
        
        file = open('Maps/map%s.txt'%(str(self.mapid).zfill(3)))
        lines = file.readlines()
        curline = 1
        i=0
        j=0
        for line in lines[curline:curline+self.rows]:
            row=[]
            j=0
            for val in line.split():
                row.append(val)
                tile = Tile(val,i,j,self.game)
                self.game.tiles.add(tile)
                self.game.all_sprites.add(tile)
                j+=1
            
            i+=1
        
        curline+=self.rows+1
        n_turrets = int(lines[curline])
        curline+=1

        first_turret = None
        for line in lines[curline:curline+n_turrets]:
            t,x,y = map(int,line.split())
            tur = TURRETCLASSES[t](t,x,y,self.game)
            if not first_turret:
                first_turret = tur

            self.game.turrets.add(tur)
            self.game.all_sprites.add(tur.base)
            self.game.all_sprites.add(tur)
            self.game.all_sprites.add(tur.ammobar)

        first_turret.active = True
        self.game.current_turret = first_turret
        self.game.turret_index = 0


        curline+=n_turrets+1

        self.game.enemy_positions={0:[],1:[]}
 
        self.game.enemy_positions[0] = list(map(int,lines[curline].split()))
        self.game.enemy_positions[1] = list(map(int,lines[curline+1].split()))

        curline += 3
        n_avail_turrets = int(lines[curline])
        curline+=1
        for line in lines[curline:curline+n_avail_turrets]:
            self.game.available_turrets.append(int(line))

        print(self.game.available_turrets)

        file.close()


class ScreenFlash(pg.sprite.Sprite):
    def __init__(self,game):
        super().__init__()

        self.image = pg.image.load('Images/ScreenFlash.png').convert_alpha()
        self.rect = self.image.get_rect()

        self.image.set_alpha(0)

        self.last_time = pg.time.get_ticks()

        self.game = game
    
    def update(self):

        self.new_alpha = 255 * (pg.time.get_ticks() - self.game.last_switched)/15000
        self.image.set_alpha(Lerp(self.image.get_alpha(),self.new_alpha,deltaTime(self.last_time)))
        self.last_time = pg.time.get_ticks()
        self.game.clock.tick(60)

