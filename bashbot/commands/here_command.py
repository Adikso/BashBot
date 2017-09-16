from bashbot.commands import Command
from bashbot.commands.syntax import SyntaxBuilder
from bashbot.session_manager import SessionManager


class HereCommand(Command):
    def __init__(self):
        super().__init__()

        self.name = "Move Terminal Here"
        self.aliases = [".here", ".h"]
        self.description = "Moves selected terminal below the user message"
        self.usage = ".here"
        self.permission = "session.move"

        self.syntax = SyntaxBuilder()\
            .set_action("move")\
        .build()

    async def move(self, client, message, parameters):
        session = SessionManager.get_session(message.channel)

        if session:
            await client.delete_message(session.message)
            session.message = await client.send_message(message.channel, session.message.content)
        else:
            await client.send_message(message.channel, ":no_entry_sign: You are trying to move non-existing session")

