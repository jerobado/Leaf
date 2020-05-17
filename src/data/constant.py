# Put all literal constants here

__version__ = '0.1.7'

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

        self.seeds = {'tomato seed': 202,
                      'lettuce seed': 280,
                      'watermelon seed': 306,
                      '__test_seed__': 3}
        self.duration = 0
        self._generate_information(seed)

    def _generate_information(self, seed):

        self.duration = self.seeds.get(seed, None)
