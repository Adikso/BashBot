from discord import Embed
from discord.ext import commands

from bashbot.constants import EMBED_COLOR
from bashbot.core.exceptions import TerminalNotFoundException
from bashbot.terminal.sessions import sessions


class SelectCommand(commands.Cog):
    @commands.hybrid_command(
        name='select',
        aliases=['.select', '.s'],
        description='Sets terminal as selected',
        usage='[name]'
    )
    async def select(self, ctx, name):
        terminal = sessions().by_name(name)
        if not terminal:
            raise TerminalNotFoundException()

        sessions().select(ctx.message.channel, terminal)
        embed = Embed(description=f"Selected terminal #{name}", color=EMBED_COLOR)
        await ctx.send(embed=embed)
