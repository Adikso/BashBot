import asyncio
import logging

from bashbot.core.settings import settings

loop = asyncio.get_event_loop()


def get_logger(name):
    logger = logging.getLogger(name)

    handler = logging.FileHandler('bashbot.log')
    formatter = logging.Formatter('[%(asctime)s] %(levelname)s:%(name)s: %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    return logger


def parse_template(template, **kwargs):
    for key, value in kwargs.items():
        template = template.replace('{' + key + '}', str(value))

    return template


def execute_async(method, *args, **kwargs):
    asyncio.run_coroutine_threadsafe(method(*args, **kwargs), loop)


def block_escape(text):
    return text.replace('```', '`‎`‎`')


def extract_prefix(content):
    for prefix in settings().get('commands.prefixes'):
        if content.startswith(prefix):
            return prefix


def remove_prefix(content):
    prefix = extract_prefix(content)
    if prefix:
        return content[len(prefix):]
    else:
        return content


def is_command(content):
    return any(content.startswith(prefix + '.') for prefix in settings().get('commands.prefixes'))
