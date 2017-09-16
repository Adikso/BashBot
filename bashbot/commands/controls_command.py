from bashbot.commands import Command
from bashbot.commands.syntax import SyntaxBuilder
from bashbot.controls import add_control, remove_control
from bashbot.session_manager import SessionManager


class ControlsCommand(Command):
    def __init__(self):
        super().__init__()

        self.name = "Manage Controls"
        self.aliases = [".controls"]
        self.description = "Manages terminal controls"
        self.usage = ".controls add/remove [emoji] [content..]"
        self.permission = "input.controls.manage"

        self.syntax = SyntaxBuilder() \
            .set_action("show") \
            .node("add") \
            .param("emoji_id") \
            .param("content", action="add", multiple=True) \
            .parent().parent().parent() \
            .node("remove") \
            .param("emoji_id", action="remove") \
            .build()

    async def add(self, client, message, parameters):
        session = SessionManager.get_session(message.channel)

        if session:
            add_control(parameters["emoji_id"], parameters["content"], session)
        else:
            await client.send_message(message.channel, ":no_entry_sign: You are trying to add controls to non-existing session")

    async def remove(self, client, message, parameters):
        session = SessionManager.get_session(message.channel)

        if session:
            remove_control(parameters["emoji_id"], session)
        else:
            await client.send_message(message.channel, ":no_entry_sign: You are trying to add controls to non-existing session")

    async def show(self, client, message, parameters):
        session = SessionManager.get_session(message.channel)
        controls = ""

        if session:
            for key, value in list(session.controls.items()):
                controls += "%s = %s\n" % (key, value)

            await client.send_message(message.channel, controls)
        else:
            await client.send_message(message.channel, ":no_entry_sign: You are trying to show controls of non-existing session")
