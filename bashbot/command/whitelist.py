from discord import User, Embed
from discord.ext import commands

from bashbot.core.settings import settings


class WhitelistCommand(commands.Cog):
    @commands.hybrid_group(
        name='whitelist',
        aliases=['.whitelist'],
        description='Manages users whitelist',
        usage='add/remove <user_tag>'
    )
    async def controls(self, ctx):
        if ctx.invoked_subcommand is None:
            pass

    @controls.command()
    async def add(self, ctx, user: User):
        whitelist = settings().config['discord']['users_whitelist']
        if user.id not in whitelist:
            whitelist.append(user.id)
            settings().save()

            embed = Embed(description=f"Added user {user.mention} to whitelist", color=0x00ff00)
            await ctx.send(embed=embed)
        else:
            embed = Embed(description=f"User {user.mention} is already on the whitelist", color=0xff0000)
            await ctx.send(embed=embed)

    @controls.command()
    async def remove(self, ctx, user: User):
        whitelist = settings().config['discord']['users_whitelist']
        if user.id in whitelist:
            whitelist.remove(user.id)
            settings().save()
            embed = Embed(description=f"Removed user {user.mention} from whitelist", color=0x00ff00)
            await ctx.send(embed=embed)
        else:
            embed = Embed(description=f"User {user.mention} is not on the whitelist", color=0xff0000)
            await ctx.send(embed=embed)
