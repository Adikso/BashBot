from discord.ext import commands

from bashbot.command import has_permission
from bashbot.exceptions import SessionDontExistException
from bashbot.terminal.sessions import sessions
from bashbot.terminal.terminal import TerminalState


class FreezeCommand(commands.Cog):
    @commands.command(name='.freeze', aliases=['.f'])
    @has_permission('session.freeze')
    async def freeze(self, ctx, name=None):
        if name:
            terminal = sessions().get_by_name(name)
        else:
            terminal = sessions().get_by_channel(ctx.message.channel)

        if not terminal:
            raise SessionDontExistException()

        if terminal.state == TerminalState.FROZEN:
            terminal.state = TerminalState.OPEN
        elif terminal.state == TerminalState.OPEN:
            terminal.state = TerminalState.FROZEN

        terminal.refresh()
