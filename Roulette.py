import math
import numpy as np
import random
import pdb

class Spot:
    def __init__(self, number, color):
        self.number = number
        self.color = color

    def get_num(self):
        return self.number
    
    def get_color(self):
        return self.color
    
    def get_numColor(self):
        return str(self.number) + ' ' + str(self.color)

class Roulette:
    red = [1, 3, 5, 7, 9, 12, 14, 16, 18, 19, 21, 23, 25, 27, 30, 32, 34, 36]
    black = [2, 4, 6, 8, 10, 11, 13, 15, 17, 20, 22, 24, 26, 28, 29, 31, 33, 35]
    
    def __init__(self, seed=0):
        self.seed = seed
        np.random.seed(seed)
        self.setup_wheel()

    def setup_wheel(self):
        temp = []
        nums = ['00', '27', '10', '25', '29', '12', '8', '19', '31', '18', '6', '21', '33', '16', '4', '23', '35', '14', '2', '0', '28', '9', '26', '30', '11', '7', '20', '32', '17', '5', '22', '34', '15', '3', '24', '36', '13', '1']
        colors = [2, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 2, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0]
        for i in range(len(nums)):
            temp.append(Spot(nums[i], colors[i]))
        self.wheel = temp

    def spin(self):
        num = self._get_spin_number()
        return num

    def bet(self):
        pass

    def _determine_winnings(self):
        pass

    def _get_spin_number(self):
        return np.random.choice(self.wheel)
    
    def _color_to_string(self, num):
        colors = ['red', 'black', 'green']
        return colors[num]


r = Roulette()
print(r.spin().get_numColor())