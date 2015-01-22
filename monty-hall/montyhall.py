from random import randint
import sys
from decimal import *
getcontext().prec = 2048


def do_monty():
    """
        Simulates a game of "Let's make a deal" where the player always make the switch.
    """
    # Select randomly where the car is
    car = randint(1, 3)
    # Pick a door randomly
    choice = randint(1, 3)

    # Find the first door where there is a zonk, such that this door
    # is not the one of choice, neither the one with the car (wouldn't be a zonk heh?)
    zonk =  1 if (car != 1 and choice != 1) \
        else 2 if (car != 2 and choice != 3) \
        else 3

    # Switch the selected door to the one which is not the revealed zonk (above)
    # neither the curretly selected one (wouldn't be a switch heh?)
    choice = 1 if (zonk != 1 and choice != 1) \
        else 2 if (zonk != 2 and choice != 3) \
        else 3

    # is the new selection (after the switch) the car?
    return choice == car

def do_sum(n):
    """
        Sums up the results of `n` games of "Let's make a deal",
        and returns the percentage of times the player wins.
    """
    res = Decimal(sum(do_monty() for _ in xrange(n))) / Decimal(n)
    return res


if __name__ == '__main__':
    iterations = 1000
    if len(sys.argv) > 1:
        iterations = int(sys.argv[1])

    percent = do_sum(iterations)
    print 'Winning on switch percentage is: %f' % percent, '%'


