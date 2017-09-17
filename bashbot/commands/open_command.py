import asyncio

from bashbot import bot
from bashbot.commands import Command
from bashbot.commands.syntax import SyntaxBuilder
from bashbot.session_manager import SessionManager


class OpenCommand(Command):
    def __init__(self):
        super().__init__()

        self.name = "Opens Session"
        self.aliases = [".open", ".o"]
        self.description = "Opens new terminal session"
        self.usage = ".open [name]"
        self.permission = "session.open"

        self.syntax = SyntaxBuilder() \
            .set_action("open") \
            .param("name", "open") \
        .build()

    async def open(self, client, message, parameters):
        loop = asyncio.get_event_loop()
        session_name = None

        if "name" in list(parameters.keys()):
            if not len(parameters["name"]) > 10:
                session_name = parameters["name"]
            else:
                await client.send_message(message.channel, ":no_entry_sign: Maximum length of session name is 10. Your is: %s" % len(parameters["name"]))
                return

        session = SessionManager.create_session(client, message, session_name)

        session.message = await client.send_message(
            message.channel,
            bot.settings.get("terminal_template") % (
                session.name,
                "Opening",
                "",
                "Waiting for tty..\n" + ((" " * 80) + "\n") * 23
            )
        )

        session.open(loop)
