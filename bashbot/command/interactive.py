from discord.ext import commands
from discord.ext.commands import Context

from bashbot.command import session_exists
from bashbot.core.exceptions import SessionDontExistException
from bashbot.terminal.sessions import sessions


class InteractiveCommand(commands.Cog):
    @commands.command(
        name='.interact',
        aliases=['.i'],
        description='Toggles interactive mode where all messages are sent to terminal'
    )
    @session_exists()
    async def interactive(self, ctx: Context):
        terminal = sessions().by_channel(ctx.message.channel)

        if not terminal:
            raise SessionDontExistException()

        terminal.interactive = not terminal.interactive

        if terminal.interactive:
            await ctx.send(f"`Entered interactive mode. Repeat command to disable`")
        else:
            await ctx.send(f"`Exited interactive mode`")
