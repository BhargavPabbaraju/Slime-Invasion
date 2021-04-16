from  sprites import *





class Baseclass:
    def __init__(self,width=WIDTH,height=HEIGHT):

        self.exit = False
        self.screen = pg.Surface((width,height))
        self.init_groups()
        
    

    def init_groups(self):
        '''Initialize all sprite groups'''

        self.all_sprites = pg.sprite.Group()
        


    def draw(self):

        self.screen.fill(1)
        self.all_sprites.update()
        self.all_sprites.draw(self.screen)
        pg.display.flip()

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
        
        self.screen = disp
    

    def init_groups(self):
        '''Initialize all sprite groups'''

        self.all_sprites = pg.sprite.Group()
        self.tiles = pg.sprite.Group()
        self.turrets = pg.sprite.Group()
        self.enemies = pg.sprite.Group()
    
    



        
    

game = Game()
game.loop()