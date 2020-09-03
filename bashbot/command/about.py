from discord.ext import commands
from discord.ext.commands import Context

from bashbot.command import has_permission


class AboutCommand(commands.Cog):
    @commands.command(name='.about', description='Shows information about project')
    @has_permission('info.about')
    async def about(self, ctx: Context):
        await ctx.send("__**About me**__\n"
                       "BashBot is a Discord bot that allows terminal access via chat.\n"
                       "**Github**: https://github.com/Adikso/BashBot\n"
                       "**Author**: Adikso.")
