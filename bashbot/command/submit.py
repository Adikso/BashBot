from discord import Embed
from discord.ext import commands
from discord.ext.commands import Context

from bashbot.command import session_exists
from bashbot.constants import EMBED_COLOR
from bashbot.terminal.sessions import sessions


class SubmitCommand(commands.Cog):
    @commands.hybrid_command(
        name='submit',
        aliases=['.submit'],
        description='Toggles auto submit mode'
    )
    @session_exists()
    async def submit(self, ctx: Context):
        terminal = sessions().by_channel(ctx.channel)

        terminal.auto_submit = not terminal.auto_submit
        if terminal.auto_submit:
            embed = Embed(description=f"Enabled auto submit mode", color=EMBED_COLOR)
            await ctx.send(embed=embed)
        else:
            embed = Embed(description=f"Disabled auto submit mode", color=EMBED_COLOR)
            await ctx.send(embed=embed)
