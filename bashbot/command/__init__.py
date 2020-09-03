from discord.ext import commands

from bashbot.exceptions import SessionDontExistException
from bashbot.terminal.sessions import sessions


def session_exists():
    async def predicate(ctx):
        if not sessions().get_by_channel(ctx.message.channel):
            raise SessionDontExistException()

        return True

    return commands.check(predicate)


def has_permission(name):
    async def predicate(ctx):
        return True

    return commands.check(predicate)
