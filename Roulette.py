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
    
    def get_color_string(self):
        colors = ['red', 'black', 'green']
        return colors[self.color]
    
    def get_numColor(self):
        return str(self.number) + ' ' + str(self.color)

class Bet:
    # Bet Types: 
        # Name - Payout - Odds(Optional)
        # 1:1 pays your bet
        # 2:1 doubles your bet

        # Outside Bets (bets made on the perimeter)
            # Red/Black
                # Red - 1:1 - <0.5          betting on red numbers
                # Black - 1:1 - <0.5        betting on black number
            # Odd/Even
                # Odd - 1:1 - <0.5          betting on odd numbers 1-35
                # Even - 1:1 - <0.5         betting on even numbers 2-36
            # Low/High 
                # Low -  - 1:1              betting on numbers 1-18
                # High -  - 1:1             betting on numbers 19-36
            # Columns
                # Column1 - 2:1             betting on numbers [1, 4, 7, 10, 13, 16, 19, 22, 25, 28, 31, 34]
                # Column2 - 2:1             betting on numbers [2, 5, 8, 11, 14, 17, 20, 23, 26, 29, 32, 35]
                # Column3 - 2:1             betting on numbers [3, 6, 9, 12, 15, 18, 21, 24, 27, 30, 33, 36]
            # Dozens
                # 1st 12 - 2:1              betting on numbers 1-12
                # 2nd 12 - 2:1              betting on numbers 13-24
                # 3rd 12 - 2:1              betting on numbers 25-36

        # Inside Bets (bets made inside the rectangle)
            # Straight Up - 35:1            betting on any one number
            # Split - 17:1                  betting on any two numbers that are adjacent
            # Street - 11:1                 betting on any row of numbers
            # Corner - 8:1                  betting on four numbers that all share a common corner
            # Line - 5:1                    covering two rows that are adjacent
            # Top-Line - 6:1 - 13.16%       betting on 0,00,1,2,3 also called 5-number
            # Basket - 6:1                  betting on 0,1,2,3 also called first four
            # Snake Bet - 2:1               betting on 1,5,9,12,14,16,19,23,27,30,32,34


    def __init__(self, amount, bet_type, options=None):
        self.amount = 0
        self.options = None

        # check and set bet type
        self.bet_type = self.set_type(bet_type, options)
        assert(self.bet_type != None)

        # place bet
        self.up_Bet(amount)

    def get_Amount(self):
        return self.amount
    
    def _set_Amount(self, amount):
        self.amount = amount

    def up_Bet(self, amount):
        x = self.get_Amount() + amount
        if x > 0:
            self._set_Amount(x)
        else:
            print("Bet cannot be less than 0")

    def down_Bet(self, amount):
        x = self.get_Amount() - amount
        if x > 0:
            self._set_Amount(x)
        else:
            print("Bet cannot be less than 0")

    def get_type(self):
        return self.bet_type, self.options

    def set_type(self, bet_type, options):
        # must check that type is set properly
        bet_type_list = ["Color", "EvenOdd", "LowHigh", "Columns", "Dozens", "Straight", "Split", "Street", "Corner", "Line", "Basket", "Snake-Bet", "Penta"]
        if (bet_type in bet_type_list):
            match bet_type:
                case "Color":
                    assert(isinstance(options, str))
                    assert(options == "Red" or options == "Black")
                    self.options = options
                    return "Color"
                case "EvenOdd":
                    assert(isinstance(options, str))
                    assert(options == "Even" or options == "Odd")
                    self.options = options
                    return "EvenOdd"
                case "LowHigh":
                    assert(isinstance(options, str))
                    assert(options == "Low" or options == "High")
                    self.options = options
                    return "LowHigh"
                case "Columns":
                    assert(isinstance(options, int))
                    assert(1<=options<=3)
                    self.options = options
                    return "Columns"
                case "Dozens":
                    assert(isinstance(options, int))
                    assert(1<=options<=3)
                    self.options = options
                    return "Dozens"
                case "Straight":
                    assert(isinstance(options, int))
                    # assert proper number, -1 is 00
                    assert(-1<=options<=36)
                    self.options = options
                    return "Straight"
                case "Split":
                    assert(isinstance(options, list))
                    assert(len(options) == 2)
                    # make sure its a valid split, i.e. the numbers are next to each other
                    # HERE
                    self.options = options
                    return "Split"
                case "Street":
                    assert(isinstance(options, int))
                    assert(1<=options<=12)
                    self.options=options
                    return "Street"
                case "Corner":
                    return "Corner"
                case "Line":
                    return "Line"
                case "Basket":
                    # options don't matter in this case
                    # betting on 0,1,2,3
                    return "Basket"
                case _:
                    print("Error: This bet type is not implemented yet.")
                    # throw error
                    return None
        else:
            return None

class Roulette:
    red = [1, 3, 5, 7, 9, 12, 14, 16, 18, 19, 21, 23, 25, 27, 30, 32, 34, 36]
    black = [2, 4, 6, 8, 10, 11, 13, 15, 17, 20, 22, 24, 26, 28, 29, 31, 33, 35]
    
    def __init__(self, seed=0):
        self.seed = seed
        np.random.seed(seed)
        self.setup_wheel()
        # defaults
        lastSpot = None
        self.bets = []

    def setup_wheel(self):
        temp = []
        nums = ['00', '27', '10', '25', '29', '12', '8', '19', '31', '18', '6', '21', '33', '16', '4', '23', '35', '14', '2', '0', '28', '9', '26', '30', '11', '7', '20', '32', '17', '5', '22', '34', '15', '3', '24', '36', '13', '1']
        colors = [2, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 2, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0]
        for i in range(len(nums)):
            temp.append(Spot(nums[i], colors[i]))
        self.wheel = temp

    def spin(self):
        spot = self._get_spin_number()
        self.lastSpot = spot
        return spot

    def bet(self):
        pass

    def _determine_winnings(self):
        pass

    def _get_spin_number(self):
        return np.random.choice(self.wheel)


r = Roulette()
# for i in range(3000):
#     x = r.spin()
#     print(f'Spin {i+1}: {str(x.get_color_string())} {x.get_num()}')

# program will stop as it should when given bad bet
b = Bet(100, "c")