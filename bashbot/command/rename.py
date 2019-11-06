from discord.ext import commands

from bashbot.command import has_permission, session_exists
from bashbot.terminal.sessions import sessions


class RenameCommand(commands.Cog):
    @commands.command(name='.rename', aliases=['.r'])
    @has_permission('session.rename')
    @session_exists()
    async def rename(self, ctx, new_name):
        terminal = sessions().get_by_channel(ctx.message.channel)

        terminal.name = new_name
        terminal.refresh()
