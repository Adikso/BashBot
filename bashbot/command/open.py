from discord.ext import commands

from bashbot.core.exceptions import ArgumentFormatException
from bashbot.core.macros import execute_macro
from bashbot.core.settings import settings
from bashbot.terminal.sessions import sessions
from bashbot.terminal.terminal import Terminal
from bashbot.core.utils import parse_template


class OpenCommand(commands.Cog):
    @commands.command(
        name='.open',
        aliases=['.o'],
        description='Opens new terminal session',
        usage='[name]'
    )
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

        # Prepare terminal
        sh_path = settings().get('terminal.shell_path')

        login_as_other_user = settings().get('terminal.user.login_as_other_user')
        if login_as_other_user:
            su_path = settings().get('terminal.su_path')
            login = settings().get('terminal.user.username')
            password = settings().get('terminal.user.password')

            terminal = Terminal(name, sh_path=sh_path, on_change=sessions().update_message, su_path=su_path, login=login, password=password)
        else:
            terminal = Terminal(name, sh_path=sh_path, on_change=sessions().update_message)

        sessions().add(message, terminal)
        terminal.open()

        # Run macro on terminal startup
        startup_macro = settings().get('terminal.startup_macro')
        if startup_macro:
            await execute_macro(ctx, startup_macro)
