from discord.ext import commands
from discord.ext.commands import Context

from bashbot.command import has_permission, session_exists
from bashbot.macros import execute_macro


class MacroCommand(commands.Cog):
    @commands.command(name='.macro', aliases=['.m'])
    @has_permission('session.macro')
    @session_exists()
    async def macro(self, ctx: Context, macro_name: str):
        await execute_macro(ctx, macro_name)
        await ctx.send(f"`Executed macro {macro_name}`")
