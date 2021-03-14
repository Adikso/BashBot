from discord.ext import commands

from bashbot.core.exceptions import SessionDontExistException
from bashbot.terminal.sessions import sessions


def session_exists():
    async def predicate(ctx):
        if not sessions().by_channel(ctx.message.channel):
            raise SessionDontExistException()

        return True

    return commands.check(predicate)

