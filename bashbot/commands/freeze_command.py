import asyncio

from bashbot.commands import Command
from bashbot.commands.syntax import SyntaxBuilder
from bashbot.session_manager import SessionManager


class FreezeCommand(Command):
    def __init__(self):
        super().__init__()

        self.name = "Freeze terminal"
        self.aliases = [".freeze", ".f"]
        self.description = "Freezes terminal session"
        self.usage = ".freeze [name]"
        self.permission = "session.freeze"

        self.syntax = SyntaxBuilder() \
            .set_action("freeze") \
            .param("name", "freeze") \
        .build()

    async def freeze(self, client, message, parameters):
        session = SessionManager.get_session(message.channel)

        if session:
            if session.status == "frozen":
                session.status = "working"
            else:
                session.status = "frozen"

            session.send_output(asyncio.get_event_loop())
        else:
            await client.send_message(message.channel, ":no_entry_sign: You are trying to freeze non-existing session")
