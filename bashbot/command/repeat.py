from discord.ext import commands

from bashbot.command import has_permission
from bashbot.exceptions import SessionDontExistException
from bashbot.terminal.sessions import sessions


class RepeatCommand(commands.Cog):
    @commands.command(name='.repeat', aliases=['.r'])
    @has_permission('session.repeat')
    async def repeat(self, ctx, n: int, *, text):
        terminal = sessions().get_by_channel(ctx.message.channel)
        if not terminal:
            raise SessionDontExistException()

        terminal.input(text * n)
