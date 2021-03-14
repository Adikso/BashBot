from discord import User
from discord.ext import commands

from bashbot.core.settings import settings


class WhitelistCommand(commands.Cog):
    @commands.group(
        name='.whitelist',
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
            await ctx.send(f"Added user {user.mention} to whitelist")
        else:
            await ctx.send(f"User {user.mention} is already on the whitelist")

    @controls.command()
    async def remove(self, ctx, user: User):
        whitelist = settings().config['discord']['users_whitelist']
        if user.id in whitelist:
            whitelist.remove(user.id)
            settings().save()
            await ctx.send(f"Removed user {user.mention} from whitelist")
        else:
            await ctx.send(f"User {user.mention} is not on the whitelist")
