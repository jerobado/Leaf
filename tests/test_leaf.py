import unittest
import sys


# Unit testing
class LeafTestCase(unittest.TestCase):

    def test_single_command(self):
        """
        Test to accept only single command.

        i.e. LEAF > till
        """

        command = input('LEAF (single) > ').split(maxsplit=1)
        result = len(command)
        expected = 1

        self.assertEqual(expected, result)

    def test_multiple_commands(self):
        """
        Test to accept multiple commands.

        i.e. LEAF > plant tomato
        """

        command = input('LEAF (multiple) > ').split(maxsplit=1)
        result = len(command)
        expected = 2

        self.assertEqual(expected, result)


# Integration testing
class LeafIntegrationTesting(unittest.TestCase):

    ...


if __name__ == '__main__':
    unittest.main()
