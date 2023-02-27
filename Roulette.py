import math
import numpy as np
import random
import pdb




class Roulette:
    # list of lists
        # inner list is the number followed by color
        # 'number', [0 = red, 1 = black, 2 = green]
    wheel = np.array([
            ('00', 2), ('27', 0), ('10', 1), ('25', 0), ('29', 1), ('12', 0), 
            ('8', 1), ('19', 0), ('31', 1), ('18', 0), ('6', 1), ('21', 0), ('33', 1), 
            ('16', 0), ('4',1 ), ('23', 0), ('35', 1), ('14', 0), ('2', 1), ('0', 2),
            ('28', 1), ('9', 0), ('26', 1), ('30', 0), ('11', 1), ('7', 0), ('20', 1),
            ('32', 0), ('17',1 ), ('5', 0), ('22', 1), ('34', 0), ('15', 1), ('3', 0),
            ('24', 1), ('36', 0), ('13', 1), ('1', 0)
        ])
    
    def __init__(self, seed=0):
        self.seed = seed
        


    def spin(self):
        num = self._get_spin_number()
        return num

    def bet(self):
        pass

    def _determine_winnings(self):
        pass

    def _get_spin_number(self):
        return np.random.choice(self.wheel)


r = Roulette()
print(r.spin())