from discord.ext import commands

from bashbot.command import has_permission
from bashbot.exceptions import SessionDontExistException
from bashbot.terminal.sessions import sessions


class CloseCommand(commands.Cog):
    @commands.command(name='.close', aliases=['.c'])
    @has_permission('session.close')
    async def close(self, ctx, name=None):
        if name:
            terminal = sessions().get_by_name(name)
        else:
            terminal = sessions().get_by_channel(ctx.message.channel)

        if not terminal:
            raise SessionDontExistException()

        terminal.close()
        sessions().remove(terminal)
