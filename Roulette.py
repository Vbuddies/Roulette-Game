import math
import numpy as np
import random




class Roulette:
    def __init__(self, seed=0):
        self.seed = seed
        # list of lists
        # inner list is the number followed by color
        # 'number', [0 = red, 1 = black, 2 = green]
        self.wheel = np.array([
            ['00', 2], ['27', 0], ['10', 1], ['25', 0], ['29', 1], ['12', 0], 
            ['8', 1], ['19', 0], ['31', 1], ['18', 0], ['6', 1], ['21', 0], ['33', 1], 
            ['16', 0], ['4',1 ], ['23', 0], ['35', 1], ['14', 0], ['2', 1], ['0', 2],
            ['28', 1], ['9', 0], ['26', 1], ['30', 0], ['11', 1], ['7', 0], ['20', 1]
            ['32', 0], ['17',1 ], ['5', 0], ['22', 1], ['34', 0], ['15', 1], ['3', 0]
            ['24', 1], ['36', 0], ['13', 1], ['1', 0]
        ])


    def spin():
        pass

    def bet():
        pass

    def _determine_winnings():
        pass

    def _get_spin_number():
        pass


r = Roulette()