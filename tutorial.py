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
         "->The turret looses its ammo while shooting and",
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
         "->Right click turret to activate skill.(When its ammo is full)",
         "->Spacebar to Pause the game."
    ],

    #Page 2 Wave and Life info
    2 : ["->Click on start next wave button to start the next wave.",
         "->The shop is accessible in between waves.",
          "->Once per wave , you can activate the  skill for each turret ","by right clicking on it when its ammo is full.",
         "->A turret skill will last for 10 seconds and will","drain all ammo over the 10 seconds",
         "->Kill all slimes in the wave to clear it.",
         "->If you fail to kill a slime before it escapes , you will lose a life. ",
         "->When you run out of all three lives, the game is over."
    ],

    #Page 4 Turret info
    4 : ["Turret Type\t Damage\t Cost"
    ],

    #Page 5 Slime info
    5 : ["Slime Type\t Health\t Speed"
         
    ],


}

