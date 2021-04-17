

class EnemyPath:
    def __init__(self,enemy,mapid):
        self.enemy = enemy
        self.mapid = mapid


    def find_dir_map1_lane_0(self):
        

        if self.x>=370 and self.y<=362:
            return "u"
        elif self.x>=364 and self.y<=47:
            return "r"
        else:
            return "r"

    def find_dir_map1_lane_1(self):
        
        if self.x>=563 and self.y<=209 or (self.x>=880 and self.y<=47):
            return "r"
        
        elif self.x>=880 and self.y<=209:
            return "u"
        else:
            return "u"




    
    def find_next_dir(self):
        self.x,self.y = self.enemy.rect.topleft

        if self.mapid == 1:
            if self.enemy.lane==0:
                return self.find_dir_map1_lane_0()

            else:
                return self.find_dir_map1_lane_1()



