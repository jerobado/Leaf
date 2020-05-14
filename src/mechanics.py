# Classes of game mechanics

import inspect
import sys
import time
import threading
from collections import (Counter,
                         deque)
from datetime import (datetime,
                      timedelta)
from src.data.constant import (HELP,
                               WELCOME_MESSAGE,
                               QUIT_MESSAGE,
                               SeedCatalog)
from src.errors import (NoCommandError,
                        MismatchCommandError,
                        UnregisteredCommandError,
                        IncompleteCommandError)


class GameMechanics:

    def __init__(self):

        self.GAME_COMMANDS = {'help': self.help,
                              'quit': self.quit}
        self.inventoryMechanics = InventoryMechanics()
        self.playerMechanics = PlayerMechanics()
        self.playerMechanics.playerInventoryMechanics = self.inventoryMechanics
        self.raw_command = None
        self.command = None
        self.argument = None
        self.task = None                    # function to execute
        self.isCommandMultiple = bool       # multiple commands or single

        self._combine_commands()

    def _combine_commands(self):

        self.GAME_COMMANDS.update(self.playerMechanics.PLAYER_COMMANDS)
        self.GAME_COMMANDS.update(self.inventoryMechanics.INVENTORY_COMMANDS)

    def help(self):

        print(HELP)

    def quit(self):

        print(QUIT_MESSAGE)
        sys.exit()

    def start_game(self):

        self.welcome_message()
        while True:
            try:
                self.reset_commands()
                self.get_commands()
                self.parse_commands()
                self.get_command_action()
                self.process_commands()
            except (NoCommandError, MismatchCommandError, UnregisteredCommandError, IncompleteCommandError):
                continue

    def welcome_message(self):

        print(WELCOME_MESSAGE)

    def reset_commands(self):

        self.command = None
        self.argument = None

    def get_commands(self):

        self.raw_command = str(input('\nLEAF > ')).split(maxsplit=1)
        if not self.raw_command:
            raise NoCommandError

    def parse_commands(self):

        command_count = len(self.raw_command)
        if command_count == 1:
            self.command = self.raw_command[0]
            self.isCommandMultiple = False
        elif command_count > 1:
            self.command, self.argument = self.raw_command
            self.isCommandMultiple = True

    def get_command_action(self):

        task = self.GAME_COMMANDS.get(self.command)
        if task:
            self.task = task
        else:
            raise UnregisteredCommandError(self.command)

    def process_commands(self):

        self._validate_command(self.task)

        if self.isCommandMultiple:
            self.task(self.argument)
        else:
            self.task()

    def _validate_command(self, method):

        signature = str(inspect.signature(method))
        if signature == '()' and self.argument:
            raise MismatchCommandError(self.command, self.argument)
        elif signature != '()' and not self.argument:
            raise IncompleteCommandError(self.command)


class PlayerMechanics:

    def __init__(self):

        self.PLAYER_COMMANDS = {'till': self.till,
                                'plant': self.plant,
                                'check': self.check,
                                'harvest': self.harvest}

        self.playerInventoryMechanics = None
        self.plantGrowthMechanics = None
        self.growing_plants = deque()        # list of active and non-active threads
        self.isTilled = False

    def till(self):

        # [] TODO: add a mechanics that will prevent other commands from executing if this is not executed first
        print('tilling the soil...')
        time.sleep(5)
        print('soil tilled!')
        self.isTilled = True

    def plant(self, seed=None):

        if not self.isTilled:
            print('You need to \'till\' the soil first before planting.')
            return 0

        if seed not in self.playerInventoryMechanics.inventoryDeque:
            print(f'You don\'t have a \'{seed}\' in your inventory.')
            return 0

        # Get seed information from Seed Catalog
        seed_details = SeedCatalog(seed)

        # Remove seed in player's inventory
        self.playerInventoryMechanics.remove_item(seed)

        # Simulate planting
        print(f'planting {seed}...')
        time.sleep(3)

        # Start growing plant
        self.plantGrowthMechanics = GrowthMechanics(seed, duration=seed_details.duration)
        self.growing_plants.append(self.plantGrowthMechanics)
        self.plantGrowthMechanics.start()
        print(f'{seed} planted!')

        # Reset isTilled
        self.isTilled = False

    def check(self):

        PAD = 16

        # [] TODO: display growth percentage of planted crop
        print(f'{"#":<10}{"DESCRIPTION":<{PAD}}{"REMAINING (h:mm:ss)":<{PAD}}')
        for index, plant in enumerate(self.growing_plants):
            print(f'{index:<10}{plant.name:<{PAD}}{plant._remaining_time()}')

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
                                   'add': self.add_item}
        self.inventoryDeque = deque()
        self.inventoryCounter = Counter(self.inventoryDeque)

    def inventory(self):

        print(f'{"ITEM":<16}{"QUANTITY":<16}')
        for item in set(self.inventoryDeque):
            print(f'{item:<16}{self.inventoryCounter[item]:<16}')

    # [] TODO: you can literally add anything! Limit this!
    def add_item(self, item=None):

        if item:
            self.inventoryDeque.append(item)

            # update inventoryCounter
            self.inventoryCounter = Counter(self.inventoryDeque)
            print(f'+1 \'{item}\' added to inventory')
        else:
            print('Incomplete command, should be add [item], i.e. add watermelon')

    def remove_item(self, item):

        self.inventoryDeque.remove(item)

        # Update inventoryCounter
        self.inventoryCounter = Counter(self.inventoryDeque)


class GrowthMechanics(threading.Thread):

    def __init__(self, seed, duration):

        super().__init__()
        self.name = str(seed)
        self.duration = int(duration)
        self.time_started = datetime
        self.time_remaining = timedelta

    def run(self):

        self.time_started = datetime.now()
        time.sleep(self.duration)

    def _remaining_time(self):

        start = self.time_started
        end = start + timedelta(seconds=self.duration)
        remaining = end - datetime.now()

        if self.is_alive():
            return str(remaining)[:-7]  # [:-7] truncates milliseconds
        else:
            return timedelta()          # T-0
