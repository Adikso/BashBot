import os
import toml
from pathlib import Path

from bashbot.factory import SingletonDecorator


class Settings:
    DEFAULT_CONFIG_PATH = 'config.toml'
    DEFAULT_MACRO_PATH = 'macros'

    def __init__(self):
        self.config: dict = {}
        self.macros: dict = {}

    def load(self, path=DEFAULT_CONFIG_PATH):
        if os.path.exists(path):
            with open(path, 'r') as file:
                self.config = toml.load(file)

        # [commands]
        self.add_default('commands.prefixes', ['$', '.bash'])

        # [discord]
        self.add_default('discord.token', 'TOKEN_HERE')
        self.add_default('discord.presence', '{prefix}help')

        # [terminal]
        self.add_default('terminal.template', '`| TTY #{name} | {state} |`\n```{content}```')
        self.add_default('terminal.shell_path', '/bin/bash')
        self.add_default('terminal.su_path', '/bin/su')

        # [terminal.user]
        self.add_default('terminal.user.login_as_other_user', False)
        self.add_default('terminal.user.username', 'myuser')
        self.add_default('terminal.user.password', 'mypassword')

        self.save()

    def load_macros(self, path=DEFAULT_MACRO_PATH):
        os.makedirs(path, exist_ok=True)

        for filename in os.listdir(path):
            if filename.endswith('.txt'):
                self.macros[filename[:-4]] = Path(path + '/' + filename).read_text()

    def get(self, config_path, default=None):
        current_node = self.config

        # Follow dot path
        for node_name in config_path.split('.'):
            if node_name not in current_node.keys():
                return default

            current_node = current_node[node_name]

        return current_node or default

    def add_default(self, path, value):
        current_node = self.config
        parts = path.split('.')

        for node_name in parts[:-1]:
            if node_name not in current_node.keys():
                current_node[node_name] = {}

            current_node = current_node[node_name]

        if not parts[-1] in current_node:
            current_node[parts[-1]] = value

    def save(self, path=DEFAULT_CONFIG_PATH):
        with open(path, 'w') as file:
            toml.dump(self.config, file)


settings = SingletonDecorator(Settings)
