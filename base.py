from  sprites import *
from tutorial import *

class Baseclass:
    def __init__(self,width=WIDTH,height=HEIGHT):

        self.exit = False
        self.screen = pg.Surface((width,height))
        self.init_groups()
        self.clock = pg.time.Clock()



        
    

    def init_groups(self):
        '''Initialize all sprite groups'''

        self.all_sprites = pg.sprite.Group()
        self.overlay = pg.sprite.Group()
        self.texts = pg.sprite.Group()


    def draw(self):

        self.screen.fill(1)
        self.all_sprites.update()
        self.all_sprites.draw(self.screen)
        self.overlay.update()
        self.overlay.draw(self.screen)
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
    def __init__(self,menu,mapid=1):
        super().__init__()

        self.mapid = mapid
        self.available_turrets = []

        self.map = Map(self)
        self.shopFlag = False

        self.screenflash = ScreenFlash(self)
        self.flash = Flash(self)
        self.life = Life(self)

        self.waiting = False

        self.coins = 10
        self.shop = ShopUI(self)
        

        self.screen = disp
    
        self.menu = menu
        

        self.paths = findpaths(self.mapid)

        self.last_switched = pg.time.get_ticks()


        self.wave = 0
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

        self.last_paused = pg.time.get_ticks()

        

        self.next_wave_button = Text(*NEXTWAVEBUTTONPOSITION,"Start Next Wave",self,32,-1,WHITE,button=1)
        self.next_wave_button.pos = (WIDTH-self.next_wave_button.rect.width)//2 , NEXTWAVEBUTTONPOSITION[1]
        self.all_sprites.add(self.next_wave_button)
        self.overlay.add(self.screenflash)
        self.overlay.add(self.flash)

        

    def init_groups(self):
        '''Initialize all sprite groups'''

        self.all_sprites = pg.sprite.Group()
        self.tiles = pg.sprite.Group()
        self.bases = pg.sprite.Group()
        self.overlay = pg.sprite.Group()
        self.turrets = pg.sprite.Group()
        self.enemies = pg.sprite.Group()
        self.shop_sprites = pg.sprite.Group()
        self.bullets = pg.sprite.Group()
    
    def events(self):
        
        self.shop.coins_text.msg = "Coins: %d"%self.coins
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
        
        
        mouse = pg.mouse.get_pos()

        if pg.time.get_ticks() - self.last_switched > 9800:
            self.flash.flash()
        
        if self.waiting:
            self.last_switched = pg.time.get_ticks()
            if self.next_wave_button.rect.collidepoint(mouse):
                self.next_wave_button.active = True
            else:
                self.next_wave_button.active = False


        self.check_collisions()
    

    def start_next_wave(self):
        now = pg.time.get_ticks()
        self.stop_spawning = False
        self.last_wave = now

        for turret in self.turrets:
            turret.refreshAmmo()

        self.shopFlag = False
        sounds['WaveStart'].play()
        mx.music.unload()
        mx.music.load(music['Wave'])
        mx.music.play(-1)
        self.wave += 1
        self.n = self.wave * ENEMYMULTIPLIER
        self.spawned_enemies = 0
        self.wave_delay = self.wave * DELAYMULTIPLIER
        self.wave_text.msg = "Wave : %d"%self.wave
        self.waiting = False
        self.shop_hide()

        self.last_switched = now
        self.last_update = now

    def shop_hide(self):
        for sprite in self.shop_sprites:
            sprite.hidden = True
    
    def shop_unhide(self):
        for sprite in self.shop_sprites:
            sprite.hidden = False


    

    def spawn_enemies(self):

        now = pg.time.get_ticks()


        if self.spawned_enemies>=self.n and not self.stop_spawning:
            self.stop_spawning = True
            self.last_wave = now

        if not self.stop_spawning:
            typ = rd.choice([0,1,2,3,4,5])
            lane = rd.choice([0,1])
            en = ENEMYCLASSES[typ](*self.enemy_positions[lane],self,lane)
            self.all_sprites.add(en)
            self.enemies.add(en)
            self.spawned_enemies += en.housingSpace
        

        if len(self.enemies)==0:
            self.waiting = True
            if not self.shopFlag:
                mx.music.unload()
                mx.music.load(music['Shop'])
                mx.music.play(-1)
                self.shopFlag = True
            self.shop_unhide()
        else:
            self.waiting = False
            self.shop_hide()


        
                    
    

    def keyevents(self,key):
        if key == pg.K_TAB:
            self.current_turret.active = False
            self.current_turret.action = 0
            self.current_turret.animation_frame = 0
            self.turret_index = (self.turret_index+1)%len(self.turrets)
            self.current_turret = self.turrets.sprites()[self.turret_index]
            self.current_turret.active = True
        
        if key == pg.K_SPACE:
            self.pausegame()

    def mouseevents(self,button,action):

        mouse = pg.mouse.get_pos()
        if self.waiting:
            if self.next_wave_button.rect.collidepoint(mouse):
                self.start_next_wave()

        if action == pg.MOUSEBUTTONDOWN and button == 1:
            mx,my = pg.mouse.get_pos()
            if not self.waiting:
                for turret in self.turrets:
                    if turret.rect.collidepoint(mx,my):
                        self.current_turret.active = False
                        self.current_turret.action = 0
                        self.current_turret.animation_frame = 0
                        self.current_turret = turret
                        self.current_turret.active = True
                self.current_turret.toggle_shoot(True)

            self.mx,self.my = pg.mouse.get_pos()
            if self.waiting:
                for icon in self.shop.turret_icons:
                    if icon.rect.collidepoint(self.mx,self.my):
                        self.shop.selected_turret = icon.value
                        self.shop.selected_turret_cost = TURRETCOSTS[self.shop.selected_turret]

                for base in self.bases:
                    if base.rect.collidepoint(self.mx,self.my):
                        if base.turret_val == -1:
                            if self.coins < self.shop.selected_turret_cost:
                                return
                            self.coins -= self.shop.selected_turret_cost
                            base.turret_val = self.shop.selected_turret
                            base.turret = TURRETCLASSES[self.shop.selected_turret](self.shop.selected_turret,base.rect.x,base.rect.y,self,base)
                            self.all_sprites.add(base.turret)
                            self.turrets.add(base.turret)
                            self.all_sprites.add(base.turret.ammobar)

        elif action == pg.MOUSEBUTTONDOWN and button == 3:
            if self.current_turret.ammo == self.current_turret.max_ammo:
                self.current_turret.toggleSuper()

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
                        enemy.hitSound.play()
                        enemy.hp -= hit.damage
    

    def pausegame(self):
        self.menu.pausemenu = PauseMenu(self,self.menu)
        self.menu.pausemenu.screen2 = disp.copy()
        self.menu.game_state = 2
        now = pg.time.get_ticks()
        self.last_paused = now 

    def gameover(self):
        sounds['GameOver'].play()
        self.menu.gameovermenu = GameoverMenu(self,self.menu)
        self.menu.gameovermenu.screen2 = disp.copy()
        self.menu.game_state = 3
    
    def unpause(self):
        now = pg.time.get_ticks()

        diff = now - self.last_paused
        
        sl = self.last_switched
        self.last_update = diff + self.last_update
        self.last_switched = diff +self.last_switched

        

        
