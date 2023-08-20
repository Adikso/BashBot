from discord import Embed
from discord.ext import commands
from discord.ext.commands import Context

from bashbot.command import session_exists
from bashbot.constants import EMBED_COLOR
from bashbot.core.exceptions import SessionDontExistException
from bashbot.terminal.sessions import sessions


class InteractiveCommand(commands.Cog):
    @commands.hybrid_command(
        name='interact',
        aliases=['.interact', '.i'],
        description='Toggles interactive mode where all messages are sent to terminal'
    )
    @session_exists()
    async def interactive(self, ctx: Context):
        terminal = sessions().by_channel(ctx.message.channel)

        if not terminal:
            raise SessionDontExistException()

        terminal.interactive = not terminal.interactive

        if terminal.interactive:
            embed = Embed(description=f"Entered interactive mode. Repeat command to disable", color=EMBED_COLOR)
            await ctx.send(embed=embed)
        else:
            embed = Embed(description=f"Exited interactive mode", color=EMBED_COLOR)
            await ctx.send(embed=embed)
