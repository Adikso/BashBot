import asyncio

from bashbot import bot
from bashbot.session_manager import SessionManager


def add_control(emoji, data, session):
    if not session.controls:
        session.controls = {}

    session.controls[emoji] = data

    asyncio.run_coroutine_threadsafe(
        session.discord_client.add_reaction(session.message, emoji),
        asyncio.get_event_loop()
    )


def remove_control(emoji, session):
    if not session.controls:
        return

    session.controls.pop(emoji)

    asyncio.run_coroutine_threadsafe(
        session.discord_client.clear_reactions(session.message),
        asyncio.get_event_loop()
    )

    for key in list(session.controls.items()):
        asyncio.run_coroutine_threadsafe(
            session.discord_client.add_reaction(session.message, key),
            asyncio.get_event_loop()
        )


def on_reaction_click(reaction, user):
    if user == bot.client.user:
        return

    session = SessionManager.get_by_message(reaction.message)

    if not session or not session.controls:
        return

    if reaction.emoji in session.controls:
        data = session.controls[reaction.emoji]
        session.send_input(data)

        print("%s @ %s[%s] [REACTION]: %s" % (user.name, reaction.message.channel.name,
                                   (reaction.message.channel.server.name if hasattr(reaction.message.channel, "server") else "PM"),
                                   data.encode("utf-8")))
