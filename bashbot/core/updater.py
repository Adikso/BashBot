import json
import time
from datetime import datetime
from pathlib import Path

import requests

from bashbot.core.factory import SingletonDecorator
from bashbot.constants import REPOSITORY_AUTHOR, REPOSITORY_NAME, TIME_BETWEEN_UPDATE_CHECKS


class Updater:
    def __init__(self):
        self.last_check = None
        self.cached_updates = None

    def check_for_updates(self):
        current_time = int(time.time())
        if self.last_check and current_time - self.last_check < TIME_BETWEEN_UPDATE_CHECKS:
            return self.cached_updates

        latest_release = self.get_latest_release()
        if latest_release is None:
            return None

        local_commit_sha = self.get_local_commit()
        if latest_release['target_commitish'] != local_commit_sha:
            releases = self.get_new_releases(local_commit_sha)
            self.cached_updates = releases
            return releases

        return []

    @staticmethod
    def get_latest_release():
        api_url = f'https://api.github.com/repos/{REPOSITORY_AUTHOR}/{REPOSITORY_NAME}/releases/latest'
        r = requests.get(api_url)

        if r.status_code != 200:
            return None

        return r.json()

    @staticmethod
    def get_commit(commit_sha):
        api_url = f'https://api.github.com/repos/{REPOSITORY_AUTHOR}/{REPOSITORY_NAME}/commits/{commit_sha}'
        r = requests.get(api_url, headers={'X-GitHub-Api-Version': '2022-11-28'})

        if r.status_code != 200:
            return None

        return r.json()

    @staticmethod
    def get_new_releases(local_version):
        api_url = f'https://api.github.com/repos/{REPOSITORY_AUTHOR}/{REPOSITORY_NAME}/releases'
        r = requests.get(api_url, headers={'X-GitHub-Api-Version': '2022-11-28'})

        if r.status_code != 200:
            return None

        data = r.json()

        releases = []
        for release in data:
            if release['target_commitish'] == local_version:
                break
            releases.append(release)
        else:
            # Find updates if current local commit is not a part of a release
            releases = []
            commit = Updater.get_commit(local_version)
            commit_date = datetime.fromisoformat(commit['commit']['committer']['date'].replace('Z', '+00:00'))
            for release in data:
                release_date = datetime.fromisoformat(release['published_at'].replace('Z', '+00:00'))
                if release_date <= commit_date:
                    break
                releases.append(release)

        return releases

    @staticmethod
    def get_git_commit():
        try:
            with open('.git/HEAD', 'r') as file:
                ref = file.readline().split(": ")[1].rstrip()

            with open(f'.git/{ref}', 'r') as file:
                commit_hash = file.readline().rstrip()

            return commit_hash
        except FileNotFoundError:
            return None

    @staticmethod
    def get_local_commit():
        build_path = Path('build.json')
        if build_path.is_file():
            with build_path.open() as file:
                build_details = json.load(file)
                return build_details.get('version')

        git_commit = Updater.get_git_commit()
        if git_commit:
            return git_commit


updater = SingletonDecorator(Updater)
