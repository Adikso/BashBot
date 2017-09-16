import json

import os
from pathlib import Path

import pkg_resources


class Settings:

    def __init__(self, filename):
        self.settings = {}
        self.filename = filename

    def get(self, key):
        if key not in list(self.settings.keys()):
            return None

        return self.settings[key]

    def set(self, key, value):
        self.settings[key] = value

    def load(self, filename=None):
        try:
            settings_file = open(filename if filename else self.filename, "r")
            self.settings = json.loads(settings_file.read())
            settings_file.close()
        except (OSError, IOError):
            print("Failed to load settings %s" % (filename if filename else self.filename))
            self.copy_default(home=False)
            return

        print("Loaded `%s`" % self.filename)

    def save(self, filename=None):
        try:
            settings_file = open(filename if filename else self.filename, "w+")

            for key in list(self.settings.keys()):
                if key.startswith("_"):
                    self.settings.pop(key, None)

            settings_file.write(json.dumps(self.settings, sort_keys=True, indent=4, separators=(',', ': ')))
            settings_file.close()
        except (OSError, IOError):
            print("Failed to write settings to file %s" % (filename if filename else self.filename))
            return False

        print("Saved `%s`" % self.filename)

        return True

    def copy_default(self, home):
        if home:
            self.settings = json.loads(pkg_resources.resource_string('bashbot', self.filename.replace(".json", ".default.json")))
            self.filename = os.path.join(str(Path.home()), ".bashbot", self.filename)

            if not os.path.exists(self.filename):
                self.create_home_dir()
                self.save()
        else:
            self.load(os.path.join("bashbot", self.filename.replace(".json", ".default.json")))
            self.save()

    def create_home_dir(self):
        os.makedirs(os.path.dirname(self.filename), exist_ok=True)
