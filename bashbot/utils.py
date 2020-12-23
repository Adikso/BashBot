import asyncio
import logging
import time

import requests

from bashbot.constants import REPOSITORY_AUTHOR, REPOSITORY_NAME, REPOSITORY_BRANCH
from bashbot.settings import settings

loop = asyncio.get_event_loop()
last_check = int(time.time())


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


def check_update(rate_limit=True):
    global last_check

    current_time = int(time.time())
    if rate_limit and current_time - last_check < 600:
        return False

    last_check = current_time

    try:
        api_url = f'https://api.github.com/repos/{REPOSITORY_AUTHOR}/{REPOSITORY_NAME}/branches/{REPOSITORY_BRANCH}'
        r = requests.get(api_url)

        if r.status_code != 200:
            return False

        data = r.json()
        if data.commit.sha != current_commit():
            return {
                'sha': data.commit.sha,
                'message': data.commit.commit.message
            }

        return None
    except:
        # Just in case
        return False


def current_commit():
    try:
        with open('.git/HEAD', 'r') as file:
            ref = file.readline().split(": ")[1].rstrip()

        with open(f'.git/{ref}', 'r') as file:
            commit_hash = file.readline().rstrip()

        return commit_hash
    except FileNotFoundError:
        return None


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
