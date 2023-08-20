from discord import Embed
from discord.ext import commands
from discord.ext.commands import Context

from bashbot.command import session_exists
from bashbot.constants import EMBED_COLOR
from bashbot.core.macros import execute_macro


class MacroCommand(commands.Cog):
    @commands.command(
        name='macro',
        aliases=['.macro', '.m'],
        description='Executes macro from "macros" directory',
        usage='<macro_name>'
    )
    @session_exists()
    async def macro(self, ctx: Context, macro_name: str):
        await execute_macro(ctx, macro_name)

        embed = Embed(description=f"Executed macro {macro_name}", color=EMBED_COLOR)
        await ctx.send(embed=embed)
