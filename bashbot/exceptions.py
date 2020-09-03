from discord.ext import commands


class ArgumentFormatException(commands.CheckFailure):
    def __init__(self, message):
        self.message = message


class SessionDontExistException(commands.CheckFailure):
    def __init__(self):
        self.message = 'You need to have open terminal to use this command'


class TerminalNotFoundException(commands.CheckFailure):
    def __init__(self):
        self.message = 'Could not find requested terminal'


class MacroNotFoundException(commands.CheckFailure):
    def __init__(self):
        self.message = 'Macro with requested name not found'
