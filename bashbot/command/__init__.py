from discord.ext import commands

from bashbot.exceptions import SessionDontExistException
from bashbot.terminal.sessions import Sessions


def session_exists():
    async def predicate(ctx):
        if not Sessions().get(ctx.message.channel):
            raise SessionDontExistException()

        return True

    return commands.check(predicate)


def has_permission(name):
    async def predicate(ctx):
        return True

    return commands.check(predicate)
