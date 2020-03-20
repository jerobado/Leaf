# creating a simple game loop

import sys
import time

COMMAND = None
command = None
ARGUMENT = None
argument = None
INVENTORY = {'seeds': ['tomato', 'chili pepper']}


def game_loop():

    while True:
        get_commmand()
        process_command()
        display_result()


def get_commmand():

    global COMMAND
    global command
    global ARGUMENT
    global argument

    user_input = str(input('leaf > ')).split(maxsplit=1)

    if len(user_input) > 1:
        COMMAND, ARGUMENT = user_input
        command = COMMAND
        argument = ARGUMENT
    else:
        COMMAND = user_input
        command = COMMAND[0]


def process_command():

    global COMMAND
    global command
    global ARGUMENT
    global argument
    global INVENTORY

    # command = COMMAND[0]
    # argument = ARGUMENT[1]
    seeds = INVENTORY['seeds']

    if command in ['exit', 'quit']:
        sys.exit()

    elif command == 'help':
        help = """\nValid commands:
        till            - till the current spot/location
        plant <seed>    - plant a particular seed
        water           - water current spot/location
        fertilize       - add fertilizer to current spot/location

        market          - go the market and shop for goods
        buy             - buy item
        sell            - sell item
        inventory       - display current items in inventory

        help            - show this help information
        exit or quit    - exit the application
        """
        print(help)

    elif command == 'till':
        print('tilling the soil')
        time.sleep(3)
        print('soil tilled!')

    elif command == 'plant':
        if argument:
            if argument in seeds:
                print(f'planting {argument}')
                time.sleep(5)
                print(f'{argument} planted!')
            else:
                print(f'{argument} not in inventory')
        else:
            print('incomeplete command, must be `plant <seed>')


def display_result():

    ...


if __name__ == "__main__":
    game_loop()

