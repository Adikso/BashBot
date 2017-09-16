import asyncio

import pyte

from bashbot import bash


class SessionManager:
    sessions = []
    last_number = 0
    selected_sessions = {}

    @staticmethod
    def create_session(client, message, name=None):
        if not name:
            SessionManager.last_number += 1
            name = SessionManager.last_number

        screen = pyte.Screen(80, 24)

        session = bash.BashSession(screen)
        session.name = name
        session.discord_client = client

        SessionManager.sessions.append(session)
        SessionManager.select(session, message.channel)

        print("Created session #%s @ %s[%s]" % (
            session.name,
            message.channel.name,
              (
                message.channel.server.name if hasattr(message.channel, "server") else "PM"))
              )

        return session

    @staticmethod
    def get(name):
        for session in SessionManager.sessions:
            if str(session.name) == str(name):
                return session

        return None

    @staticmethod
    def get_by_message(message):
        for session in SessionManager.sessions:
            if session.message.id == message.id:
                return session

        return None

    @staticmethod
    def select(session, channel):
        if isinstance(session, str):
            session = SessionManager.get(session)

        last_session = SessionManager.get_session(channel)

        if last_session:
            last_session.send_output(asyncio.get_event_loop())

        SessionManager.set_session(session, channel)
        session.status = "selected"
        return session

    @staticmethod
    def get_session(channel):
        if channel not in list(SessionManager.selected_sessions.keys()):
            return None

        return SessionManager.selected_sessions[channel]

    @staticmethod
    def set_session(session, channel):
        SessionManager.selected_sessions[channel] = session

    @staticmethod
    def delete_session(session):
        session.close()
        SessionManager.selected_sessions.pop(session.message.channel)
        SessionManager.sessions.pop(SessionManager.sessions.index(session))
