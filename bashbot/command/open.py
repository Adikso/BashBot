from discord.ext import commands

from bashbot.command import has_permission
from bashbot.exceptions import ArgumentFormatException
from bashbot.settings import settings
from bashbot.terminal.sessions import sessions
from bashbot.terminal.terminal import Terminal
from bashbot.utils import parse_template


class OpenCommand(commands.Cog):
    @commands.command(name='.open', aliases=['.o'])
    @has_permission('session.open')
    async def open(self, ctx, name: str = None):
        if name and len(name) > 20:
            raise ArgumentFormatException('Session name length exceeds 20 characters limit')

        # Auto-generated name
        if not name:
            name = str(len(sessions().sessions))

        content = parse_template(
            settings().get('terminal.template'),
            name=name,
            state='OPENING',
            content='Waiting for tty..'
        )
        message = await ctx.send(content)

        sh_path = settings().get('terminal.shell_path')
        terminal = Terminal(name, sh_path=sh_path, on_change=sessions().update_message)
        terminal.open()

        sessions().add(message, terminal)
