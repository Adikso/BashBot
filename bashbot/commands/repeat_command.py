from bashbot.commands import Command
from bashbot.commands.syntax import SyntaxBuilder
from bashbot.session_manager import SessionManager


class RepeatCommand(Command):
    def __init__(self):
        super().__init__()

        self.name = "Repeat input"
        self.aliases = [".repeat", ".r"]
        self.description = "Repeats string n times ands sends to current terminal"
        self.usage = ".repeat <n> <string..>"
        self.permission = "input.repeat"

        self.syntax = SyntaxBuilder()\
            .param("times")\
            .param("text", "repeat", multiple=True)\
        .build()

    async def repeat(self, client, message, parameters):
        session = SessionManager.get_session(message.channel)

        if session:
            session.send_input(parameters['text'] * int(parameters['times']))
        else:
            await client.send_message(message.channel, ":no_entry_sign: You are trying to send input to non-existing session")
