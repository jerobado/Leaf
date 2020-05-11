import sys

from threading import Timer

from src.legacy.leaf.player import Player


if __name__ == '__main__':
    p1 = Player()
    while True:
        response = input("{0}: ".format(p1.getPlayersName()))
        if 'plant' in response:
            for pick in p1.seeds:
                if pick in response:
                    p1.setSeedToPlant(pick)
                    p1.plant()
                    t = Timer(5, p1.planting)
                    t.start()
        elif 'quit' in response:
            sys.exit(0)
        else:
            pass