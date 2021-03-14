from discord import Embed
from discord.ext import commands
from discord.ext.commands import Context

from bashbot.constants import THUMBNAIL_URL, EMBED_COLOR, EMBED_COLOR_ERROR
from bashbot.core.settings import settings


class HelpCommand(commands.Cog):
    @commands.command(
        name='.help',
        description='This command'
    )
    async def help(self, ctx: Context, command_name=None):
        if command_name:
            await self._help_for_command(ctx, command_name)
        else:
            await self._help_all_commands(ctx)

    @staticmethod
    async def _help_for_command(ctx: Context, command_name):
        # Command does not exist
        if command_name not in ctx.bot.all_commands:
            embed = Embed(title=f'BashBot Help', description='Command does not exist', color=EMBED_COLOR_ERROR)
            await ctx.send(embed=embed)
            return

        # Command found, generate help message
        command = ctx.bot.all_commands[command_name]

        # Use brief help if full not found
        if command.description:
            description = command.description
        elif command.brief:
            description = command.brief
        else:
            description = '<<Missing description>>'

        embed = Embed(title=f'BashBot Help for {command_name}', description=description, color=EMBED_COLOR)
        embed.set_thumbnail(url=THUMBNAIL_URL)

        if command.usage:
            embed.add_field(name='Usage', value=f'{command_name} {command.usage}', inline=False)

        await ctx.send(embed=embed)

    @staticmethod
    async def _help_all_commands(ctx: Context):
        first_prefix = settings().get('commands.prefixes')[0]

        embed = Embed(title='BashBot Help', description=f'For more help type {first_prefix}.help [command]', color=EMBED_COLOR)
        embed.set_thumbnail(url=THUMBNAIL_URL)

        sorted_commands = sorted(ctx.bot.commands, key=lambda c: c.name)
        for command in sorted_commands:
            # Use full description if brief not found
            if command.brief:
                description = command.brief
            elif command.description:
                description = command.description
            else:
                description = '<<Missing description>>'

            usage = ' ' + command.usage if command.usage else ''
            embed.add_field(name=command.name + usage, value=description, inline=False)

        await ctx.send(embed=embed)
