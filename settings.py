
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
mx.set_num_channels(16)

sounds = {
    'CrossbowShoot' : mx.Sound('Sounds/crossbowsound.wav'),
    'SlimeHit' : mx.Sound('Sounds/slimehit.ogg'),
    'SlimeDie' : mx.Sound('Sounds/slimedie.wav'),
    'TripleCrossbowShoot' : mx.Sound('Sounds/triplecrossbowsound.wav'),
    'CannonShoot' : mx.Sound('Sounds/cannonsound.wav'),
    'GameOver' : mx.Sound('Sounds/GameOver.wav'),
    'Click' : mx.Sound('Sounds/click.wav'),
    'Hover' : mx.Sound('Sounds/hover.wav'),
    'WaveStart' : mx.Sound('Sounds/WaveStart.wav')
}
music = {
    'Shop' : 'Sounds/Loop.wav',
    'Wave' : 'Sounds/Loop1.wav',
    'MainMenu' : 'Sounds/MainMenu.wav'
}

TURRETDAMAGES=[3,9,35]
TURRETNAMES=["Crossbow","Triple Crossbow","Cannon"]
CROSSBOWDAMAGE = 3
CANNONDAMAGE = 35
TRIPLECROSSBOWDAMAGE = 9
AMMOBARWIDTH = 50

SLIMEHEALTHS = [15,25,40,15,50,35]
SLIMECOLORS = ["Green","Blue","Pink","Orange","Yellow","Teal"]
SLIMESPEEDS = [10,10,7.5,15,7.5,10]
GREENSLIMEHEALTH = 15
BLUESLIMEHEALTH = 25
PINKSLIMEHEALTH = 40
ORANGESLIMEHEALTH = 15
YELLOWSLIMEHEALTH = 50
TEALSLIMEHEALTH = 35


BGTYPES = ["bg","bushleft","bushright","slimeblue","slimegreen","treeleft","treeright"]



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