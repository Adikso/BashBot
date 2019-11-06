from discord.ext import commands

from bashbot.command import has_permission
from bashbot.terminal.sessions import sessions


class CloseCommand(commands.Cog):
    @commands.command(name='.close')
    @has_permission('session.close')
    async def close(self, ctx, name):
        terminal = sessions().get_by_name(name)
        if not terminal:
            return

        terminal.close()
        sessions().remove(terminal)
