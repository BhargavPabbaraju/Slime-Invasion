from settings import *
from text import *
from utility import *



TEXTDUMP = {
    #Page 0 Intro text
    0 : ["Slimes are planning to invade the planet.",       
    "Your task is to kill all the slimes and save humanity."]  ,

    #Page 1 What to do 
    1 : ["->Buy and place turrets on the platforms.",
         "->You can control only one turret at a time.",
         "->Hold Left Click to shoot.",
         "->The turret drains ammo while shooting and",
         "the ammo recovers over time.",
         "->Ammo will recover 4x faster if a turret is inactive",
        
        ] ,

    #Page 3 Controls
    3 : ["CONTROLS",
          "",
         "->Left click on base to place selected turret.",
         "->Left click to shoot.",
         "->Tab to switch to next turret.",
         "->Left click to select specific turret.",
         "->Right click turret to activate skill.",
         "->Spacebar to Pause the game."
    ],

    #Page 2 Wave and Life info
    2 : [
         "->The shop is accessible in between waves.",
          "->Once per wave , you can activate the  skill for each turret ","by right clicking on it.",
         "->A turret skill will last for 10 seconds and will","drain all ammo over the 10 seconds",
         "->If you fail to kill a slime before it escapes , you will lose a life. ",
         "->Every 10 seconds , the slimes switch their lanes."
         
    ],

    #Page 4 Turret info
    4 : ["\t\t\t\t\t\t\tTurret Type\t\t\t\t\tDamage\t\t\t\t\t\t\t\tCost"
    ],

    #Page 5 Slime info
    5 : ["\t\t\t\t\t\t\tSlime Color\t\t\t\t\tHealth\t\t\t\t\t\t\t\tSpeed"
         
    ],


}

