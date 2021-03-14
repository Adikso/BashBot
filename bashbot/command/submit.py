from discord.ext import commands
from discord.ext.commands import Context

from bashbot.command import session_exists
from bashbot.terminal.sessions import sessions


class SubmitCommand(commands.Cog):
    @commands.command(
        name='.submit',
        description='Toggles auto submit mode'
    )
    @session_exists()
    async def submit(self, ctx: Context):
        terminal = sessions().by_channel(ctx.channel)

        terminal.auto_submit = not terminal.auto_submit
        if terminal.auto_submit:
            await ctx.send(f'`Enabled auto submit mode`')
        else:
            await ctx.send(f'`Disabled auto submit mode`')
