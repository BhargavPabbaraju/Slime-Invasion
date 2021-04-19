from settings import *

class Text(pg.sprite.Sprite):

    def __init__(self,x,y,msg,game,size,ind=0,color=BLACK):
        super().__init__()
        self.ind = ind 
        self.game = game
        self.msg = msg
        self.pos = x,y
        self.size = size
        self.color = color
        self.active = False
        

        self.update()

        self.rect = self.image.get_rect()
        self.rect.topleft = self.pos
    

    def update(self):
        self.font = pg.font.Font(FONT,self.size)
        self.image = self.font.render(self.msg,True,self.color)