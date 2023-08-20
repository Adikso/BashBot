from discord import Message, Status, Game, DMChannel, Embed, Interaction, InteractionType
from discord.abc import PrivateChannel
from discord.ext.commands import Bot, Context
from discord.ui import View, Button
from discord.utils import oauth_url

from bashbot.command.about import AboutCommand
from bashbot.command.exec import ExecCommand
from bashbot.command.close import CloseCommand
from bashbot.command.controls import ControlsCommand
from bashbot.command.freeze import FreezeCommand
from bashbot.command.here import HereCommand
from bashbot.command.interactive import InteractiveCommand
from bashbot.command.macro import MacroCommand
from bashbot.command.open import OpenCommand
from bashbot.command.rename import RenameCommand
from bashbot.command.repeat import RepeatCommand
from bashbot.command.select import SelectCommand
from bashbot.command.submit import SubmitCommand
from bashbot.command.help import HelpCommand
from bashbot.command.whitelist import WhitelistCommand
from bashbot.core.exceptions import SessionDontExistException, ArgumentFormatException, TerminalNotFoundException, \
    MacroNotFoundException
from bashbot.core.settings import settings
from bashbot.core.state import state
from bashbot.terminal.sessions import sessions
from bashbot.terminal.terminal import TerminalState
from bashbot.core.updater import updater, Updater
from bashbot.core.utils import get_logger, parse_template, extract_prefix, is_command, remove_prefix


class BashBot(Bot):
    logger = get_logger('BashBot')
    cmd_logger = get_logger('Command')

    async def setup_hook(self):
        await self.add_cog(OpenCommand())
        await self.add_cog(CloseCommand())
        await self.add_cog(HereCommand())
        await self.add_cog(FreezeCommand())
        await self.add_cog(RenameCommand())
        await self.add_cog(ControlsCommand())
        await self.add_cog(AboutCommand())
        await self.add_cog(RepeatCommand())
        await self.add_cog(MacroCommand())
        await self.add_cog(SelectCommand())
        await self.add_cog(InteractiveCommand())
        await self.add_cog(SubmitCommand())
        await self.add_cog(ExecCommand())
        await self.add_cog(WhitelistCommand())

        self.remove_command("help")
        await self.add_cog(HelpCommand())

    async def on_ready(self):
        if state()['last_run_version'] != Updater.get_local_commit():
            self.logger.info('Synchronizing command tree...')
            await self.tree.sync()
            self.logger.info('Command tree synchronized')

        self.__check_for_updates()

        self.logger.info(f'Logged in as {self.user.name} ({self.user.id})')
        self.logger.info(f'You can add bot to your server via {oauth_url(self.user.id)}')

        presence = parse_template(
            settings().get("discord.presence"),
            prefix=self.command_prefix
        )
        await self.change_presence(
            status=Status.online,
            activity=Game(presence)
        )

    def __check_for_updates(self):
        if settings().get('other.check_for_updates'):
            self.logger.info(f'Checking for updates...')

            releases = updater().check_for_updates()
            if releases is None:
                self.logger.info(f'Failed to fetch updates information')
            elif releases:
                self.logger.info(
                    f'New updates available. Try running `git pull`. \n' +
                    '\n'.join([f'- {x["name"]} ({x["html_url"]})' for x in releases])
                )
            else:
                self.logger.info(f'BashBot is up to date')

    async def check_permissions(self, message):
        is_owner = await self.is_owner(message.author)
        if not is_owner:
            if settings().get('discord.enable_users_whitelist'):
                users_whitelist = settings().get('discord.users_whitelist', [])

                if message.author.id not in users_whitelist:
                    first_prefix = settings().get('commands.prefixes')[0]
                    embed = Embed(
                        title=f'Only whitelisted users can execute commands',
                        description=f'{first_prefix}.whitelist add {message.author.mention}'
                    )

                    await message.channel.send(embed=embed)
                    return False

            if isinstance(message.channel, DMChannel) and settings().get('discord.disable_dm'):
                embed = Embed(
                    title=f'Using bot on DM is disabled',
                    description='discord.disable_dm = true'
                )

                await message.channel.send(embed=embed)
                return False

        return True

    async def on_message(self, message: Message):
        if message.author.bot:
            return

        terminal = sessions().by_channel(message.channel)

        if self.is_invoke(message):
            if not await self.check_permissions(message):
                return

            await self.process_commands(message)
        elif terminal and terminal.state == TerminalState.OPEN:
            prefix = extract_prefix(message.content)
            if not terminal.interactive and not prefix:
                return

            if not await self.check_permissions(message):
                return

            # We don't remove prefix when in interactive mode
            content = message.content
            if not terminal.interactive:
                content = remove_prefix(content)

            if terminal.auto_submit:
                content += '\n'

            terminal.send_input(content)

            # Log message
            guild_name = message.channel.guild.name
            channel_name = message.channel.name
            author_name = message.author.name
            self.cmd_logger.info(f"[{guild_name}/#{channel_name}/{terminal.name}] {author_name} typed: {content}")

            should_delete_any = settings().get('terminal.delete_messages')
            should_delete_interactive = settings().get('terminal.interactive.delete_messages')
            if should_delete_any or (should_delete_interactive and terminal.interactive):
                await message.delete()

    async def on_interaction(self, interaction: Interaction):
        if interaction.type != InteractionType.component:
            return

        terminal = sessions().by_message(interaction.message)

        label = interaction.data['custom_id']
        if label.startswith('control_') and not terminal:
            await interaction.response.send_message(content='This terminal is unavailable', ephemeral=True)
            view = View.from_message(interaction.message)
            for component in view.children:
                if isinstance(component, Button):
                    component.disabled = True

            await interaction.message.edit(view=view)
            terminal.state = TerminalState.BROKEN
            terminal.refresh()

    async def on_command(self, ctx: Context):
        if not isinstance(ctx.message.channel, DMChannel):
            guild_name = ctx.message.channel.guild.name
            channel_name = ctx.message.channel.name
        else:
            guild_name = 'DM'
            channel_name = 'DM'

        author_name = ctx.message.author.name
        content = ctx.message.content

        self.cmd_logger.info(f"[{guild_name}/#{channel_name}] {author_name} invoked command: {content}")

    async def on_command_error(self, ctx: Context, error):
        message = None

        if isinstance(error, ArgumentFormatException):
            message = error.message

        if isinstance(error, SessionDontExistException):
            message = error.message

        if isinstance(error, TerminalNotFoundException):
            message = error.message

        if isinstance(error, MacroNotFoundException):
            message = error.message

        if message:
            await ctx.send(f'`{message}`')

    def is_invoke(self, message: Message):
        if isinstance(message.channel, PrivateChannel):
            return True

        has_mention = self.user in message.mentions
        return is_command(message.content) or has_mention
