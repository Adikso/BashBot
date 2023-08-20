import json
from pathlib import Path

from bashbot.core.factory import SingletonDecorator
from bashbot.core.updater import Updater


class State(dict):
    def __init__(self):
        super().__init__()
        self.path = Path('state.json')

    def load(self):
        if self.path.is_file():
            with self.path.open() as source:
                self.update(json.load(source))
        else:
            self.update({
                'last_run_version': Updater.get_local_commit()
            })
            self.save()

    def save(self):
        with self.path.open('w') as source:
            json.dump(self, source, indent=2)


state = SingletonDecorator(State)
