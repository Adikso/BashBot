from discord import Embed
from discord.ext import commands
from discord.ext.commands import Context

from bashbot.constants import REPOSITORY_URL, THUMBNAIL_URL, EMBED_COLOR
from bashbot.core.settings import settings
from bashbot.core.updater import updater


class AboutCommand(commands.Cog):
    @commands.hybrid_command(
        name='about',
        aliases=['.about'],
        description='Shows information about project'
    )
    async def about(self, ctx: Context):
        embed = Embed(title='About BashBot', description='BashBot is a Discord bot that allows terminal access via chat.', color=EMBED_COLOR)
        embed.add_field(name='Source code', value=REPOSITORY_URL, inline=False)
        embed.add_field(name='Author', value='[Adikso](https://github.com/Adikso)', inline=False)
        embed.add_field(name='Current version', value=updater().get_local_commit(), inline=False)
        embed.set_thumbnail(url=THUMBNAIL_URL)

        if settings().get('other.check_for_updates'):
            releases = updater().check_for_updates()
            if releases is None:
                embed.add_field(name='Failed to fetch updates information', value='Try again later', inline=False)
            elif releases:
                embed.add_field(name='Updates available', value='\n'.join([f'- [{x["name"]}]({x["html_url"]})' for x in releases]), inline=False)
            else:
                embed.add_field(name='No updates available', value='BashBot is up to date', inline=False)
        else:
            embed.add_field(name='Updates check disabled', value='You can re-enable it via "other.check_for_updates" in the configuration file', inline=False)

        await ctx.send(embed=embed)
