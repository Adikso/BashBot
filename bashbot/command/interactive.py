from discord.ext import commands
from discord.ext.commands import Context

from bashbot.command import has_permission, session_exists
from bashbot.exceptions import SessionDontExistException
from bashbot.terminal.sessions import sessions


class InteractiveCommand(commands.Cog):
    @commands.command(name='.interact', aliases=['.i'])
    @has_permission('session.interactive')
    @session_exists()
    async def interactive(self, ctx: Context):
        terminal = sessions().get_by_channel(ctx.message.channel)

        if not terminal:
            raise SessionDontExistException()

        terminal.interactive = not terminal.interactive

        if terminal.interactive:
            await ctx.send(f"`Entered interactive mode. Repeat command to disable`")
        else:
            await ctx.send(f"`Exited interactive mode`")
