# Classes of game mechanics

import sys
import time
import threading
from collections import (Counter,
                         deque)
from src.data.constant import (HELP,
                               WELCOME_MESSAGE,
                               SeedCatalog)


class GameMechanics:

    def __init__(self):

        self.GAME_COMMANDS = {'help': self.help,
                              'quit': self.quit}
        self.inventoryMechanics = InventoryMechanics()
        self.playerMechanics = PlayerMechanics()
        self.playerMechanics.playerInventoryMechanics = self.inventoryMechanics
        self.rCommand = None            # user's raw command(s)
        self.command = None
        self.argument = None
        self.task = None                # function to execute
        self.isMultiple = bool          # multiple commands or single

        self._combine_commands()

    def help(self):

        print(HELP)

    def quit(self):

        print('Leaf closing. See you soon!')
        sys.exit()

    def start_game(self):

        self.welcome_message()
        while True:
            self.get_commands()
            self.parse_commands()
            self.get_command_action()
            self.process_commands()

    def welcome_message(self):

        print(WELCOME_MESSAGE)

    def get_commands(self):

        self.rCommand = str(input('\nLEAF > ')).split(maxsplit=1)

    def parse_commands(self):

        command_count = len(self.rCommand)
        if command_count == 1:
            self.command = self.rCommand[0]
            self.isMultiple = False
        elif command_count > 1:
            print(f'{self.rCommand=}')
            self.command, self.argument = self.rCommand
            self.isMultiple = True
        else:
            self.command = None
            self.isMultiple = None

    def get_command_action(self):
        """ Get the corresponding class function for the player's input command. If the user hits the 'inventory'
        command, this will map to InventoryMechanics.inventory() class function """

        self.task = self.GAME_COMMANDS.get(self.command,
                                           self._unrecognized_command)

    def process_commands(self):

        if self.isMultiple:
            self.task(self.argument)
        else:
            # [] TODO: test if the user add an extra argument which should not be
            self.task()

    def _combine_commands(self):

        self.GAME_COMMANDS.update(self.playerMechanics.PLAYER_COMMANDS)
        self.GAME_COMMANDS.update(self.inventoryMechanics.INVENTORY_COMMANDS)

    # GameMechanics command errors
    # [] TODO: create custom error types, i.e. GameCommandError, PlayerCommandError, etc.
    def _unrecognized_command(self):

        print(f'\'{self.command}\' is not a valid command.\nSee \'help\' command.')

    def _incomplete_command(self):

        print(f'{self.command} needs a value to work.')


class PlayerMechanics:

    def __init__(self):

        self.PLAYER_COMMANDS = {'till': self.till,
                                'plant': self.plant,
                                'check': self.check,
                                'harvest': self.harvest}

        self.playerInventoryMechanics = None
        self.plantGrowthMechanics = None
        self.growing_plants = deque()        # list of active and non-active threads

    def till(self):

        # [] TODO: add a mechanics that will prevent other commands from executing if this is not executed first
        print('tilling the soil...')
        time.sleep(5)
        print('soil tilled!')

    # [] TODO: filter only seed type as valid argument, currently you can plant anything!
    def plant(self, seed=None):

        if seed:
            if seed in self.playerInventoryMechanics.inventoryDeque:
                # Get seed information from Seed Catalog
                seed_details = SeedCatalog(seed)

                # Update player inventory
                self.playerInventoryMechanics.remove_item(seed)

                # Simulate planting
                print(f'planting {seed}...')
                time.sleep(3)

                # Start growing plant
                self.plantGrowthMechanics = GrowthMechanics(seed, duration=seed_details.duration)
                self.growing_plants.append(self.plantGrowthMechanics)
                self.plantGrowthMechanics.start()
                print(f'{seed} planted!')
            else:
                print(f'You don\'t have a \'{seed}\' in your inventory.')
        else:
            print('Incomplete command, should be plant [seed], i.e. plant tomato')

    def check(self):

        # [] TODO: display growth percentage of planted crop
        for index, plant in enumerate(self.growing_plants):
            print(index, plant.name, plant.is_alive())

    def harvest(self):

        # [] TODO: display harvestable (100% growth) crops
        # [] TODO: you can only harvest thread that completed its task
        if self.growing_plants:
            print(f'Harvesting \'{self.growing_plants.popleft().name}\'...')
            time.sleep(4)
            print('Done!')


class InventoryMechanics:

    def __init__(self):

        self.INVENTORY_COMMANDS = {'inventory': self.inventory,
                                   'add_item': self.add_item}
        self.inventoryDeque = deque()
        self.inventoryCounter = Counter(self.inventoryDeque)

    def inventory(self):

        print(f'{"ITEM":<16}{"QUANTITY":<16}')
        for item in set(self.inventoryDeque):
            print(f'{item:<16}{self.inventoryCounter[item]:<16}')

    # [] TODO: you can literally add anything! Limit this!
    def add_item(self, item):

        self.inventoryDeque.append(item)

        # update inventoryCounter
        self.inventoryCounter = Counter(self.inventoryDeque)

        print(f'\'{item}\' added to inventory')

    def remove_item(self, item):

        self.inventoryDeque.remove(item)

        # Update inventoryCounter
        self.inventoryCounter = Counter(self.inventoryDeque)


class GrowthMechanics(threading.Thread):

    def __init__(self, seed, duration):

        super().__init__()
        self.name = seed
        self.duration = duration

    def run(self):

        time.sleep(self.duration)
