from discord import Embed
from discord.ext import commands

from bashbot.command import session_exists
from bashbot.constants import EMBED_COLOR
from bashbot.terminal.sessions import sessions


class RenameCommand(commands.Cog):
    @commands.hybrid_command(
        name='rename',
        aliases=['.rename'],
        description='Changes session name',
        usage='<new_name>'
    )
    @session_exists()
    async def rename(self, ctx, new_name):
        terminal = sessions().by_channel(ctx.message.channel)

        old_name = terminal.name
        terminal.name = new_name
        terminal.refresh()

        embed = Embed(description=f"Renamed terminal #{old_name} -> #{new_name}", color=EMBED_COLOR)
        await ctx.send(embed=embed)
