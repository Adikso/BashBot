import logging

from discord import LoginFailure

from bashbot.bot import BashBot
from bashbot.settings import settings
from bashbot.utils import get_logger

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

    prefix = settings().get('commands.prefixes', ['$'])[0]
    token = settings().get('discord.token')

    if token == 'TOKEN_HERE':
        logger.error('You need to specify bot TOKEN in config.toml')
        return

    try:
        BashBot(prefix).run(token)
    except LoginFailure as e:
        logger.error(e.args[0])


if __name__ == '__main__':
    launch()
