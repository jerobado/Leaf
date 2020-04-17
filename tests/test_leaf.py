import unittest
import sys

from src.mechanics import GameMechanics


# Unit testing
class LeafTestCase(unittest.TestCase):

    def test_single_command(self):
        """
        Test to accept only single command.

        i.e. LEAF > till
        """

        command = 'till'.split(maxsplit=1)
        result = len(command)
        expected = 1

        self.assertEqual(expected, result)

    def test_multiple_commands(self):
        """
        Test to accept multiple commands.

        i.e. LEAF > plant tomato
        """

        command = 'plant tomato'.split(maxsplit=1)
        result = len(command)
        expected = 2

        self.assertEqual(expected, result)

    def test_if_command_exists(self):

        command = 'help'
        game = GameMechanics()
        result = command in game.GAME_COMMANDS.keys()
        expected = True

        self.assertEqual(expected, result)

    def test_assigning_and_executing_class_method(self):

        game = GameMechanics()
        execute = game.help
        result = execute()
        expected = None

        self.assertEqual(expected, result)


# Integration testing
class LeafIntegrationTesting(unittest.TestCase):

    def test_game_loop_flow(self):

        ...


if __name__ == '__main__':
    unittest.main()
