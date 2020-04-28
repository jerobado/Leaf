import inspect
import unittest
import sys

from src.mechanics import (GameMechanics,
                           InventoryMechanics)


class TestGameMechanics(unittest.TestCase):

    def setUp(self):

        self.leafGameMechanics = GameMechanics()
        self.leafInventoryMechanics = InventoryMechanics()

    def test_GET_COMMANDS_function(self):

        none_commands = ''
        single_commands = 'till'
        multiple_commands = 'plant lettuce'

        # See GameMechanics.get_commands() function for the full implementation
        none_result = none_commands.split(maxsplit=1)
        single_result = single_commands.split(maxsplit=1)
        multiple_result = multiple_commands.split(maxsplit=1)

        none_expected = []
        single_expected = ['till']
        multiple_expected = ['plant', 'lettuce']

        self.assertEqual(none_expected, none_result)
        self.assertEqual(single_expected, single_result)
        self.assertEqual(multiple_expected, multiple_result)

    def test_PARSE_COMMANDS_function_none(self):
        """ Test parse_command() if with no given command by the player. """

        # No commands
        self.leafGameMechanics.rCommand = ''
        self.leafGameMechanics.parse_commands()

        self.assertIsNone(self.leafGameMechanics.isMultiple)
        self.assertIsNone(self.leafGameMechanics.command)

    def test_PARSE_COMMANDS_function_single(self):

        # Single command
        self.leafGameMechanics.rCommand = ['harvest']
        self.leafGameMechanics.parse_commands()

        self.assertFalse(self.leafGameMechanics.isMultiple)
        self.assertEqual('harvest', self.leafGameMechanics.command)
        self.assertIsNone(self.leafGameMechanics.argument)

    def test_PARSE_COMMANDS_function_multiple(self):

        # Multiple commands
        self.leafGameMechanics.rCommand = ['plant', 'tomato']
        self.leafGameMechanics.parse_commands()

        self.assertTrue(self.leafGameMechanics.isMultiple)
        self.assertEqual('plant', self.leafGameMechanics.command)
        self.assertEqual('tomato', self.leafGameMechanics.argument)

    def test_GET_COMMAND_TYPE_function_task_instance(self):

        self.leafGameMechanics.command = 'inventory'
        self.leafGameMechanics.get_command_type()

        # print(self.leafGameMechanics.task)
        print(self.leafGameMechanics.task)

        expected = self.leafGameMechanics.task

        # [] TODO: check if self.leafInventoryMechanics.task is a member of InventoryMechanics.__dict__

        result = inspect.getmembers(InventoryMechanics)
        print('using inspect')
        for i, v in result:
            if i == 'inventory':
                print(i, v)
                result = v

        print('InventoryMechanics')
        for i, v in InventoryMechanics.__dict__.items():
            print(i, v)

        self.leafGameMechanics.task()



if __name__ == '__main__':
    unittest.main()
