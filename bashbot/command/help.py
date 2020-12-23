from discord import Embed
from discord.ext import commands
from discord.ext.commands import Context

from bashbot.command import has_permission
from bashbot.settings import settings


class HelpCommand(commands.Cog):
    REPOSITORY_URL = 'https://github.com/Adikso/BashBot'
    THUMBNAIL_URL = 'https://cdn.discordapp.com/avatars/258638578798559233/8a50a65e7bfaf661d01db9ca2b617748.png'
    
    @commands.command(
        name='.help',
        description='This command'
    )
    @has_permission('help')
    async def help(self, ctx: Context, command_name=None):
        if command_name:
            await self._help_for_command(ctx, command_name)
        else:
            await self._help_all_commands(ctx)

    async def _help_for_command(self, ctx: Context, command_name):
        # Command does not exist
        if command_name not in ctx.bot.all_commands:
            embed = Embed(title=f'BashBot Help', description='Command does not exist', color=0xff0000)
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

        embed = Embed(title=f'BashBot Help for {command_name}', description=description, color=0x327ef7)
        embed.set_thumbnail(url=self.THUMBNAIL_URL)

        if command.usage:
            embed.add_field(name='Usage', value=f'{command_name} {command.usage}', inline=False)

        await ctx.send(embed=embed)

    async def _help_all_commands(self, ctx: Context):
        first_prefix = settings().get('commands.prefixes')[0]

        embed = Embed(title='BashBot Help', description=f'For more help type {first_prefix}.help [command]', color=0x327ef7)
        embed.set_thumbnail(url=self.THUMBNAIL_URL)

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

        embed.set_footer(text=f'Check for updates at {self.REPOSITORY_URL}')
        await ctx.send(embed=embed)
