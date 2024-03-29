import logging

from discord import LoginFailure, Intents

from bashbot.bot import BashBot
from bashbot.core.settings import settings
from bashbot.core.state import state
from bashbot.core.utils import get_logger

logger = get_logger('Launcher')


def setup_logger():
    logging.basicConfig(
        level=logging.INFO,
        format='[%(asctime)s] %(levelname)s:%(name)s: %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )


def launch():
    setup_logger()
    settings().load()
    settings().load_macros()
    state().load()

    prefix = settings().get('commands.prefixes', ['$'])[0]
    token = settings().get('discord.token')

    if token == 'TOKEN_HERE':
        logger.error('You need to specify bot TOKEN in config.toml')
        return

    try:
        intents = Intents.default()
        intents.message_content = True
        BashBot(prefix, intents=intents).run(token)
    except LoginFailure as e:
        logger.error(e.args[0])


if __name__ == '__main__':
    launch()
