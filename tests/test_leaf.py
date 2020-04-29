import inspect
import unittest
import sys

from src.mechanics import (GameMechanics,
                           InventoryMechanics,
                           PlayerMechanics)


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

    def test_GET_COMMAND_ACTION_function(self):

        # Game
        self.leafGameMechanics.command = 'help'
        self.leafGameMechanics.get_command_action()
        self.assertTrue(self.leafGameMechanics.command in GameMechanics.__dict__.keys())

        # Inventory
        self.leafGameMechanics.command = 'inventory'
        self.leafGameMechanics.get_command_action()
        self.assertTrue(self.leafGameMechanics.command in InventoryMechanics.__dict__.keys())

        # Player
        self.leafGameMechanics.command = 'plant'
        self.leafGameMechanics.get_command_action()
        self.assertTrue(self.leafGameMechanics.command in PlayerMechanics.__dict__.keys())


if __name__ == '__main__':
    unittest.main()
