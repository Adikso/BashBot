from discord import Embed
from discord.ext import commands
from discord.ext.commands import Context

from bashbot.constants import EMBED_COLOR
from bashbot.core.exceptions import SessionDontExistException
from bashbot.terminal.sessions import sessions


class RepeatCommand(commands.Cog):
    @commands.hybrid_command(
        name='repeat',
        aliases=['.repeat', '.r'],
        description='Repeats string n times and sends to the current terminal session',
        usage='<string..>'
    )
    async def repeat(self, ctx: Context, n: int, *, text):
        terminal = sessions().by_channel(ctx.message.channel)
        if not terminal:
            raise SessionDontExistException()

        terminal.send_input(text * n)

        if ctx.interaction:
            embed = Embed(description=f"Text sent", color=EMBED_COLOR)
            await ctx.reply(embed=embed, ephemeral=False, delete_after=0)
