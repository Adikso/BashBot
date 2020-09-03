from discord import TextChannel, Message

from bashbot.factory import SingletonDecorator
from bashbot.settings import settings
from bashbot.terminal.terminal import Terminal
from bashbot.utils import execute_async, parse_template, block_escape


class Sessions:
    def __init__(self):
        self.sessions = {}

    def add(self, message: Message, terminal: Terminal):
        self.sessions[message] = terminal

    def get_by_channel(self, channel: TextChannel) -> Terminal:
        for message, terminal in self.sessions.items():
            if message.channel == channel:
                return terminal

    def get_by_message(self, searched_message: Message) -> Terminal:
        for message, terminal in self.sessions.items():
            if searched_message.id == message.id:
                return terminal

    def get_by_name(self, name: str) -> Terminal:
        for message, terminal in self.sessions.items():
            if terminal.name == name:
                return terminal

    def remove(self, terminal: Terminal):
        for k in self.sessions.copy():
            if self.sessions[k] == terminal:
                del self.sessions[k]

    def get_message(self, terminal: Terminal):
        inv_map = {v: k for k, v in self.sessions.items()}
        return inv_map.get(terminal)

    def update_message(self, terminal: Terminal, content: str):
        message = self.get_message(terminal)

        content = parse_template(
            settings().get('terminal.template'),
            name=terminal.name,
            state=terminal.state.name,
            content=block_escape(content)
        )

        execute_async(message.edit, content=content)


sessions = SingletonDecorator(Sessions)