class MainMenu(Baseclass):
    def __init__(self,game,menu):
        super().__init__()

        self.game = game

        txts = ["Play".center(10),"How to Play","Quit".center(10)]

       
        

       

        mx.music.unload()
        mx.music.load(music['MainMenu'])
        mx.music.play(-1)

       


        self.menu = menu
        
        
        self.bgsprites = pg.sprite.Group()
        for typ in BGTYPES:
            bgs = Bgsprite(self,typ)
            self.bgsprites.add(bgs)
            self.all_sprites.add(bgs)
        

        txt = Text(0*32,0*32,TITLE.center(22),self.game,72,0,GOLD,3)
        txt.pos = (WIDTH-txt.rect.width)//2 , 0*32
        self.all_sprites.add(txt)


        txt = Text(391,174,txts[0],self.game,44,1,BLACK,3)
        txt.pos = (WIDTH-txt.rect.width)//2 , 174
        self.texts.add(txt)
        self.all_sprites.add(txt)

        txt = Text(391,174+80,txts[1],self.game,44,3,BLACK,3)
        txt.pos = (WIDTH-txt.rect.width)//2 , 174+80
        self.texts.add(txt)
        self.all_sprites.add(txt)

        txt = Text(391,174+160,txts[2],self.game,44,4,BLACK,3)
        txt.pos = (WIDTH-txt.rect.width)//2 , 174+160
        self.texts.add(txt)
        self.all_sprites.add(txt)

        self.screen = disp

        
    
   


    

 
        
    
    def events(self,clicked=False):
        mouse = pg.mouse.get_pos()
        for txt in self.texts:
            if txt.rect.collidepoint(mouse):
                if txt.button>1:
                    if txt.active == False:
                        sounds['Hover'].play()
                    txt.active = True
                if clicked:
                    sounds['Click'].play()
                    if txt.ind == 1: #New Game
                        self.menu.game_state = 4
                        self.menu.mapmenu = MapMenu(self.game,self.menu)
                    
                    if txt.ind == 3: #How to Play
                        self.menu.game_state = 5
                        self.menu.htpmenu = HowtoPlayMenu(self.game,self.menu)

                    elif txt.ind == 4: #QUIT:
                        pg.quit()
                        quit()

            else:
                txt.active = False
    

        




