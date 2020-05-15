import inspect
import unittest
import sys
from datetime import (datetime,
                      timedelta)

from src.data.constant import SeedCatalog
from src.errors import (NoCommandError,
                        MismatchCommandError,
                        UnregisteredCommandError,
                        IncompleteCommandError)
from src.mechanics import (GameMechanics,
                           InventoryMechanics,
                           PlayerMechanics,
                           GrowthMechanics)


class TestGameMechanics(unittest.TestCase):

    def setUp(self):

        self.leafGameMechanics = GameMechanics()
        self.leafInventoryMechanics = InventoryMechanics()

    def test_RESET_COMMANDS_function(self):

        self.leafGameMechanics.command = 'plant'
        self.leafGameMechanics.argument = 'coconut'
        self.leafGameMechanics.reset_commands()

        self.assertIsNone(self.leafGameMechanics.command)
        self.assertIsNone(self.leafGameMechanics.argument)

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

    def test_PARSE_COMMANDS_function_single(self):

        # Single command
        self.leafGameMechanics.raw_command = ['harvest']
        self.leafGameMechanics.parse_commands()

        self.assertEqual('harvest', self.leafGameMechanics.command)
        self.assertFalse(self.leafGameMechanics.isCommandMultiple)
        self.assertIsNone(self.leafGameMechanics.argument)

    def test_PARSE_COMMANDS_function_multiple(self):

        # Multiple commands (with argument)
        self.leafGameMechanics.raw_command = ['plant', 'tomato']
        self.leafGameMechanics.parse_commands()

        self.assertEqual('plant', self.leafGameMechanics.command)
        self.assertEqual('tomato', self.leafGameMechanics.argument)
        self.assertTrue(self.leafGameMechanics.isCommandMultiple)

    def test_GET_COMMAND_ACTION_if_task_isMethod(self):
        """ Test if 'task' is a valid method. """

        self.leafGameMechanics.command = 'till'
        self.leafGameMechanics.get_command_action()

        result = inspect.ismethod(self.leafGameMechanics.task)
        self.assertTrue(result)

    def test_VALIDATE_COMMAND_function_if_raises_UnregisteredCommandError(self):

        self.leafGameMechanics.command = 'unknown-command'
        self.leafGameMechanics.get_command_action()

        result = self.leafGameMechanics._validate_command
        self.assertRaises(UnregisteredCommandError, result, command=self.leafGameMechanics.command)

    def test_VALIDATE_COMMAND_function_if_raises_MismatchCommandError(self):

        self.leafGameMechanics.command = 'check'
        self.leafGameMechanics.argument = 'something'
        self.leafGameMechanics.get_command_action()

        result = self.leafGameMechanics._validate_command
        self.assertRaises(MismatchCommandError, result, command=self.leafGameMechanics.command)

    def test_VALIDATE_COMMAND_function_if_raises_IncompleteCommandError(self):

        self.leafGameMechanics.command = 'plant'
        self.leafGameMechanics.get_command_action()

        result = self.leafGameMechanics._validate_command
        self.assertRaises(IncompleteCommandError, result, command=self.leafGameMechanics.command)


class TestGrowthMechanics(unittest.TestCase):

    def setUp(self):

        self.plantGrowthMechanics = GrowthMechanics('test-seed', 1)

    def test_INIT_function_object_type(self):

        self.assertIsInstance(self.plantGrowthMechanics.name, str)
        self.assertIsInstance(self.plantGrowthMechanics.duration, int)

    def test_INIT_function_time_started_attribute(self):

        self.plantGrowthMechanics.start()

        self.assertIsInstance(self.plantGrowthMechanics.time_started, datetime)

    def test_ADD_DURATION_TO_TIME_STARTED_function(self):

        self.plantGrowthMechanics = GrowthMechanics('test-seed', 3)
        self.plantGrowthMechanics.start()

        start = self.plantGrowthMechanics.time_started
        duration = self.plantGrowthMechanics.duration
        end = start + timedelta(seconds=duration)

        # check if difference is 3 seconds
        diff = end - timedelta(seconds=duration)

        self.assertEqual(diff, start)

    def test_REMAINING_TIME(self):

        self.plantGrowthMechanics = GrowthMechanics('test-seed', 3)
        self.plantGrowthMechanics.start()

        start = self.plantGrowthMechanics.time_started
        duration = self.plantGrowthMechanics.duration
        end = start + timedelta(seconds=duration)
        diff = end - timedelta(seconds=duration)
        remaining = end - datetime.now()

        self.assertEqual(3, remaining.seconds)


class TestPlayerMechanics(unittest.TestCase):

    def setUp(self):

        self.playerMechanics = PlayerMechanics()
        self.playerMechanics.playerInventoryMechanics = InventoryMechanics()

    def test_TILL_isTilled_true(self):

        self.playerMechanics.till()

        self.assertTrue(self.playerMechanics.isTilled)

    def test_PLANT_isTilled_false_and_return_zero(self):
        """ Test isTilled if false and return 0 if till() is not called first. """

        result = self.playerMechanics.plant()
        self.assertFalse(self.playerMechanics.isTilled)
        self.assertEqual(0, result)

    def test_PLANT_if_seed_doesnt_exist_in_inventory(self):

        self.playerMechanics.isTilled = True

        result = self.playerMechanics.plant('coke')
        self.assertEqual(0, result)

    def test_PLANT_if_seed_has_been_planted(self):

        seed = '__test_seed__'
        self.playerMechanics.playerInventoryMechanics.add_item(seed)
        self.playerMechanics.isTilled = True
        self.playerMechanics.plant(seed)

        self.assertNotIn(seed, self.playerMechanics.playerInventoryMechanics.inventoryDeque)
        self.assertFalse(self.playerMechanics.isTilled)


class TestInventoryMechanics(unittest.TestCase):

    def setUp(self):

        self.playerMechanics = PlayerMechanics()
        self.playerMechanics.playerInventoryMechanics = InventoryMechanics()

    def test_ADD_ITEM_function_if_seed_exists_in_inventory(self):

        seed = 'eggplant'
        self.playerMechanics.playerInventoryMechanics.add_item(seed)

        self.assertIn(seed, self.playerMechanics.playerInventoryMechanics.inventoryDeque)

    def test_REMOVE_ITEM_function_if_seed_removed_in_inventory(self):

        seed = 'grape'
        self.playerMechanics.playerInventoryMechanics.inventoryDeque.append(seed)
        self.playerMechanics.playerInventoryMechanics.remove_item(seed)

        self.assertNotIn(seed, self.playerMechanics.playerInventoryMechanics.inventoryDeque)

    def test_REMOVE_ITEM_if_will_return_zero_if_seed_doesnt_exist(self):

        seed = 'rock'

        result = self.playerMechanics.playerInventoryMechanics.remove_item(seed)
        self.assertEqual(0, result)


if __name__ == '__main__':
    unittest.main()
