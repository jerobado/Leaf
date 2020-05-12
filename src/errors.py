# Leaf Game Errors
class LeafGameError(Exception):

    pass


class NoCommandError(LeafGameError):
    """ Raised when the user enters a blank command. """

    def __init__(self):

        pass


class MismatchCommandError(LeafGameError):
    """ Raised when the user enter mismatch commands, i.e. till something. """

    def __init__(self, command, argument):

        print(f'\'{command}\' does not need to have an argument \'{argument}\'')


class UnregisteredCommandError(LeafGameError):
    """ Raised when the player enter an unregistered Leaf commands. i.e jump. """

    def __init__(self, command):

        print(f'\'{command}\' is not a valid command.\n\nSee \'help\' command.')


class IncompleteCommandError(LeafGameError):
    """ Raised when the player enters a command that requires an argument, i.e. plant or harvest. """

    def __init__(self, command):

        print(f'Incomplete command, should be {command} [value], i.e. {command} something')
