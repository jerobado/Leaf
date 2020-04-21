# Classes of game mechanics


import sys
import time
import threading
from collections import deque

__version__ = '0.1.3'


class GameMechanics:

    def __init__(self):

        self.GAME_COMMANDS = {'help': self.help,
                              'quit': self.quit}
        self.playerMechanics = PlayerMechanics()
        self.rCommand = None            # user's raw command(s)
        self.command = None
        self.argument = None
        self.task = None                # function to execute
        self.isMultiple = bool          # multiple commands or single

        self._combine_commands()

    def help(self):

        HELP = """\nLeaf valid commands:\n
        till*           - till the current spot/location
        plant* <seed>   - plant a particular seed
        water           - water current spot/location
        fertilize       - add fertilizer to current spot/location
        harvest*        - harvest fully grown crop

        check*          - examine soil

        inventory       - display current items in inventory
        market          - visit the farmer's market
        buy             - buy item
        sell            - sell item

        help*           - show this help information
        quit*           - exit the application

    * - currently working"""
        print(HELP)

    def quit(self):

        print('Leaf closing. See you soon!')
        sys.exit()

    def start_game(self):

        self.welcome_message()
        while True:
            self.get_commands()
            self.parse_commands()
            self.get_command_type()
            self.process_commands()

    def welcome_message(self):

        message = f'Leaf\n' \
                  f'Simple text-based farming game for the bored developer.\n' \
                  f'------------------------------------------------------- \
                    \n\nVersion: {__version__}' \
                  f'\n\nType \'help\' for the list of valid commands.'
        print(f'{message}')

    def get_commands(self):

        self.rCommand = str(input('\nLEAF > ')).split(maxsplit=1)

    def parse_commands(self):

        input_count = len(self.rCommand)
        if input_count == 1:
            self.isMultiple = False
            self.command = self.rCommand[0]
        else:
            self.command, self.argument = self.rCommand
            self.isMultiple = True

    # [] TODO: test next
    def get_command_type(self):

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

    # GameMechanics command errors
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

        self.playerInventoryMechanics = InventoryMechanics()
        self.plantGrowthMechanics = None
        self.growing_plants = deque()        # list of active and non-active threads

    def till(self):

        # [] TODO: add a mechanics that will prevent other commands from executing if this is not executed first
        print('tilling the soil...')
        time.sleep(5)
        print('soil tilled!')

    def plant(self, seed=None):

        if seed:
            if seed in self.playerInventoryMechanics.seeds.keys():
                # [] TODO: deduct 1 seed to player's inventory
                print(f'planting {seed}...')
                time.sleep(3)
                # start growing plant
                self.plantGrowthMechanics = GrowthMechanics(seed, duration=self.playerInventoryMechanics.seeds[seed])
                self.growing_plants.append(self.plantGrowthMechanics)
                self.plantGrowthMechanics.start()
                print(f'{seed} planted!')
            else:
                print(f'You don\'t have a \'{seed}\' in your inventory.')
        else:
            print('Incomplete command, must be plant <seed>, i.e. plant tomato')

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

        # seed, duration (seconds)
        self.seeds = {'tomato': 15,
                      'lettuce': 16}

    def add_item(self):

        # [] TODO: implement adding new item(s) to inventory
        ...

    def remove_item(self):

        # [] TODO: implement removing item(s) to inventory
        ...


class GrowthMechanics(threading.Thread):

    def __init__(self, seed, duration):

        super().__init__()
        self.name = seed
        self.duration = duration

    def run(self):

        time.sleep(self.duration)
