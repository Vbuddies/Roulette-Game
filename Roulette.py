import math
import numpy as np
import random
import pdb

class Spot:
    def __init__(self, number, color):
        self.number = number
        self.color = color

    def __str__(self):
        details = 'Spot\n'
        details += self.get_numColor() + '\n'
        return details

    def get_num(self):
        return self.number
    
    def get_color(self):
        return self.color
    
    def get_color_string(self):
        colors = ['red', 'black', 'green']
        return colors[self.color]
    
    def get_numColor(self):
        return str(self.number) + ' ' + str(self.get_color_string())

class Roulette:
    # American Roulette
    
    def __init__(self, style= "American",  seed=0):
        self.style = style
        self.seed = seed
        np.random.seed(seed)
        self.setup_wheel()
        self.setup_board(style)
        # defaults
        lastSpot = None
        self.bets = []

    def __str__(self):
        details = 'Roulette\n'
        details += f'Style: {self.style}\n'
        return details

    def setup_wheel(self):
        temp = []
        nums = [-1, 27, 10, 25, 29, 12, 8, 19, 31, 18, 6, 21, 33, 16, 4, 23, 35, 14, 2, 0, 28, 9, 26, 30, 11, 7, 20, 32, 17, 5, 22, 34, 15, 3, 24, 36, 13, 1]
        colors = [2, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 2, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0]
        for i in range(len(nums)):
            temp.append(Spot(nums[i], colors[i]))
        self.wheel = temp
        if self.style == "European":
            # remove double zero
            self.wheel = self.wheel[1:]

    def setup_board(self, style):
        self.red = [1, 3, 5, 7, 9, 12, 14, 16, 18, 19, 21, 23, 25, 27, 30, 32, 34, 36]
        self.black = [2, 4, 6, 8, 10, 11, 13, 15, 17, 20, 22, 24, 26, 28, 29, 31, 33, 35]
    
        if style == "American":
            self.board = [
                [0, -1],
                [1, 2, 3],
                [4, 5, 6],
                [7, 8, 9],
                [10, 11, 12],
                [13, 14, 15],
                [16, 17, 18],
                [19, 20, 21],
                [22, 23, 24],
                [25, 26, 27],
                [28, 29, 30],
                [31, 32, 33],
                [34, 35, 36]
            ]
        else:
            # European
            self.board = [
                [0],
                [1, 2, 3],
                [4, 5, 6],
                [7, 8, 9],
                [10, 11, 12],
                [13, 14, 15],
                [16, 17, 18],
                [19, 20, 21],
                [22, 23, 24],
                [25, 26, 27],
                [28, 29, 30],
                [31, 32, 33],
                [34, 35, 36]
            ]

    def spin(self):
        spot = self._get_spin_number()
        self.lastSpot = spot
        self.lastSpotNum = spot.get_num()
        return spot
    
    def spin_and_win(self):
        spot = self._get_spin_number()
        self.lastSpot = spot
        self.lastSpotNum = spot.get_num()
        winnings = self._determine_winnings()
        return winnings

    def bet(self, amount, bet_type, options=None):
        # check if amount fits table 

        # place bet
        try:
            b = self.Bet(self, amount, bet_type, options)
            self.bets.append(b)
            # print(f'You bet ${amount} on {bet_type} with {options} option')
            return amount
        except:
            # print("Bet Failure")
            return 0

    def _determine_winnings(self):
        # calculate winnings
        total_win = 0
        for i in self.bets:
            total_win += i.payout(self.lastSpotNum)
        # set bets to empty
        self.bets = []

        # create winning object and return
        return self.Winning(self.lastSpot, total_win)

    def _get_spin_number(self):
        return np.random.choice(self.wheel)

    class Bet:
        parent = None
        payout_rate = 1
        payout_numbers = []
        # region Bet Types: 
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
        # endregion

        def __init__(self, parent, amount, bet_type, options=None):
            self.parent = parent
            self.amount = 0
            self.options = None

            # check and set bet type
            self.bet_type = self.set_type(bet_type, options)
            assert(self.bet_type != None)

            # place bet
            self.up_Bet(amount)
        
        def __str__(self):
            details = 'Bet\n'
            details += 'Type:   {self.bet_type}\n'
            details += 'Amount: {self.amount}\n'
            return details

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

        def set_type(self, bet_type, options=None):
            # must check that type is set properly
            bet_type_list = ["Color", "EvenOdd", "LowHigh", "Columns", "Dozens", "Straight", "Split", "Street", "Corner", "Line", "TopLine", "Basket", "Snake-Bet", "Penta"]
            if (bet_type in bet_type_list):
                match bet_type:
                    case "Color":
                        assert(isinstance(options, str))
                        assert(options == "Red" or options == "Black")
                        self.options = options
                        self.payout_rate = 1
                        if options == "Red":
                            self.payout_numbers = [1, 3, 5, 7, 9, 12, 14, 16, 18, 19, 21, 23, 25, 27, 30, 32, 34, 36]
                        else:
                            self.payout_numbers = [2, 4, 6, 8, 10, 11, 13, 15, 17, 20, 22, 24, 26, 28, 29, 31, 33, 35]
                        return "Color"
                    case "EvenOdd":
                        assert(isinstance(options, str))
                        assert(options == "Even" or options == "Odd")
                        self.options = options
                        self.payout_rate = 1
                        if options == "Even":
                            self.payout_numbers = [2, 4, 6, 8, 10, 12, 14, 16, 18, 20, 22, 24, 26, 28, 30, 32, 34, 36]
                        else:
                            self.payout_numbers = [1, 3, 5, 7, 9, 11, 13, 15, 17, 19, 21, 23, 25, 27, 29, 31, 33, 35]
                        return "EvenOdd"
                    case "LowHigh":
                        assert(isinstance(options, str))
                        assert(options == "Low" or options == "High")
                        self.options = options
                        self.payout_rate = 1
                        if options == "Low":
                            self.payout_numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18]
                        else:
                            self.payout_numbers = [19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36]
                        return "LowHigh"
                    case "Columns":
                        assert(isinstance(options, int))
                        assert(1<=options<=3)
                        self.options = options
                        self.payout_rate = 2
                        if options == 1:
                            self.payout_numbers = [1, 4, 7, 10, 13, 16, 19, 22, 25, 28, 31, 34]
                        elif options == 2:
                            self.payout_numbers = [2, 5, 8, 11, 14, 17, 20, 23, 26, 29, 32, 35]
                        else:
                            self.payout_numbers = [3, 6, 9, 12, 15, 18, 21, 24, 27, 30, 33, 36]
                        return "Columns"
                    case "Dozens":
                        assert(isinstance(options, int))
                        assert(1<=options<=3)
                        self.options = options
                        self.payout_rate = 2
                        if options == 1:
                            self.payout_numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
                        elif options == 2:
                            self.payout_numbers = [13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24]
                        else:
                            self.payout_numbers = [25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36]
                        return "Dozens"
                    case "Straight":
                        assert(isinstance(options, int))
                        # assert proper number, -1 is 00
                        assert(-1<=options<=36)
                        self.options = options
                        self.payout_rate = 35
                        self.payout_numbers = [options]
                        return "Straight"
                    case "Split":
                        assert(isinstance(options, list))
                        assert(len(options) == 2)
                        assert(-1 not in options and 0 not in options)
                        # make sure its a valid split, i.e. the numbers are next to each other
                        np.sort(options)
                        diff = math.abs(options[1] - options[0])
                        assert(diff == 1 or diff == 3)
                        self.options = options
                        self.payout_rate = 17
                        self.payout_numbers = options
                        return "Split"
                    case "Street":
                        assert(isinstance(options, int))
                        assert(1<=options<=12)
                        self.options=options
                        self.payout_rate = 11
                        if options == 1:
                            self.payout_numbers = [1, 2, 3]
                        elif options == 2:
                            self.payout_numbers = [4, 5, 6]
                        elif options == 3:
                            self.payout_numbers = [7, 8, 9]
                        elif options == 4:
                            self.payout_numbers = [10, 11, 12]
                        elif options == 5:
                            self.payout_numbers = [13, 14, 15]
                        elif options == 6:
                            self.payout_numbers = [16, 17, 18]
                        elif options == 7:
                            self.payout_numbers = [19, 20, 21]
                        elif options == 8:
                            self.payout_numbers = [22, 23, 24]
                        elif options == 9:
                            self.payout_numbers = [25, 26, 27]
                        elif options == 10:
                            self.payout_numbers = [28, 29, 30]
                        elif options == 11:
                            self.payout_numbers = [31, 32, 33]
                        else:
                            self.payout_numbers = [34, 35, 36]
                        return "Street"
                    case "Corner":
                        assert(isinstance(options, list))
                        assert(len(options) == 2)
                        assert(-1 not in options and 0 not in options)
                        # make sure its a valid corner, i.e. all numbers touch common point
                        np.sort(options)
                        if options == [1, 2, 4, 5]:
                            pass
                        elif options == [2, 3, 5, 6]:
                            pass
                        elif options == [4, 5, 7, 8]:
                            pass
                        elif options == [5, 6, 8, 9]:
                            pass
                        elif options == [7, 8, 10, 11]:
                            pass
                        elif options == [8, 9, 11, 12]:
                            pass
                        elif options == [10, 11, 13, 14]:
                            pass
                        elif options == [11, 12, 14, 15]:
                            pass
                        elif options == [13, 14, 16, 17]:
                            pass
                        elif options == [14, 15, 17, 18]:
                            pass
                        elif options == [16, 17, 19, 20]:
                            pass
                        elif options == [17, 18, 20, 21]:
                            pass
                        elif options == [19, 20, 22, 23]:
                            pass
                        elif options == [20, 21, 23, 24]:
                            pass
                        elif options == [22, 23, 25, 26]:
                            pass
                        elif options == [23, 24, 26, 27]:
                            pass
                        elif options == [25, 26, 28, 29]:
                            pass
                        elif options == [26, 27, 29, 30]:
                            pass
                        elif options == [28, 29, 31, 32]:
                            pass
                        elif options == [29, 30, 32, 33]:
                            pass
                        elif options == [31, 32, 34, 35]:
                            pass
                        elif options == [32, 33, 35, 36]:
                            pass
                        else:
                            print("bad values")
                            assert(False)
                        self.options = options
                        self.payout_rate = 8
                        self.payout_numbers = options
                        return "Corner"
                    case "Line":
                        assert(isinstance(options, int))
                        assert(1<=options<=11)
                        self.options=options
                        self.payout_rate = 5
                        if options == 1:
                            self.payout_numbers = [1, 2, 3, 4, 5, 6]
                        elif options == 2:
                            self.payout_numbers = [4, 5, 6, 7, 8, 9]
                        elif options == 3:
                            self.payout_numbers = [7, 8, 9, 10, 11, 12]
                        elif options == 4:
                            self.payout_numbers = [10, 11, 12, 13, 14, 15]
                        elif options == 5:
                            self.payout_numbers = [13, 14, 15, 16, 17, 18]
                        elif options == 6:
                            self.payout_numbers = [16, 17, 18, 19, 20, 21]
                        elif options == 7:
                            self.payout_numbers = [19, 20, 21, 22, 23, 24]
                        elif options == 8:
                            self.payout_numbers = [22, 23, 24, 25, 26, 27]
                        elif options == 9:
                            self.payout_numbers = [25, 26, 27, 28, 29, 30]
                        elif options == 10:
                            self.payout_numbers = [28, 29, 30, 31, 32, 33]
                        else:
                            self.payout_numbers = [31, 32, 33, 34, 35, 36]
                        return "Line"
                    case "TopLine":
                        # only available in American Roulette
                        self.options = options
                        self.payout_rate = 6
                        self.payout_numbers = [-1, 0, 1, 2, 3]
                        return "TopLine"
                    case "Basket":
                        # only available in European, not American
                        # options don't matter in this case
                        # betting on 0,1,2,3
                        self.options = options
                        self.payout_rate = 6
                        self.payout_numbers = [0, 1, 2, 3]
                        return "Basket"
                    case _:
                        print("Error: This bet type is not implemented yet.")
                        # throw error
                        return None
            else:
                return None

        def is_winner(self, num):
            return num in self.payout_numbers
        
        def payout(self, num):
            if self.is_winner(num):
                # win bet
                return ((self.payout_rate + 1) * self.get_Amount())
            else:
                # lose bet
                return (-1 * self.get_Amount())

    class Winning:
        def __init__(self, spot, amount=0):
            self.spot = spot
            self.amount = amount

        def __str__(self):
            details = 'Winning\n'
            details += f'Spot:      {self.spot}\n'
            details += f'Amount:    {self.amount}\n'
            return details
        
        def get_spot(self):
            return self.spot
        
        def get_amount(self):
            return self.amount
        
        def up_amount(self, am):
            self._set_amount(self.get_amount() + am)
        
        def _set_amount(self, am):
            self.amount = am


if __name__ == "__main__":
    # for testing
    r = Roulette()

    r.bet(25, "Dozens", 1)
    r.bet(25, "Dozens", 2)
    r.bet(25, "Columns", 2)

    pdb.set_trace()