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
        self.waypoint_index = 0
        self.lane = 0
        self.waypoints = self.game.paths[self.lane]
        self.target = self.waypoints[self.waypoint_index]

        self.pos = vec(self.x,self.y)
        self.imagify()
        
        
        
        self.last_update = pg.time.get_ticks()
        self.last_update2 = pg.time.get_ticks()
        self.update_thres = 250
        self.update_thres2 = 10

        self.last_moved = pg.time.get_ticks()
        self.move_thres = 100

        self.animation_database = self.sheet.load_animation(32,32,self.color,1)

        self.speed = speed 

        self.vel = vec()
        self.vel.from_polar((self.speed,0))

        self.vel2 = vec()
        self.vel2.from_polar((self.speed,-90))

        self.rect.topleft = vec(self.x,self.y)

    def imagify(self):
        self.image = self.sheet.scale(self.index*32,0*32,32,32,self.color,1)
        self.rect = self.image.get_rect()
        self.rect.topleft = vec(self.x,self.y)
    

    def move(self):
        if self.rect.x < self.target[0]:
            self.rect.topleft += self.vel
        elif self.rect.x > self.target[0]:
            self.rect.topleft -= self.vel
        elif self.rect.y > self.target[1]:
            self.rect.topleft += self.vel2
        elif self.rect.y < self.target[1]:
            self.rect.topleft -= self.vel2

        if self.rect.y == self.target[1] and self.rect.x == self.target[0]:
            self.waypoint_index += 1
            self.target = self.waypoints[self.waypoint_index]

        self.x = self.rect.x
        self.y = self.rect.y
    
    def update(self):
        
        now = pg.time.get_ticks()
        

        if now - self.last_update > self.update_thres:
            self.index = (self.index+1)%4
            self.imagify()

            self.pos += self.vel
            
            self.last_update = now
        if now - self.last_update2 > self.update_thres2:
            self.move()

            self.last_update2 = now

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
