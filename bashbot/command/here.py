from discord import Embed
from discord.ext import commands
from discord.ext.commands import Context

from bashbot.command import session_exists
from bashbot.constants import EMBED_COLOR
from bashbot.terminal.sessions import sessions


class HereCommand(commands.Cog):
    @commands.hybrid_command(
        name='here',
        aliases=['.here', '.h'],
        description='Moves selected terminal below the user message'
    )
    @session_exists()
    async def here(self, ctx: Context):
        terminal = sessions().by_channel(ctx.channel)
        message = sessions().find_message(terminal)

        await message.delete()
        sessions().remove(terminal)

        embed = Embed(description=f"Moving terminal...", color=EMBED_COLOR)
        message = await ctx.send(embed=embed)
        sessions().add(message, terminal)

        terminal.refresh()
