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



    





class Game(Baseclass):
    def __init__(self,menu):
        super().__init__()

        self.mapid = 1
        self.available_turrets = []

        self.map = Map(self)

        self.screenflash = ScreenFlash(self)
        self.all_sprites.add(self.screenflash)
        self.life = Life(self)
        self.shop = ShopUI(self)
        

        self.screen = disp
    
        self.menu = menu
        

        self.paths = findpaths(self.mapid)

        self.last_switched = pg.time.get_ticks()


        self.wave = 1
        self.n = self.wave * ENEMYMULTIPLIER
        self.spawned_enemies = 0
        self.wave_delay = self.wave * DELAYMULTIPLIER

        self.last_update = pg.time.get_ticks()
        self.last_wave = pg.time.get_ticks()
        self.stop_spawning = False

        self.wave_text = Text(*WAVETEXTPOSITION,"Wave : %d"%self.wave,self,32)
        self.all_sprites.add(self.wave_text)
        
        self.score = 0
        self.score_text = Text(*SCORETEXTPOSITION,"Score : %d"%self.score,self,32)
        self.all_sprites.add(self.score_text)
    

    def init_groups(self):
        '''Initialize all sprite groups'''

        self.all_sprites = pg.sprite.Group()
        self.tiles = pg.sprite.Group()
        self.bases = pg.sprite.Group()
        self.turrets = pg.sprite.Group()
        self.enemies = pg.sprite.Group()
        #self.antienemies = pg.sprite.Group()
        self.bullets = pg.sprite.Group()
    
    def events(self):
        self.life.update()
        mx,my = pg.mouse.get_pos()
        
        now = pg.time.get_ticks()

        if now - self.last_update > INBETWEENDELAY*10**3:
            self.spawn_enemies()
            self.last_update = now

        if now - self.last_switched > 10000:
            for enemy in self.enemies:
                enemy.switch_lane()
            
            self.last_switched = now
        
        

        self.check_collisions()
        
    

    def spawn_enemies(self):

        now = pg.time.get_ticks()


        if self.spawned_enemies==self.n and not self.stop_spawning:
            self.stop_spawning = True
            self.last_wave = now

        
        if now - self.last_wave > self.wave_delay * 10**3:
            self.stop_spawning = False
            self.last_wave = now

            self.wave += 1
            self.n = self.wave * ENEMYMULTIPLIER
            self.spawned_enemies = 0
            self.wave_delay = self.wave * DELAYMULTIPLIER
            self.wave_text.msg = "Wave : %d"%self.wave
            



        


        

        if not self.stop_spawning:
            typ = rd.choice([0,1])
            lane = rd.choice([0,1])
            en = ENEMYCLASSES[typ](*self.enemy_positions[lane],self,lane)
            self.all_sprites.add(en)
            self.enemies.add(en)
            self.spawned_enemies += 1
        



        
                    
    

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

            self.mx,self.my = pg.mouse.get_pos()
            for icon in self.shop.turret_icons:
                if icon.rect.collidepoint(self.mx,self.my):
                    self.shop.selected_turret = icon.value

            for base in self.bases:
                if base.rect.collidepoint(self.mx,self.my):
                    if base.turret_val == -1:
                        base.turret_val = self.shop.selected_turret
                        base.turret = TURRETCLASSES[self.shop.selected_turret](self.shop.selected_turret,base.rect.x,base.rect.y,self,base)
                        self.all_sprites.add(base.turret)
                        self.turrets.add(base.turret)
                        self.all_sprites.add(base.turret.ammobar)
        elif action == pg.MOUSEBUTTONUP and button == 1:
            self.current_turret.toggle_shoot(False)
    

    def new_collide(self,sprite1,sprite2):
        if sprite1.hitrect.colliderect(sprite2.rect):
            return True
        
        return False

        
    def check_collisions(self):
        for enemy in self.enemies:
            hits = pg.sprite.spritecollide(enemy,self.bullets,True,self.new_collide)
            if hits:
                for hit in hits:
                    if(enemy.isActive):
                        enemy.hp -= hit.damage

    def gameover(self):
        self.menu.gameovermenu = GameoverMenu(self,self.menu)
        self.menu.gameovermenu.screen2 = disp.copy()
        self.menu.game_state = 3


        


class GameoverMenu(Baseclass):
    def __init__(self,game,menu):
        super().__init__()
        
        self.game = game
        self.texts = pg.sprite.Group()
        txts = ["Game Over","Waves Cleared : %d"%self.game.wave,"Highscore : %d"%self.game.score,"Play Again","Quit"]
        txts2 = []
        txt = Text(*GAMEOVERTEXTPOSITIONS[0],txts[0],self.game,72,0,BLUE,2)
        txt.pos = (WIDTH-txt.rect.width)//2 , GAMEOVERTEXTPOSITIONS[0][1]
        txts2.append(txt)
        txt = Text(*GAMEOVERTEXTPOSITIONS[1],txts[1],self.game,32,0,BLUE,2)
        txt.pos = (WIDTH-txt.rect.width)//2 , GAMEOVERTEXTPOSITIONS[1][1]
        txts2.append(txt)


        for txt in txts2:
            self.texts.add(txt)
            self.all_sprites.add(txt)
        
        
        
        self.screen = disp
        


    def draw(self):
        
        self.screen.fill(-1)
        self.screen.blit(self.screen2,(0,0))
        self.all_sprites.update()
        self.all_sprites.draw(self.screen)
        pg.display.flip()
        self.clock.tick(60)


    
    def events(self):
        pass

        
            
                        


class Main(Baseclass):
    def __init__(self):
        super().__init__()
        self.game_state = 1
        self.game = Game(self)
        
        #0 == InitialMenu
        #1 == Game
        #2 == PauseMenu
        #3 == GameoverMenu

    def loop(self):
        while not self.exit:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    sys.exit()
                
                if event.type == pg.KEYDOWN:
                    if self.game_state ==1:
                        self.game.keyevents(event.key)
                        self.game.gameover()
                    
                    

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
            
            elif self.game_state == 3:
                self.gameovermenu.events()
                self.gameovermenu.draw()

                



        

main = Main()
main.loop()