class PauseMenu(Baseclass):
    def __init__(self,game,menu):
        super().__init__()
        
        self.game = game
       
        txts = ["Paused".center(10),"Continue","Quit".center(10)]

        txt = Text(*GAMEOVERTEXTPOSITIONS[0],txts[0],self.game,72,0,BLUE,2)
        txt.pos = (WIDTH-txt.rect.width)//2 , (HEIGHT-txt.rect.height*1.5)//2
        self.texts.add(txt)
        self.all_sprites.add(txt)
        
        txt = Text(0,0,"Press any key to continue",self.game,22,0,WHITE,2)
        txt.pos = (WIDTH-txt.rect.width)//2 , (HEIGHT+txt.rect.height*3)//2
        self.texts.add(txt)
        self.all_sprites.add(txt)
        
        txt = Text(*GAMEOVERTEXTPOSITIONS[3],txts[1],self.game,32,3,WHITE,1)
        txt.pos = (WIDTH-txt.rect.width)//2 -200, GAMEOVERTEXTPOSITIONS[3][1]
        self.texts.add(txt)
        self.all_sprites.add(txt)
        txt = Text(*GAMEOVERTEXTPOSITIONS[4],txts[2],self.game,32,4,WHITE,1)
        txt.pos = (WIDTH-txt.rect.width)//2 +200, GAMEOVERTEXTPOSITIONS[4][1]
        self.texts.add(txt)
        self.all_sprites.add(txt)

        self.menu = menu

        
        
        
        self.screen = disp
        


    def draw(self):
        
        self.screen.fill(-1)
        self.screen.blit(self.screen2,(0,0))
        self.all_sprites.update()
        self.all_sprites.draw(self.screen)
        pg.display.flip()
        self.clock.tick(60)


    
    def events(self):
        mouse = pg.mouse.get_pos()
        for txt in self.texts:
            if txt.rect.collidepoint(mouse):
                if txt.button==1:
                    txt.active = True
                clicks = pg.mouse.get_pressed()
                if clicks[0]:

                    if txt.ind == 3: #Continue
                        self.menu.game_state = 1
                        self.game.unpause()

                    elif txt.ind == 4: #QUIT:
                        pg.quit()
                        quit()

            else:
                txt.active = False
        


class GameoverMenu(Baseclass):
    def __init__(self,game,menu):
        super().__init__()
        
        self.game = game
        
        txts = ["Game Over","Waves Cleared : %d"%(self.game.wave-1),"Score : %d"%self.game.score,"Play Again","Quit".center(10)]
        for i in range(3):
            s=32 if i else 72
            txt = Text(*GAMEOVERTEXTPOSITIONS[i],txts[i],self.game,s,i,BLUE,2)
            txt.pos = (WIDTH-txt.rect.width)//2 , GAMEOVERTEXTPOSITIONS[i][1]
            self.texts.add(txt)
            self.all_sprites.add(txt)
        

        txt = Text(*GAMEOVERTEXTPOSITIONS[3],txts[3],self.game,s,3,WHITE,1)
        txt.pos = (WIDTH-txt.rect.width)//2 -200, GAMEOVERTEXTPOSITIONS[3][1]
        self.texts.add(txt)
        self.all_sprites.add(txt)
        txt = Text(*GAMEOVERTEXTPOSITIONS[4],txts[4],self.game,s,4,WHITE,1)
        txt.pos = (WIDTH-txt.rect.width)//2 +200, GAMEOVERTEXTPOSITIONS[4][1]
        self.texts.add(txt)
        self.all_sprites.add(txt)


        self.menu = menu
        
        
        self.screen = disp
        


    def draw(self):
        
        self.screen.fill(-1)
        self.screen.blit(self.screen2,(0,0))
        self.all_sprites.update()
        self.all_sprites.draw(self.screen)
        pg.display.flip()
        self.clock.tick(60)


    
    def events(self):
        mouse = pg.mouse.get_pos()
        for txt in self.texts:
            if txt.rect.collidepoint(mouse):
                if txt.button==1:
                    txt.active = True
                clicks = pg.mouse.get_pressed()
                if clicks[0]:
                    
                    if txt.ind == 3: #New Game
                        self.menu.game_state = 4

                    elif txt.ind == 4: #QUIT:
                        pg.quit()
                        quit()

            else:
                txt.active = False
        


