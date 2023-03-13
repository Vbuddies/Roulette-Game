import pdb
import numpy as np
import argparse
from Roulette import Spot, Roulette



def main():
    # create roulette
    r = Roulette()
    start_amount = 5000
    amount = start_amount
    goal = amount * 2
    default_bet_amount = 25
    bet_amount = default_bet_amount
    runs = 0

    # play loop
    while continue_play(amount, goal):
        runs += 1
        bet_count = 0
        print(f'Run {runs}')
        print(f'Starting amount: ${amount}')

        # set bets
        bet_count += check_and_bet(r, amount-bet_count, bet_amount, "Dozens", 1)
        bet_count += check_and_bet(r, amount-bet_count, bet_amount, "Dozens", 2)
        bet_count += check_and_bet(r, amount-bet_count, bet_amount, "Columns", 2)

        # call spin
        x = r.spin_and_win()
        print(f'{x.get_spot().get_numColor()} was hit and you receive {x.get_amount()}')

        # update values
        amount += x.get_amount()
        if x.get_amount() >= 0:
            print("Reset back to default bet amount")
            bet_amount = default_bet_amount
        else:
            print("Doubling bet after loss")
            bet_amount = bet_amount * 2
        print(f'Running Amount: ${amount}\n')
        if bet_count <= 0:
            break

    print("Running complete")
    print(f'You started with ${start_amount}')
    print(f'You ended up walking away with ${amount}')


def continue_play(amount, goal):
    if amount == goal:
        return False
    elif amount <= 0:
        return False
    else:
        return True
    
def check_and_bet(r, amount, bet_amount, type, options=None):
    if amount < bet_amount:
        print("Can't place bet, not enough money")
        return 0
    else:
        return r.bet(bet_amount, type, options)

if __name__ == "__main__":
    main()