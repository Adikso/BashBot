from discord.ext import commands
from discord.ext.commands import Context

from bashbot.command import has_permission, session_exists
from bashbot.terminal.sessions import sessions


class HereCommand(commands.Cog):
    @commands.command(name='.here', aliases=['.h'])
    @has_permission('session.here')
    @session_exists()
    async def here(self, ctx: Context):
        terminal = sessions().get_by_channel(ctx.channel)
        message = sessions().get_message(terminal)

        await message.delete()
        sessions().remove(terminal)

        message = await ctx.send("Moving terminal...")
        sessions().add(message, terminal)

        terminal.refresh()