class MapMenu(Baseclass):
    def __init__(self,game,menu):
        super().__init__()
        self.game = game
        self.menu = menu

        

        self.mapimgs = []
        for i in range(1,4):
            self.mapimgs.append(pg.image.load('Images/map%d.png'%i).convert())

        positions = [[2*32,2*32],[17*32,2*32],[10*32,10*32]]
        self.texts = pg.sprite.Group()

        for i in range(3):
            map1 = pg.sprite.Sprite()
            map1.image = self.mapimgs[i]
            map1.rect = map1.image.get_rect()
            map1.rect.topleft = positions[i]
            self.mapimgs[i] = map1
            self.all_sprites.add(map1)
            txt = Text(0,0,"Map %d"%(i+1),self.game,32,i+1,WHITE,1)
            txt.rect.center = map1.rect.center
            txt.pos = txt.rect.topleft[0],txt.rect.topleft[1] + 64

            self.texts.add(txt)
            self.all_sprites.add(txt)

        
        

        
      

        self.menu = menu
        
        
        self.screen = disp

    def generate_sprites(self):
        for i in range(30):
            typ = rd.choice([0,1,2,3,4,5])
            x=rd.randint(1,29)*32
            y = rd.randint(1,14)*32
            sli =ENEMYCLASSES[typ](x,y,self.game,0)
            sli.menu_slime = True
            self.all_sprites.add(sli)

    def draw(self):
        
        self.screen.fill(1)
        self.all_sprites.update()
        self.all_sprites.draw(self.screen)
        pg.display.flip()
        self.clock.tick(60)

    def events(self,clicked=False):
        mouse = pg.mouse.get_pos()
        for txt in self.texts:
            if txt.rect.collidepoint(mouse):
                if txt.button==1:
                    txt.active = True
                if clicked:
                    
                    if txt.ind == 1: #Map 1
                        self.menu.game = Game(self.menu,mapid=1)
                        self.menu.game_state = 1

                    elif txt.ind == 2: #Map 2
                        self.menu.game = Game(self.menu,mapid=2)
                        self.menu.game_state = 1
                    
                    elif txt.ind == 3: #Map 3
                        self.menu.game = Game(self.menu,mapid=3)
                        self.menu.game_state = 1
                        

            else:
                txt.active = False
        

        for i in range(3):
            if self.mapimgs[i].rect.collidepoint(mouse):
                self.mapimgs[i].image.set_alpha(100)
                if clicked:
                    self.menu.game = Game(self.menu,mapid=i+1)
                    self.menu.game_state = 1

            else:
                self.mapimgs[i].image.set_alpha(255)

    

            
                        


