from bullet import *
from turret import *
from enemy import *
from utility import *
from settings import *
from life import *
from text import *
from background import *


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

        self.origimg = self.image

        self.last_update = pg.time.get_ticks()
        self.update_thres = 200

        self.offset = 1


    
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
    
    def update(self):
        if self.type=="0" and self.game.mapid==3:

            now = pg.time.get_ticks()

            
            if now - self.last_update > self.update_thres:
            
                self.image = pg.Surface((32,32))
                self.image.blit(self.origimg,(0,-self.offset))
                self.image.blit(self.origimg,(0,self.offset))
                self.offset+=1

                if self.offset==15:
                    self.offset = 1

            
                self.last_update = now
        


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
            base = Base(y,x)
            if not first_turret:
                first_turret = base
            self.game.bases.add(base)
            self.game.all_sprites.add(base)
            '''
            tur = TURRETCLASSES[t](t,x,y,self.game)
            if not first_turret:
                first_turret = tur

            self.game.turrets.add(tur)
            self.game.all_sprites.add(tur.base)
            self.game.all_sprites.add(tur)
            self.game.all_sprites.add(tur.ammobar)'''

        self.fturret = TURRETCLASSES[0](0,first_turret.rect.x,first_turret.rect.y,self.game,first_turret)
        first_turret.turret_val = 0
        first_turret.turret = self.fturret
        self.game.all_sprites.add(self.fturret)
        self.game.turrets.add(self.fturret)
        self.game.current_turret = self.fturret
        self.game.all_sprites.add(self.fturret.ammobar)
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

        #print(self.game.available_turrets)

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

        #print(pg.time.get_ticks(),self.game.last_switched,self.game.menu.game_state)
        self.new_alpha = 150 * (pg.time.get_ticks() - self.game.last_switched)/15000
        self.image.set_alpha(Lerp(self.image.get_alpha(),self.new_alpha,deltaTime(self.last_time)))
        self.last_time = pg.time.get_ticks()
        self.game.clock.tick(60)

class Flash(ScreenFlash):
    def __init__(self,game):
        super().__init__(game)
        self.image = pg.transform.scale(pg.image.load('Images/flash.png').convert_alpha(),(960,544))
        self.last_flash = 600
        self.flashed = False

    def update(self):
        if self.flashed and pg.time.get_ticks() - self.last_flash < 200:
            self.image.set_alpha(Lerp(self.image.get_alpha(),255,8 * deltaTime(self.last_time)))
        else :
            self.flashed = False
            self.image.set_alpha(Lerp(self.image.get_alpha(),0,3 * deltaTime(self.last_time)))
        self.last_time = pg.time.get_ticks()
        self.game.clock.tick(60)

    def flash(self):
        if self.flashed:
            return
        self.flashed = True
        self.last_flash = pg.time.get_ticks()



class MenuSprite(pg.sprite.Sprite):
    def __init__(self,ind,x,y,game,isslime=False):
        super().__init__()

        self.ind =ind
        
        self.pos = x,y
        self.isslime = isslime

        self.game = game 

        i=self.ind
        if not self.isslime:

            self.damage = str(TURRETDAMAGES[i])
            self.name = TURRETNAMES[i]
            self.cost = str(TURRETCOSTS[i])
        
            self.image = TURRETIMAGES[i]

        else:
            self.cost = str(SLIMESPEEDS[i])
            self.name = SLIMECOLORS[i]
            self.damage = str(SLIMEHEALTHS[i])

            self.image = pg.Surface((32,32))
            self.image.set_colorkey((0,0,0))
            self.sheet = pg.image.load('Images/slime%d.png'%i).convert_alpha()
            self.image.blit(self.sheet,(0,0),[0,0,32,32])

        self.rect = self.image.get_rect()
        self.rect.topleft = self.pos

        


