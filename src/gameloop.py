"""
Leaf - simple text-based planting game for the bored developer.
"""

import sys
import time

__version__ = '0.1.1'
COMMAND = None
command = None
ARGUMENT = None
argument = None
INVENTORY = {'seeds': ['tomato', 'chili pepper']}
HELP = """\nLeaf valid commands:\n
    till*           - till the current spot/location
    plant* <seed>    - plant a particular seed
    water           - water current spot/location
    fertilize       - add fertilizer to current spot/location
    
    inventory       - display current items in inventory
    market          - go the market and shop for goods
    buy             - buy item
    sell            - sell item
    
    help*            - show this help information
    exit or quit*    - exit the application

* - currently working"""


def game_loop():

    welcome_message()
    while True:
        get_commmand()
        process_command()
        display_result()


def welcome_message():

    message = f'Leaf\n' \
              f'Simple text-based planting game for the bored developer.\n' \
              f'-------------------------------------------------------- \
                \n\nVersion: {__version__}' \
              f'\n\nType \'help\' for the list of valid commands.'
    print(f'{message}')


def get_commmand():

    global COMMAND
    global command
    global ARGUMENT
    global argument

    # [] TODO: test parsing of user input
    user_input = str(input('\nLEAF > ')).split(maxsplit=1)

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
        print(HELP)

    elif command == 'till':
        print('*tilling the soil*')
        time.sleep(4)
        print('soil tilled!')

    elif command == 'plant':
        if argument:
            if argument in seeds:
                print(f'planting {argument}')
                time.sleep(5)
                print(f'{argument} planted!')
            else:
                print(f'\'{argument}\' not in inventory')
        else:
            print('incomplete command, must be plant <seed>')

    else:
        print(f'\'{command}\' is not a valid command.\n{HELP}')


def display_result():

    # [] TODO: get data to output from process_command function
    ...


if __name__ == "__main__":
    game_loop()
