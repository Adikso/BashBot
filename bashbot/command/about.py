from discord import Embed
from discord.ext import commands
from discord.ext.commands import Context

from bashbot.constants import REPOSITORY_URL, REPOSITORY_AUTHOR, THUMBNAIL_URL, EMBED_COLOR
from bashbot.core.settings import settings
from bashbot.core.updater import updater


class AboutCommand(commands.Cog):
    @commands.command(
        name='.about',
        description='Shows information about project'
    )
    async def about(self, ctx: Context):
        embed = Embed(title='About BashBot', description='BashBot is a Discord bot that allows terminal access via chat.', color=EMBED_COLOR)
        embed.add_field(name='Github', value=REPOSITORY_URL, inline=False)
        embed.add_field(name='Author', value=REPOSITORY_AUTHOR, inline=False)
        embed.add_field(name='Current version', value=updater().get_local_commit(), inline=False)
        embed.set_thumbnail(url=THUMBNAIL_URL)

        if settings().get('other.check_for_updates'):
            update_details = updater().check_for_updates()
            if update_details:
                embed.add_field(name='New update available', value=f'"{update_details["message"]}"\n{update_details["sha"]}', inline=False)
            else:
                embed.add_field(name='No updates available', value='BashBot is up to date', inline=False)

        await ctx.send(embed=embed)
