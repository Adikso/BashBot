from discord.ext import commands

from bashbot.command import session_exists
from bashbot.core.exceptions import SessionDontExistException
from bashbot.terminal.sessions import sessions
from bashbot.terminal.terminal import TerminalState


class FreezeCommand(commands.Cog):
    @commands.command(
        name='.freeze',
        aliases=['.f'],
        description='Freezes current terminal session'
    )
    @session_exists()
    async def freeze(self, ctx):
        terminal = sessions().by_channel(ctx.message.channel)

        if not terminal:
            raise SessionDontExistException()

        if terminal.state == TerminalState.FROZEN:
            terminal.state = TerminalState.OPEN
        elif terminal.state == TerminalState.OPEN:
            terminal.state = TerminalState.FROZEN

        terminal.refresh()
        await ctx.send(f"`Changed terminal #{terminal.name} state to {terminal.state.name}`")
