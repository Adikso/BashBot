from discord.ext import commands
from discord.ext.commands import Context

from bashbot.command import session_exists
from bashbot.terminal.sessions import sessions


class HereCommand(commands.Cog):
    @commands.command(
        name='.here',
        aliases=['.h'],
        description='Moves selected terminal below the user message'
    )
    @session_exists()
    async def here(self, ctx: Context):
        terminal = sessions().by_channel(ctx.channel)
        message = sessions().find_message(terminal)

        await message.delete()
        sessions().remove(terminal)

        message = await ctx.send("Moving terminal...")
        sessions().add(message, terminal)

        terminal.refresh()
