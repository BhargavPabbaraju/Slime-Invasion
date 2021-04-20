from settings import *
from utility import *
from bullet import *
from text import *


class Turret(pg.sprite.Sprite):
    def __init__(self,type,r,c,game,base):
        super().__init__()

        self.type = type
        self.r = r -1
        self.c = c -1
        self.x = self.r
        self.y = self.c
        self.game = game
        self.last_time = pg.time.get_ticks()
        self.ammo = 5
        self.max_ammo = 5

        self.base = base
        self.sheet = Spritesheet('Images/CrossbowSheet.png')
        self.image = self.sheet.scale(0,0,48,32,(0,0,0),1.25)
        self.spr = self.image.copy()
        self.rect = self.image.get_rect()
        self.base.rect.topleft = self.x,self.y
        self.animation_framerate = 52
        self.rect.center = self.base.rect.center
        self.shot = False
        self.max_ammo = 25
        self.ammo = self.max_ammo
        self.ammobar = AmmoBar(self.ammo,self.game,self.rect.x,self.rect.y)

        
        #load animations
        self.animation_database = self.sheet.load_animation(48,32,(0,0,0),1)

        #animation variables
        self.action = 0
        self.animation_frame = 0

        self.image = pg.Surface((50,100))
        self.rect = self.image.get_rect()

        self.active = False

    def update(self):
        self.ammobar.set_ammo(int(self.ammo))
        if not self.active:
            self.ammo += 2 * deltaTime(self.last_time)
            if self.ammo > self.max_ammo:
                self.ammo = self.max_ammo
            self.image = self.animation_database[self.action][self.animation_frame]
            self.rect = self.image.get_rect()
            self.rect.center = [self.base.rect.center[0],self.base.rect.center[1]]
            self.last_time = pg.time.get_ticks()
            return

        if self.action != 1:
            self.ammo += 0.5 * deltaTime(self.last_time)
            if self.ammo > self.max_ammo:
                self.ammo = self.max_ammo
        self.animation_frame += deltaTime(self.last_time) * self.animation_framerate
        if int(self.animation_frame) >= len(self.animation_database[self.action]):
            self.animation_frame = 0

        self.mx,self.my = pg.mouse.get_pos()
        self.angle = math.degrees(math.atan2(self.mx-self.rect.center[0],self.my-self.rect.center[1])) - 90
        self.image = pg.transform.rotate(self.animation_database[self.action][int(self.animation_frame)],self.angle)
        self.rect = self.image.get_rect()
        self.rect.center = [self.base.rect.center[0],self.base.rect.center[1]]

        if (self.action == 1 and self.ammo <= 0):
            self.action = 0

        if(self.action == 1 and int(self.animation_frame) <= 2):
            self.shot = False

        #shoot projectile
        if(self.action == 1 and int(self.animation_frame) >= 5 and not self.shot and self.ammo > 0):
            #shoot
            self.shoot()
        self.last_time = pg.time.get_ticks()

    def shoot(self):
        self.shot = True
        self.ammo -= 1
        self.arrow = Arrow(*self.rect.center,self.angle,5)
        self.arrow.damage = CROSSBOWDAMAGE
        self.game.all_sprites.add(self.arrow)
        self.game.bullets.add(self.arrow)
        self.arrow.rect.center = self.rect.center

    def toggle_shoot(self,val):
        if self.action == val:
            return
        self.action = val
        self.animation_frame = 0

class ShopUI(pg.sprite.Sprite):
    def __init__(self,game):
        super().__init__()
        self.game = game
        self.turret_icons = pg.sprite.Group()
        game.all_sprites.add(self)
        self.image = pg.image.load('Images/shopUI_bg.png')
        self.rect = self.image.get_rect()
        self.rect.x = WIDTH - self.image.get_width()
        self.rect.y = 0
        self.selected_turret = 0
        self.selected_turret_cost = 0
        self.coins_text = Text(self.rect.x + 20,self.rect.y + 500,"Coins: %d"%self.game.coins,self,16)
        self.game.all_sprites.add(self.coins_text)

        for x in range(len(self.game.available_turrets)):
            self.icon = pg.sprite.Sprite(self.game.all_sprites)
            self.icon.image = pg.transform.scale(TURRETIMAGES[self.game.available_turrets[x]],(90,80))
            self.icon.rect = self.icon.image.get_rect()
            self.icon.rect.x = self.rect.x
            self.icon.rect.y = self.rect.y + 100*x
            self.icon.value = self.game.available_turrets[x]
            self.turret_icons.add(self.icon)
            self.icon.cost_text = Text(self.icon.rect.x + 20,self.icon.rect.y + 80,"Cost: %d"%TURRETCOSTS[x],self.game,16)
            self.game.all_sprites.add(self.icon.cost_text)

class Base(pg.sprite.Sprite):
    def __init__(self,x,y):
        super().__init__()
        self.image = Spritesheet('Images/TowerBaseStone.png').scale(0,0,32,32,(0,0,0),1.5)
        self.rect = self.image.get_rect()
        self.turret_val = -1
        self.turret = None
        self.rect.center = [x*32,y*32]

class AmmoBar(pg.sprite.Sprite):
    def __init__(self,maxammo,game,x,y):
        super().__init__()
        self.maxammo = maxammo
        self.ammo = maxammo
        self.imagesource = pg.image.load('Images/redsquare.png').convert()
        self.image = pg.transform.scale(self.imagesource,(self.ammo * AMMOBARWIDTH,5))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def set_ammo(self,ammo):
        self.ammo = ammo

    def update(self):
        self.image = pg.transform.scale(self.imagesource,(abs(int((self.ammo/self.maxammo) * AMMOBARWIDTH)),5))

class CrossbowTurret(Turret):
    def __init__(self,type,r,c,game,base):
        super().__init__(type,r,c,game,base)

class TripleCrossbowTurret(Turret):
    def __init__(self,type,r,c,game,base):
        super().__init__(type,r,c,game,base)
        self.sheet = Spritesheet('Images/TripleCrossbowSheet.png')
        self.animation_framerate = 15
        
        self.animation_database = self.sheet.load_animation(48,32,(0,0,0),1)

    def shoot(self):
        self.shot = True
        self.ammo -= 3
        for x in range(3):
            self.arrow = Arrow(*self.rect.center,self.angle - 7 + 7*x,0)
            self.arrow.image = pg.image.load('Images/arrow2.png')
            self.arrow.setImage()
            self.arrow.speed = 12
            self.arrow.formVel()
            self.arrow.damage = TRIPLECROSSBOWDAMAGE
            self.game.all_sprites.add(self.arrow)
            self.game.bullets.add(self.arrow)
            self.arrow.rect.center = self.rect.center

class CannonTurret(Turret):
    def __init__(self,type,r,c,game,base):
        super().__init__(type,r,c,game,base)
        self.sheet = Spritesheet('Images/CannonSheet.png')
        self.animation_framerate = 10
        self.animation_database = self.sheet.load_animation(48,32,(0,0,0),1)

TURRETCLASSES = {
    0 : CrossbowTurret,
    1 : TripleCrossbowTurret,
    2 : CannonTurret
}

TURRETIMAGES = {
    0 : pg.image.load('Images/CrossbowIcon.png'),
    1 : pg.image.load('Images/TripleCrossbowIcon.png'),
    2 : pg.image.load('Images/CannonIcon.png')
}

TURRETCOSTS = {
    0 : 10,
    1 : 15,
    2 : 15
}

