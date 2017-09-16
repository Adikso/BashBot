import asyncio

from bashbot.commands import Command
from bashbot.commands.syntax import SyntaxBuilder
from bashbot.permissions import has_permission
from bashbot.session_manager import SessionManager


class SessionsCommand(Command):
    def __init__(self):
        super().__init__()

        self.name = "Sessions list"
        self.aliases = [".sessions", ".session"]
        self.description = "Manages sessions"
        self.usage = ".sessions\n.sessions kill <name>\n.sessions killall"
        self.permission = "session.list"

        self.syntax = SyntaxBuilder() \
            .set_action("list") \
            .action("killall", "killall") \
            .parent() \
            .node("kill") \
            .param("name", "kill") \
        .build()

    async def list(self, client, message, parameters):
        sessions_list = "**Active Sessions:**\n\n"

        if len(SessionManager.sessions) == 0:
            sessions_list += "There are no active sessions"

        for session in SessionManager.sessions:
            channel_name = None
            if session in SessionManager.selected_sessions.values():
                channel_name = list(SessionManager.selected_sessions.keys())[list(SessionManager.selected_sessions.values()).index(session)].name

            sessions_list += """**#%s**
        status: %s
        description: %s
        channel: %s
""" % (session.name, session.status, session.description, channel_name)

        await client.send_message(message.channel, sessions_list)

    async def killall(self, client, message, parameters):
        if has_permission("session.killall", message.author, message.channel):
            for session in SessionManager.sessions:
                SessionManager.delete_session(session)

            await client.send_message(message.channel, "Killed all sessions")
        else:
            await client.send_message(message.channel, ":lock: You don't have permission to use this command")

    async def kill(self, client, message, parameters):
        if has_permission("session.kill", message.author, message.channel):
            session = SessionManager.get(parameters["name"])

            if session:
                session.status = "killed"
                session.send_output(asyncio.get_event_loop())
                SessionManager.delete_session(session)

                await client.send_message(message.channel, "Session killed")
            else:
                await client.send_message(message.channel, ":no_entry_sign: You are trying to close non-existing session")
        else:
            await client.send_message(message.channel, ":lock: You don't have permission to use this command")