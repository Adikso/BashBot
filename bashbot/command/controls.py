from discord.ext import commands

from bashbot.command import session_exists, has_permission
from bashbot.terminal.sessions import sessions


class ControlsCommand(commands.Cog):
    @commands.group(name='.controls')
    async def controls(self, ctx):
        if ctx.invoked_subcommand is None:
            pass

    @controls.command()
    @session_exists()
    @has_permission('input.controls.manage')
    async def add(self, ctx, emoji_id, content):
        sessions().get(ctx)

    @controls.command()
    @session_exists()
    @has_permission('input.controls.manage')
    async def remove(self, ctx, emoji_id):
        sessions().get(ctx)
