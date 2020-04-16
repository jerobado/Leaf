# Classes of game mechanics

import sys
import time

__version__ = '0.1.2'


class GameMechanics:

    def __init__(self):

        self.COMMANDS = {'help': self.help,
                         'quit': self.quit}

        self._combine_commands()

        self.rCommand = None    # user's raw command(s)
        self.command = None
        self.argument = None
        self.task = None        # function to execute
        self.multiple = bool    # multiple commands or single

    def help(self):

        HELP = """\nLeaf valid commands:\n
            till*           - till the current spot/location
            plant* <seed>    - plant a particular seed
            water           - water current spot/location
            fertilize       - add fertilizer to current spot/location
            harvest         - harvest fully grown crop

            check           - examine soil

            inventory       - display current items in inventory
            market          - visit the farmer's market
            buy             - buy item
            sell            - sell item

            help*            - show this help information
            exit or quit*    - exit the application

        * - currently working"""
        print(HELP)

    def quit(self):

        print('Leaf closing. See you soon!')
        sys.exit()

    def startgame(self):

        self.welcome_message()
        while True:
            self.get_commands()
            self.parse_commands()
            self.get_command_type()
            self.process_commands()

    def welcome_message(self):

        message = f'Leaf\n' \
                  f'Simple text-based farming game for the bored developer.\n' \
                  f'-------------------------------------------------------- \
                    \n\nVersion: {__version__}' \
                  f'\n\nType \'help\' for the list of valid commands.'
        print(f'{message}')

    def get_commands(self):

        self.rCommand = str(input('\nLEAF > ')).split(maxsplit=1)

    def parse_commands(self):

        input_count = len(self.rCommand)
        if input_count > 1:
            self.command, self.argument = self.rCommand
            self.multiple = True
        else:
            self.multiple = False
            self.command = self.rCommand[0]

    def get_command_type(self):

        self.task = self.COMMANDS.get(self.command,
                                      self._unrecognized_command)

    def process_commands(self):

        if self.multiple:
            self.task(self.argument)
        else:
            self.task()

    def _combine_commands(self):

        player = PlayerMechanics()
        self.COMMANDS.update(player.COMMANDS)

    # Game command errors
    def _unrecognized_command(self):

        print(f'\'{self.command}\' is not a valid command.\nSee \'help\' command.')

    def _incomplete_command(self):

        print(f'{self.command} needs a value to work.')


class PlayerMechanics:

    def __init__(self):

        self.COMMANDS = {'till': self.till,
                         'plant': self.plant,
                         'check': self.check,
                         'harvest': self.harvest}

        self.player_inventory = InventoryMechanics()

    def till(self):

        print('tilling the soil...')
        time.sleep(4)
        print('soil tilled!')

    def plant(self, seed=None):

        if seed:
            if seed in self.player_inventory.seeds.keys():
                print(f'planting {seed}...')
                time.sleep(5)
                print(f'{seed} planted!')
            else:
                print(f'You don\'t have a \'{seed}\' in your inventory.')
        else:
            print('Incomplete command, must be plant <seed>, i.e. plant tomato')

    def check(self):

        # [] TODO: display growth percentage of planted crop
        print('# TODO: display growth percentage of planted crop')

    def harvest(self):

        # [] TODO: display harvestable (100% growth) crops
        print('# TODO: display harvestable (100% growth) crops')


class InventoryMechanics:

    def __init__(self):

        # seed, time to grow
        self.seeds = {'tomato': 5,
                      'lettuce': 6}
