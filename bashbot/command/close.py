from discord.ext import commands

from bashbot.command import has_permission, session_exists
from bashbot.core.exceptions import SessionDontExistException
from bashbot.core.settings import settings
from bashbot.terminal.sessions import sessions


class CloseCommand(commands.Cog):
    @commands.command(
        name='.close',
        aliases=['.c'],
        description='Closes current terminal session'
    )
    @has_permission('session.close')
    @session_exists()
    async def close(self, ctx):
        terminal = sessions().by_channel(ctx.message.channel)

        if not terminal:
            raise SessionDontExistException()

        terminal.close()

        if settings().get('terminal.delete_on_close'):
            message = sessions().find_message(terminal)
            await message.delete()

        sessions().remove(terminal)
        await ctx.send(f"`Closed terminal #{terminal.name}`")
