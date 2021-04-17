from  sprites import *

class Baseclass:
    def __init__(self,width=WIDTH,height=HEIGHT):

        self.exit = False
        self.screen = pg.Surface((width,height))
        self.init_groups()
        self.clock = pg.time.Clock()
    

    def init_groups(self):
        '''Initialize all sprite groups'''

        self.all_sprites = pg.sprite.Group()
        


    def draw(self):

        self.screen.fill(1)
        self.all_sprites.update()
        self.all_sprites.draw(self.screen)
        pg.display.flip()
        self.clock.tick(60)

    def events(self):
        '''Check for mouse click or key press events'''
        pass

    def loop(self):
        while not self.exit:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    sys.exit()
            self.events()
            self.draw()


class Menu(Baseclass):
    def __init__(self):
        super().__init__()
    
    def events(self):
        for event in pg.event.get():
            if event.type == pg.KEYUP:
                self.exit = True




class Game(Baseclass):
    def __init__(self):
        super().__init__()

        self.mapid = 1
        
        

        self.map = Map(self)

        en = Enemy('Images/enemies.png',0,0,self,1,0)
        self.all_sprites.add(en)
        
        self.screen = disp
        
        self.last_update = pg.time.get_ticks()
        self.enemy_spawn_delay = 500

        self.paths = findpaths(self.mapid)
    

    def init_groups(self):
        '''Initialize all sprite groups'''

        self.all_sprites = pg.sprite.Group()
        self.tiles = pg.sprite.Group()
        self.turrets = pg.sprite.Group()
        self.enemies = pg.sprite.Group()
        self.bullets = pg.sprite.Group()
    
    def events(self):
        mx,my = pg.mouse.get_pos()
        
        now = pg.time.get_ticks()

        if now - self.last_update > self.enemy_spawn_delay:
            self.spawn_enemies()
            self.last_update = now
        
        self.check_collisions()
    

    def spawn_enemies(self):
        if len(self.enemies)>1:
            return
        typ = rd.choice([0,1])
        lane = 0#rd.choice([0,1])
        en = ENEMYCLASSES[typ](*self.enemy_positions[lane],self,lane)
        self.all_sprites.add(en)
        self.enemies.add(en)

        
                    
    

    def keyevents(self,key):
        if key == pg.K_TAB:
            self.current_turret.active = False
            self.current_turret.action = 0
            self.current_turret.animation_frame = 0
            self.turret_index = (self.turret_index+1)%len(self.turrets)
            self.current_turret = self.turrets.sprites()[self.turret_index]
            self.current_turret.active = True

    def mouseevents(self,button,action):
        if action == pg.MOUSEBUTTONDOWN and button == 1:
            mx,my = pg.mouse.get_pos()
            for turret in self.turrets:
                if turret.rect.collidepoint(mx,my):
                    self.current_turret.active = False
                    self.current_turret.action = 0
                    self.current_turret.animation_frame = 0
                    self.current_turret = turret
                    self.current_turret.active = True
            self.current_turret.toggle_shoot(True)
        elif action == pg.MOUSEBUTTONUP and button == 1:
            self.current_turret.toggle_shoot(False)
    

    def check_collisions(self):
        pg.sprite.groupcollide(self.bullets, self.enemies,True, True)



                        


class Main(Baseclass):
    def __init__(self):
        super().__init__()
        self.game_state = 1
        self.menu = Menu()
        self.game = Game()
        #0 == Menu
        #1 == Game

    def loop(self):
        while not self.exit:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    sys.exit()
                
                if event.type == pg.KEYDOWN:
                    if self.game_state ==1:
                        self.game.keyevents(event.key)

                if event.type == pg.MOUSEBUTTONDOWN or event.type == pg.MOUSEBUTTONUP:
                    self.game.mouseevents(event.button,event.type)


            if self.game_state == 0:
                #menu
                self.menu.events()
                self.menu.draw()

            elif self.game_state ==1:
                #game
                self.game.events()
                self.game.draw()
    
    



        
    

main = Main()
main.loop()