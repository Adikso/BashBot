import asyncio

from bashbot.commands import Command
from bashbot.commands.syntax import SyntaxBuilder
from bashbot.session_manager import SessionManager


class TitleCommand(Command):
    def __init__(self):
        super().__init__()

        self.name = "Set terminal title"
        self.aliases = [".title", ".t"]
        self.description = "Sets terminal title"
        self.usage = ".title <title..>"
        self.permission = "session.title"

        self.syntax = SyntaxBuilder() \
            .param("title", "title", multiple=True) \
        .build()

    async def title(self, client, message, parameters):
        session = SessionManager.get_session(message.channel)

        if session:
            if not len(parameters["title"]) > 20:
                session.description = parameters["title"].replace("`", "'")
                session.send_output(asyncio.get_event_loop())
            else:
                await client.send_message(message.channel, ":no_entry_sign: Maximum length of title is 20. Your is: %s" % len(parameters["title"]))
        else:
            await client.send_message(message.channel, ":no_entry_sign: You are trying to title non-existing session")
