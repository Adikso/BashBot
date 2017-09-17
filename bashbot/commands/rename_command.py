import asyncio

from bashbot.commands import Command
from bashbot.commands.syntax import SyntaxBuilder
from bashbot.session_manager import SessionManager


class RenameCommand(Command):
    def __init__(self):
        super().__init__()

        self.name = "Rename terminal"
        self.aliases = [".rename"]
        self.description = "Renames terminal session"
        self.usage = ".rename <new_name>"
        self.permission = "session.rename"

        self.syntax = SyntaxBuilder() \
            .param("new_name", "rename") \
        .build()

    async def rename(self, client, message, parameters):
        session = SessionManager.get_session(message.channel)

        if session:
            if not len(parameters["new_name"]) > 20:
                session.name = parameters["new_name"]
            else:
                await client.send_message(message.channel, ":no_entry_sign: Maximum length of session name is 20. Your is: %s" % len(parameters["name"]))
                return

            session.send_output(asyncio.get_event_loop())
        else:
            await client.send_message(message.channel, ":no_entry_sign: You are trying to freeze non-existing session")
