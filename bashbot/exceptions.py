from discord.ext import commands


class ArgumentFormatException(commands.CheckFailure):
    def __init__(self, message):
        self.message = message


class SessionDontExistException(commands.CheckFailure):
    def __init__(self):
        self.message = 'You are trying to access controls of non-existing terminal'
