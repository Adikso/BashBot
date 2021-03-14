from discord.ext import commands

from bashbot.core.exceptions import SessionDontExistException
from bashbot.terminal.sessions import sessions


class RepeatCommand(commands.Cog):
    @commands.command(
        name='.repeat',
        aliases=['.r'],
        description='Repeats string n times and sends to the current terminal session',
        usage='<string..>'
    )
    async def repeat(self, ctx, n: int, *, text):
        terminal = sessions().by_channel(ctx.message.channel)
        if not terminal:
            raise SessionDontExistException()

        terminal.send_input(text * n)