class Main(Baseclass):
    def __init__(self):
        super().__init__()
        self.game_state = 0
        self.game = Game(self)
        self.mainmenu = MainMenu(self.game,self)
    
        
        #0 == InitialMenu
        #1 == Game
        #2 == PauseMenu
        #3 == GameoverMenu
        #4 == MapSelectionMenu
        #5 == HowtoPlayMenu


    def loop(self):
        while not self.exit:

            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    sys.exit()
                
                if event.type == pg.KEYDOWN:
                    if self.game_state ==1:
                        self.game.keyevents(event.key)

                    elif self.game_state ==2:
                        self.game_state = 1
                        self.game.unpause()
                    
                        
                    
                    
                    

                if event.type == pg.MOUSEBUTTONDOWN or event.type == pg.MOUSEBUTTONUP:
                    if self.game_state ==1:
                        self.game.mouseevents(event.button,event.type)
                    
                
                if event.type == pg.MOUSEBUTTONDOWN:
                    if self.game_state == 5:
                        self.htpmenu.events(clicked=True)
                    elif self.game_state == 0:
                        self.mainmenu.events(clicked=True)
                    elif self.game_state == 4:
                        self.mapmenu.events(clicked=True)
                   


            if self.game_state == 0:
                #menu
                self.mainmenu.events()
                self.mainmenu.draw()

            elif self.game_state ==1:
                #game
                self.game.events()
                self.game.draw()
            
            elif self.game_state == 2:
                self.pausemenu.events()
                self.pausemenu.draw()
            
            elif self.game_state == 3:
                self.gameovermenu.events()
                self.gameovermenu.draw()
            
            elif self.game_state == 4:
                self.mapmenu.events()
                self.mapmenu.draw()
            
            elif self.game_state == 5:
                self.htpmenu.events()
                self.htpmenu.draw()

                



class HowtoPlayMenu(Baseclass):
    def __init__(self,game,menu):
        super().__init__()
        self.game = game 
        self.menu = menu

        self.page = 0

    
        self.load_texts()


        self.screen = disp

    
    def turretpage(self,isslime=False):

        n = len(TURRETCLASSES)

        if isslime:
            n = 6
            txt = Text(18*32,14*32,"Back To Main Menu".center(5),self.game,32,2,WHITE,1)
            self.texts.add(txt)
            self.all_sprites.add(txt)
            self.backbut = txt
        
        
        y=4*32
        for i in range(n):
            x=3*32
            ms = MenuSprite(i,x,y,self.game,isslime)
            self.all_sprites.add(ms)
            x+=3*32
            txt = Text(x,y,ms.name,self.game,32,0,WHITE)
            self.texts.add(txt)
            self.all_sprites.add(txt)
            x+=8*32
            txt = Text(x,y,ms.damage,self.game,32,0,WHITE)
            self.texts.add(txt)
            self.all_sprites.add(txt)
            x+=6*32
            txt = Text(x,y,ms.cost,self.game,32,0,WHITE)
            self.texts.add(txt)
            self.all_sprites.add(txt)

            y+=32+16
            



    

    def load_texts(self):
        
        self.nextbut = None
        self.prevbut = None
        self.backbut = None
        self.texts = pg.sprite.Group()
        self.all_sprites = pg.sprite.Group()
        
        x = 2*32
        y = 1*32
        for msg in TEXTDUMP[self.page]:
            txt = Text(x,y,msg,self.game,32,0,WHITE)
            self.texts.add(txt)
            self.all_sprites.add(txt)
            y+=32+16
        
        if self.page<5:
            txt = Text(24*32,14*32,"Next".center(5),self.game,32,2,WHITE,1)
            self.texts.add(txt)
            self.all_sprites.add(txt)
            self.nextbut = txt
        if self.page>0:
            txt = Text(3*32,14*32,"Prev".center(5),self.game,32,3,WHITE,1)
            self.texts.add(txt)
            self.all_sprites.add(txt)
            self.prevbut = txt
        
        if self.page==4:
            self.turretpage()
            
        elif self.page == 5:
            self.turretpage(True)
            


    def draw(self):
        self.screen.fill(1)
        self.all_sprites.update()
        self.all_sprites.draw(self.screen)
        pg.display.flip()



    def events(self,clicked=False):
        mouse = pg.mouse.get_pos()
        if self.nextbut:
            if self.nextbut.rect.collidepoint(mouse):
                self.nextbut.active = True
                if clicked:
                    self.page+=1
                    self.load_texts()
                    pg.time.wait(200)
                    return
            else:
                self.nextbut.active = False
        
        if self.prevbut:
            if self.prevbut.rect.collidepoint(mouse):
                self.prevbut.active = True
                if clicked:
                    
                    self.page-=1
                    self.load_texts()
                    pg.time.wait(200)
                    
            else:
                self.prevbut.active = False
        
        if self.page==5 and self.backbut:
            if self.backbut.rect.collidepoint(mouse):
                self.backbut.active = True
                if clicked:
                    pg.time.wait(200)
                    self.menu.game_state = 0
            else:
                self.backbut.active = False

        


        

main = Main()
main.loop()