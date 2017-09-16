from bashbot.commands import Command
from bashbot.commands.syntax import SyntaxBuilder
from bashbot.session_manager import SessionManager


class SelectCommand(Command):
    def __init__(self):
        super().__init__()

        self.name = "Select terminal"
        self.aliases = [".select", ".s"]
        self.description = "Sets terminal as selected"
        self.usage = ".select [name]"
        self.permission = "session.select"

        self.syntax = SyntaxBuilder()\
            .param("name", "select")\
        .build()

    async def select(self, client, message, parameters):
        SessionManager.select(parameters["name"], message.channel)
