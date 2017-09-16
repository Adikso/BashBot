from bashbot.commands import Command
from bashbot.commands.syntax import SyntaxBuilder
from bashbot.session_manager import SessionManager


class CloseCommand(Command):
    def __init__(self):
        super().__init__()

        self.name = "Close terminal"
        self.aliases = [".close", ".c"]
        self.description = "Closes terminal session"
        self.usage = ".close [name]"
        self.permission = "session.close"

        self.syntax = SyntaxBuilder() \
            .set_action("close") \
            .param("name", "close") \
            .build()

    async def close(self, client, message, parameters):
        session = SessionManager.get_session(message.channel)

        if session:
            await client.delete_message(session.message)
            SessionManager.delete_session(session)
        else:
            await client.send_message(message.channel, ":no_entry_sign: You are trying to close non-existing session")
