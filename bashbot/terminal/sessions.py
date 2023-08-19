from discord import TextChannel, Message

from bashbot.core.factory import SingletonDecorator
from bashbot.core.settings import settings
from bashbot.terminal.terminal import Terminal
from bashbot.core.utils import parse_template, block_escape


class Sessions:
    def __init__(self):
        self.sessions = {}
        self.selected = {}

    def add(self, message: Message, terminal: Terminal):
        self.sessions[message] = terminal
        self.select(message.channel, terminal)

    def select(self, channel: TextChannel, terminal: Terminal):
        self.selected[channel] = terminal

    def by_channel(self, channel: TextChannel) -> Terminal:
        if channel in self.selected:
            return self.selected[channel]

    def by_message(self, searched_message: Message) -> Terminal:
        for message, terminal in self.sessions.items():
            if searched_message.id == message.id:
                return terminal

    def by_name(self, name: str) -> Terminal:
        for message, terminal in self.sessions.items():
            if terminal.name == name:
                return terminal

    def remove(self, terminal: Terminal):
        for k in self.sessions.copy():
            if self.sessions[k] == terminal:
                del self.sessions[k]

        message: Message = self.find_message(terminal)
        if message and message.channel in self.selected:
            self.selected.pop(message.channel)

    def find_message(self, terminal: Terminal):
        inv_map = {v: k for k, v in self.sessions.items()}
        return inv_map.get(terminal)

    async def update_message(self, terminal: Terminal, content: str):
        message = self.find_message(terminal)

        content = parse_template(
            settings().get('terminal.template'),
            name=terminal.name,
            state=terminal.state.name,
            content=block_escape(content)
        )

        await message.edit(content=content)


sessions = SingletonDecorator(Sessions)
