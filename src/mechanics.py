# Classes of game mechanics

import inspect
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
        self.task = None                    # function to execute
        self.isMultiple = bool              # multiple commands or single
        self.isCommandMismatch = bool       # command and argument mismatch

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
            self.check_commands()       # add something to validate user commands before parsing
            self.get_command_action()
            self.process_commands()
            self.reset_commands()       # clear values of command and argument

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
            self.command, self.argument = self.rCommand
            self.isMultiple = True
        else:
            self.command = None
            self.isMultiple = None

    def check_commands(self):

        if self.command:
            self.isCommandMismatch = self._check_command_combination()

    def get_command_action(self):
        """ Get the corresponding class function for the player's input command. If the user hits the 'inventory'
        command, this will map to InventoryMechanics.inventory() class function """

        # [] TODO: 'jflkd' does not need to have an argument 'ejwk', random command become valid
        self.task = self.GAME_COMMANDS.get(self.command,
                                           self._command_error)

    def process_commands(self):

        if self.isMultiple:
            if not self.isCommandMismatch:
                self.task(self.argument)
            else:
                self._incorrect_command()
        else:
            self.task()

    def reset_commands(self):

        self.argument = None

    def _combine_commands(self):

        self.GAME_COMMANDS.update(self.playerMechanics.PLAYER_COMMANDS)
        self.GAME_COMMANDS.update(self.inventoryMechanics.INVENTORY_COMMANDS)

    def _check_command_combination(self):
        """ Check if user command combinations are correct. """

        task = self.GAME_COMMANDS.get(self.command)
        task_signature = inspect.signature(task)

        if str(task_signature) == '()' and self.argument:
            return True
        else:
            return False

    def _incorrect_command_combination(self):

        callable_signature = inspect.signature(self.task)
        return str(callable_signature) == '()' and self.argument

    # GameMechanics command errors
    # [] TODO: create custom error types, i.e. GameCommandError, PlayerCommandError, etc.
    def _command_error(self):

        if not self.command:
            # Do nothing and continue the game loop
            ...
        elif self.command not in self.GAME_COMMANDS.keys():
            self._unrecognized_command()

    def _unrecognized_command(self):

        print(f'\'{self.command}\' is not a valid command.\n\nSee \'help\' command.')

    def _incomplete_command(self):

        print(f'{self.command} needs a value to work.')

    def _incorrect_command(self):

        print(f'\'{self.command}\' does not need to have an argument \'{self.argument}\'')


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

        print(f'+\'{item}\' added to inventory')

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
