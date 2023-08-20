from discord import Embed, Interaction, app_commands
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

    @select.autocomplete('name')
    async def select_autocomplete(self, interaction: Interaction, current: str):
        results = sessions().search(current)
        return [
            app_commands.Choice(name=option.name, value=option.name)
            for option in results
        ]
