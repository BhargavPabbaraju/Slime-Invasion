
#Imports
import pygame as pg
import random as rd
import sys
import math
from pygame import mixer as mx
from pygame.math import Vector2 as vec

###SETTING VARIABLES
WIDTH = 960
HEIGHT = 544

TITLE = "Slimes Invasion"

disp = pg.display.set_mode((WIDTH,HEIGHT))
pg.display.set_caption(TITLE)
pg.init()
mx.pre_init(44100,-16,2,512)

sounds = {
    'CrossbowShoot' : mx.Sound('Sounds/crossbowsound.wav'),
    'SlimeHit' : mx.Sound('Sounds/slimehit.ogg')
}

CROSSBOWDAMAGE = 5
CANNONDAMAGE = 35
TRIPLECROSSBOWDAMAGE = 9
AMMOBARWIDTH = 50

GREENSLIMEHEALTH = 15
BLUESLIMEHEALTH = 25
PINKSLIMEHEALTH = 40
ORANGESLIMEHEALTH = 15
YELLOWSLIMEHEALTH = 50
TEALSLIMEHEALTH = 35



ENEMYMULTIPLIER = 5
DELAYMULTIPLIER = 10
INBETWEENDELAY = 1.5

FONT = "FiddlersCoveBold-7JJV.otf"


GAMEOVERTEXTPOSITIONS = [[10*30,1*32],[12*32,6*30],[12*32,8*30],[6*32,14*32],[19*32,14*32+1]]
WAVETEXTPOSITION = [1*32,15*32]
SCORETEXTPOSITION = [14*32,0*32]
NEXTWAVEBUTTONPOSITION = [14*32,15*32-10]


SLIMESCORES = [5,10,20,10,30,25]

###LOADING IMAGES






###LOADING AUDIO





#####COLORS
BLACK = (2,2,2)
WHITE = (252,252,252)
BLUE =(102, 86, 135)
#BLUE2 = (255,255,0)
GRAY = (237, 216, 123)
GOLD = (255,215,0)