import asyncio
import logging

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


def check_update():
    return False


def block_escape(text):
    return text.replace('```', '`‎`‎`')
