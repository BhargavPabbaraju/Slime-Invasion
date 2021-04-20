from pygame.math import Vector2 as vec
from utility import *


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
        self.apparantX = self.x
        self.apparantY = self.y
        self.waypoint_index = 0
        self.waypoints = self.game.paths[self.lane]
        self.target = self.waypoints[self.waypoint_index]
        self.isActive = True

        self.pos = vec(self.x,self.y)
        self.imagify()
        
        
        
        self.last_update = pg.time.get_ticks()
        self.last_update2 = pg.time.get_ticks()
        self.update_thres = 200
        self.update_thres2 = 10

        self.last_moved = pg.time.get_ticks()
        self.move_thres = 100

        #self.last_switched = pg.time.get_ticks()

        self.animation_database = self.sheet.load_animation(32,32,self.color,1)
        self.animation_frame = 0
        self.action = 0
        self.animation_framerate = 5
        self.dropchance = 20

        self.speed = speed 

        self.vel = vec()
        self.vel.from_polar((self.speed,0))

        self.vel2 = vec()
        self.vel2.from_polar((self.speed,-90))

        self.rect.topleft = vec(self.x,self.y)
        self.apparantPos = vec(self.apparantX,self.apparantY)
        

    def imagify(self):
        self.image = self.sheet.scale(self.index*32,0*32,32,32,self.color,1)
        self.rect = self.image.get_rect()
        self.rect.topleft = vec(self.x,self.y)
        self.hitrect = self.rect.copy()
        self.hitrect.height = 20
        
        
    

    def move(self):
        if self.rect.x < self.target[0]:
            self.apparantPos += self.vel
        elif self.rect.x > self.target[0]:
            self.apparantPos -= self.vel
        elif self.rect.y > self.target[1]:
            self.apparantPos += self.vel2
        elif self.rect.y < self.target[1]:
            self.apparantPos -= self.vel2

        if self.rect.y >= self.target[1] - 5 and self.rect.y <= self.target[1] + 5 and self.rect.x >= self.target[0] - 5 and self.rect.x <= self.target[0] + 5:
        #if self.rect.y == self.target[1] and self.rect.x == self.target[0]:
            if self.waypoint_index+1 < len(self.waypoints):
                self.waypoint_index += 1
                self.target = self.waypoints[self.waypoint_index]
            else :
                self.game.life.deduct()
                self.kill()

        self.rect.topleft = vec(int(self.apparantPos.x),int(self.apparantPos.y))
        self.x = self.rect.x
        self.y = self.rect.y

    def switch_lane(self):
        if not self.isActive:
            return
        len1 = len(self.game.paths[0])
        len2 = len(self.game.paths[1])

        ind = self.waypoint_index

        factor = max(len1,len2)/min(len1,len2)
        
        if self.lane == 0:
            if len1 == max(len1,len2):
                ind = int(ind//factor)

            else:
                ind = int(ind*factor)
            self.lane = 1
            if ind>=len2:
                self.kill()
        
        else:
            if len2 == max(len1,len2):
                ind = int(ind/factor)

            else:
                ind = int(ind*factor)
            self.lane = 0
            if ind>=len1:
                self.kill()

        
        self.waypoint_index = ind
        
        self.waypoints = self.game.paths[self.lane]
        self.target = self.waypoints[self.waypoint_index]
        self.apparantPos = vec(*self.target)




    
    def update(self):
        self.animation_frame += deltaTime(self.last_update) * self.animation_framerate
        if int(self.animation_frame) >= len(self.animation_database[self.action]):
            if self.action == 2:
                self.action = 3
            elif self.action ==3:
                self.kill()
            self.animation_frame = 0
            if self.action == 0:
                self.action = 1
            elif self.action ==1:
                self.action = 0

        self.image = self.animation_database[self.action][int(self.animation_frame)]
        
        if not self.isActive:
            self.last_update = pg.time.get_ticks()
            return

        now = pg.time.get_ticks()

      

        if now - self.last_update2 > self.update_thres2:
            self.move()

            self.last_update2 = now
        
  

        if self.hp<=0:
            #self.kill()
            self.isActive = False
            self.action = 2
            for x in range(5):
                self.rand = rd.randint(1,100)
                if self.rand <= self.dropchance:
                    self.game.coins += 1
            self.game.score += SLIMESCORES[self.type]
            self.game.score_text.msg = "Score : %d"%self.game.score
           

        self.last_update = pg.time.get_ticks()

        self.hitrect = self.rect.copy()
        self.hitrect.height = 20
        self.hitrect.bottom = self.rect.bottom

        


class GreenSlime(Enemy):
    
    def __init__(self,x,y,game,lane):
        super().__init__('Images/slime0.png',x,y,game,1,lane)
        
        self.hp = GREENSLIMEHEALTH

        self.type = 0


class BlueSlime(Enemy):

    def __init__(self,x,y,game,lane):
        super().__init__('Images/slime1.png',x,y,game,1,lane)

        self.hp = BLUESLIMEHEALTH
        self.dropchance = 30
        self.type = 1


class PinkSlime(Enemy):

    def __init__(self,x,y,game,lane):
        super().__init__('Images/slime2.png',x,y,game,1,lane)

        self.hp = PINKSLIMEHEALTH
        self.dropchance = 40
        self.type = 2


class OrangeSlime(Enemy):

    def __init__(self,x,y,game,lane):
        super().__init__('Images/slime3.png',x,y,game,1.5,lane)

        self.hp = PINKSLIMEHEALTH
        self.dropchance =   10
        self.type = 3

class YellowSlime(Enemy):

     def __init__(self,x,y,game,lane):
        super().__init__('Images/slime4.png',x,y,game,0.5,lane)

        self.hp = PINKSLIMEHEALTH
        self.dropchance =   60
        self.type = 4

class TealSlime(Enemy):

     def __init__(self,x,y,game,lane):
        super().__init__('Images/slime5.png',x,y,game,0.5,lane)

        self.hp = PINKSLIMEHEALTH
        self.dropchance =   50
        self.type = 5


ENEMYCLASSES = {
    0 : GreenSlime,
    1 : BlueSlime,
    2 : PinkSlime,
    3 : OrangeSlime,
    4 : YellowSlime,
    5 : TealSlime
}
