from discord.ext import commands
from discord.ext.commands import Context

from bashbot.command import session_exists
from bashbot.core.macros import execute_macro


class MacroCommand(commands.Cog):
    @commands.command(
        name='.macro',
        aliases=['.m'],
        description='Executes macro from "macros" directory',
        usage='<macro_name>'
    )
    @session_exists()
    async def macro(self, ctx: Context, macro_name: str):
        await execute_macro(ctx, macro_name)
        await ctx.send(f"`Executed macro {macro_name}`")
