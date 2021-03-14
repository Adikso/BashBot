import os
import pty
import subprocess

from discord.ext import commands

from bashbot.core.settings import settings


class ExecCommand(commands.Cog):
    @commands.command(
        name='.exec',
        aliases=['.e'],
        description='Execute single command',
        usage='<command...>'
    )
    async def exec(self, ctx, *, command):
        shell_path = settings().get('terminal.shell_path')

        login_as_other_user = settings().get('terminal.user.login_as_other_user')
        if login_as_other_user:
            su_path = settings().get('terminal.su_path')

            login = settings().get('terminal.user.username')
            password = settings().get('terminal.user.password')

            master, slave = pty.openpty()
            subprocess.Popen([su_path, "-", login, "-s", shell_path, '-c', command], stdin=slave, stdout=slave, stderr=slave, universal_newlines=True)
            os.read(master, 10240)  # ignore prompt
            os.write(master, f'{password}\n'.encode())
            os.read(master, 10240)  # ignore empty line
            output = os.read(master, 10240).rstrip().decode('utf-8')

            os.close(master)
            os.close(slave)
        else:
            output = subprocess.check_output(
                [shell_path, '-c', command],
                universal_newlines=True,
            )

        await ctx.send(output)
