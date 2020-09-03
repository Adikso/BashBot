import discord
from discord import Message
from discord.abc import PrivateChannel
from discord.ext.commands import Bot, Context
from discord.utils import oauth_url

from bashbot.command.about import AboutCommand
from bashbot.command.close import CloseCommand
from bashbot.command.controls import ControlsCommand
from bashbot.command.freeze import FreezeCommand
from bashbot.command.here import HereCommand
from bashbot.command.open import OpenCommand
from bashbot.command.rename import RenameCommand
from bashbot.command.repeat import RepeatCommand
from bashbot.exceptions import SessionDontExistException, ArgumentFormatException
from bashbot.settings import settings
from bashbot.terminal.sessions import sessions
from bashbot.terminal.terminal import TerminalState
from bashbot.utils import get_logger, parse_template


class BashBot(Bot):
    logger = get_logger('BashBot')
    cmd_logger = get_logger('Command')

    def __init__(self, command_prefix, **options):
        super().__init__(command_prefix, **options)
        self.add_cog(OpenCommand())
        self.add_cog(CloseCommand())
        self.add_cog(HereCommand())
        self.add_cog(FreezeCommand())
        self.add_cog(RenameCommand())
        self.add_cog(ControlsCommand())
        self.add_cog(AboutCommand())
        self.add_cog(RepeatCommand())

    async def on_ready(self):
        self.logger.info(f'Logged in as {self.user.name} ({self.user.id})')
        self.logger.info(f'You can add bot to your server via {oauth_url(self.user.id)}')

        presence = parse_template(
            settings().get("discord.presence"),
            prefix=self.command_prefix
        )
        await self.change_presence(
            status=discord.Status.online,
            activity=discord.Game(presence)
        )

    async def on_message(self, message: Message):
        if message.author.bot:
            return

        terminal = sessions().get_by_channel(message.channel)

        if self.is_invoke(message):
            await self.process_commands(message)
        elif terminal and terminal.state == TerminalState.OPEN:
            terminal.input(message.content + '\n')
            self.cmd_logger.info(f"[{message.channel.guild.name}/#{message.channel.name}/{terminal.name}] {message.author.name} typed: {message.content}")

    async def on_command(self, ctx: Context):
        self.cmd_logger.info(f"[{ctx.message.channel.guild.name}/#{ctx.message.channel.name}] {ctx.message.author.name} invoked command: {ctx.message.content}")

    def is_invoke(self, message: Message):
        if isinstance(message.channel, PrivateChannel):
            return True

        has_prefix = any(message.content.startswith(prefix) for prefix in settings().get('commands.prefixes'))
        has_mention = self.user in message.mentions

        return has_prefix or has_mention

    async def on_command_error(self, ctx: Context, error):
        if isinstance(error, ArgumentFormatException):
            await ctx.send(error.message)

        if isinstance(error, SessionDontExistException):
            await ctx.send("You need to have open terminal to use this command")
