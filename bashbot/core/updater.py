import time
import requests

from bashbot.core.factory import SingletonDecorator
from bashbot.constants import REPOSITORY_AUTHOR, REPOSITORY_NAME, REPOSITORY_BRANCH, TIME_BETWEEN_UPDATE_CHECKS


class Updater:
    def __init__(self):
        self.last_check = None
        self.last_update = None

    def check_for_updates(self, rate_limit=True):
        current_time = int(time.time())
        if rate_limit and self.last_check and current_time - self.last_check < TIME_BETWEEN_UPDATE_CHECKS:
            return self.last_update

        self.last_check = current_time
        upstream_commit = self.get_upstream_commit()
        local_commit_sha = self.get_local_commit()

        if upstream_commit['sha'] != local_commit_sha:
            self.last_update = upstream_commit
            return upstream_commit

        return self.last_update

    @staticmethod
    def get_upstream_commit():
        api_url = f'https://api.github.com/repos/{REPOSITORY_AUTHOR}/{REPOSITORY_NAME}/branches/{REPOSITORY_BRANCH}'
        r = requests.get(api_url)

        if r.status_code != 200:
            return None

        data = r.json()
        return {
            'sha': data['commit']['sha'],
            'message': data['commit']['commit']['message']
        }

    @staticmethod
    def get_local_commit():
        try:
            with open('.git/HEAD', 'r') as file:
                ref = file.readline().split(": ")[1].rstrip()

            with open(f'.git/{ref}', 'r') as file:
                commit_hash = file.readline().rstrip()

            return commit_hash
        except FileNotFoundError:
            return None


updater = SingletonDecorator(Updater)
