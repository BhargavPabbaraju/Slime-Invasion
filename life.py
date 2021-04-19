from settings import *

class Life:
    def __init__(self,game):
        self.health = 3
        self.lives = pg.sprite.Group()
        self.game = game
        for x in range(self.health):
            self.lives.add(pg.sprite.Sprite())
            self.lives.sprites()[x].image = pg.image.load('Images/heart.png')
            self.lives.sprites()[x].image = pg.transform.scale(self.lives.sprites()[x].image,(32,32))
            self.lives.sprites()[x].rect = self.lives.sprites()[x].image.get_rect()
            self.lives.sprites()[x].rect.x = 35*x
            self.game.all_sprites.add(self.lives.sprites()[x])
        
        

    def deduct(self):
        self.health -= 1
        self.lives.sprites()[-1].kill()

    def update(self):
        if self.health <= 0:
            self.game.gameover()
            