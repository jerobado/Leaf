# Put all literal constants here

__version__ = '0.1.3'

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

Game commands:
    help           - show this help information
    quit           - exit the game"""