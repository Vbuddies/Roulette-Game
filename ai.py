import pdb
import numpy as np
import argparse
from Roulette import Spot, Roulette


def main():
    wins = 0
    iters = 1000000
    for i in range(0, iters):
        print(f'DAY: {i}')
        wins += play(i)
    print('{} days complete')
    print(f'Wins: {wins}')

def play(seed):
    # create roulette
    r = Roulette("American", seed)
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
        # print(f'Run {runs}')
        # print(f'Starting amount: ${amount}')

        # set bets
        bet_count += check_and_bet(r, amount-bet_count, bet_amount, "Dozens", 1)
        bet_count += check_and_bet(r, amount-bet_count, bet_amount, "Dozens", 2)
        bet_count += check_and_bet(r, amount-bet_count, bet_amount, "Columns", 2)

        # call spin
        x = r.spin_and_win()
        # print(f'{x.get_spot().get_numColor()} was hit and you receive {x.get_amount()}')

        # update values
        amount += x.get_amount()
        if x.get_amount() >= 0:
            # print("Reset back to default bet amount")
            bet_amount = default_bet_amount
        else:
            # print("Doubling bet after loss")
            bet_amount = bet_amount * 2
        # print(f'Running Amount: ${amount}\n')
        if bet_count <= 0:
            break

    # print("Running complete")
    # print(f'You started with ${start_amount}')
    print(f'You ended up walking away with ${amount}\n')
    if amount < 25:
        return 0
    else:
        return 1


def continue_play(amount, goal):
    if amount >= goal:
        return False
    elif amount <= 0:
        return False
    else:
        return True
    
def check_and_bet(r, amount, bet_amount, type, options=None):
    if amount < bet_amount:
        # print("Can't place bet, not enough money")
        return 0
    else:
        return r.bet(bet_amount, type, options)

if __name__ == "__main__":
    main()
    # seed 28 results in loss and walk away with $300
    # 996679 results in loss and walk away with $325
    # 996774 results in loss and walk away with $400
    # 996863 results in loss and walk away with $350
    # 996867 results in loss and walk away with $700
    # 996926 results in loss and walk away with $75
    # 996932 results in loss and walk away with $375
    # 996988 results in loss and walk away with $100
    # 997069 results in loss and walk away with $425
    # 997103 results in loss and walk away with $200
    # 997275 results in loss and walk away with $175
    # 997306 resuls in loss and walk away with $25
    # 997362 results in loss and walk away with $1025
    # 997395 results in loss and walk away with $675
    # 997482 results in loss and walk away with $375
    # 997497 results in loss and walk away with $375
    # 997501 results in loss and walk away with $875
    # 997505 results in loss and walk away with $1300
    # 997586 results in loss and walk away with $1300
    # 997589 results in loss and walk away with $925

    # 1,000,000 iterations results in 999,691 wins




    # New Strategy if lost all of bet...double bets
    # if come up even keep bet at what its at
    # if win and double bet reset back to default bet