# Put all literal constants here

__version__ = '0.1.8'

WELCOME_MESSAGE = f"""Leaf
Simple text-based farming game for the bored developer.
-------------------------------------------------------

Version: {__version__}

Type \'help\' for the list of valid commands."""

HELP = """Play Leaf using these valid commands:\n
Player commands:
    till           - till the current spot/location to plant seed
    plant [seed]   - plant a particular seed
    check          - view growth progress of seed(s) planted
    harvest        - harvest fully grown crop

Inventory commands:
    inventory      - display current items in your inventory
    add [item]     - add valid item to inventory
    remove [item]  - remove valid item from inventory 

Game commands:
    help           - show this help information
    quit           - exit the game"""

QUIT_MESSAGE = 'Leaf closing. See you soon!'


class SeedCatalog:

    def __init__(self, seed):

        self.seeds = {'grape seed':             60 * 8 + 5,
                      'melon seed':             60 * 4 + 46,
                      'watermelon seed':        60 * 4 + 36,
                      'tangerine seed':         60 * 5 + 11,
                      'lemon seed':             60 * 6 + 47,
                      'banana seed':            60 * 8 + 46,
                      'pineapple seed':         60 * 5 + 6,
                      'mango seed':             60 * 10 + 25,
                      'red apple seed':         60 * 8 + 24,
                      'green apple seed':       60 * 6 + 5,
                      'pear seed':              60 * 5 + 2,
                      'peach seed':             60 * 3 + 35,
                      'cherries seed':          60 * 7 + 29,
                      'strawberry seed':        60 * 7 + 37,
                      'kiwi seed':              60 * 4 + 28,
                      'tomato seed':            60 * 3 + 51,
                      'coconut seed':           60 * 10 + 22,
                      'avocado seed':           60 * 10 + 9,
                      'eggplant seed':          60 * 4 + 9,
                      'potato seed':            60 * 4 + 22,
                      'carrot seed':            60 * 4,
                      'corn seed':              60 * 4 + 50,
                      'hot pepper seed':        60 * 4 + 49,
                      'cucumber seed':          60 * 3 + 21,
                      'bok choy seed':          60 * 4 + 1,
                      'broccoli seed':          60 * 3 + 36,
                      'garlic seed':            60 * 3 + 36,
                      'onion seed':             60 * 5 + 21,
                      'mushroom seed':          60 * 4 + 31,
                      'peanut seed':            60 * 4 + 25,
                      'chestnut seed':          60 * 5 + 4,
                      '__test_seed__':          3}
        self.duration = 0
        self._generate_information(seed)

    def _generate_information(self, seed):

        self.duration = self.seeds.get(seed, None)
