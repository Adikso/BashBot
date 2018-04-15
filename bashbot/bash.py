# -*- coding: utf-8 -*-
import asyncio
import os
import sys
import threading

import pyte

from bashbot import bot


class BashSession:
    def __init__(self, terminal):
        self.name = None
        self.description = None
        self.status = "dead"
        self.controls = None

        self.message = None
        self.discord_client = None

        self.fd = None
        self.terminal = terminal
        self.stream = pyte.ByteStream(self.terminal)
        self.last_output = None
        self.new_update = True

    def open(self, loop):
        pid, self.fd = os.forkpty()
        if pid == 0:
            if bot.settings.get("user") and "login" in bot.settings.get("user") and bot.settings.get("user")["login"]:
                    os.execv(bot.settings.get("terminal")["su_path"],
                             [bot.settings.get("terminal")["su_path"], "-", bot.settings.get("user")["login"], "-s", bot.settings.get("terminal")["shell_path"]])
            else:
                os.execv(bot.settings.get("terminal")["shell_path"], [bot.settings.get("terminal")["shell_path"], ])

            sys.exit(0)
        else:
            self.status = "working"

            pty_output = threading.Thread(target=self.watch_output)
            pty_output.start()

            self.update_output(loop)

        return self

    def close(self):
        os.close(self.fd)
        print("Closed session #%s @ %s[%s]" % (self.name, self.message.channel.name, (
        self.message.channel.server.name if hasattr(self.message.channel, "server") else "PM")))

    def send_input(self, data):
        try:
            os.write(self.fd, self.replace_shortcuts(data).encode("utf-8"))
        except OSError:
            self.status = "broken"
            return

    @staticmethod
    def replace_shortcuts(command):
        d = {
            '[UP]': u'\u001b[A',
            '[DOWN]': u'\u001b[B',
            '[LEFT]': u'\u001b[D',
            '[RIGHT]': u'\u001b[C',
            '[ESC]': u'\u001b',
            '[TAB]': u'\u0009',
            '[T]': u'\u0009',
            '[F1]': u'\u001bOP',
            '[F2]': u'\u001bOQ',
            '[F3]': u'\u001bOR',
            '[F4]': u'\u001bOS',
            '[F5]': u'\u001b[15~',
            '[F6]': '',
            '[F7]': u'\u001b[18',
            '[F8]': u'\u001b[19~',
            '[F9]': u'\u001b[20~',
            '[F10]': u'\u001b[21~',
            '[F11]': u'\u001b[23~\u001b',
            '[F12]': u'\u001b[24~\u0008',
            '[<]': u'\u001b\u0005\u0015',  # ^E^U Clears input line
            '<ESC>': u'\u001b',
            '\\a': '\a',
            '\\b': '\b',
            '\\f': '\f',
            '\\n': '\n',
            '\\r': '\r',
            '\\t': '\t',
            '\\v': '\v'
        }

        d = {**d, **bot.settings.get("custom_shortcuts")}

        ctrl_chars = "@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\\]^_"

        for char in ctrl_chars:
            command = command.replace("^" + char, str(chr(ctrl_chars.index(char))))

        for initial, to in d.items():
            command = command.replace(initial, to)

        return command

    def update_output(self, loop):
        update_output = threading.Timer(
            int(bot.settings.get("terminal")["refresh"]),
            self.update_output,
            args=(loop,))

        update_output.start()

        if not self.last_output:
            return

        if self.status != "frozen" and self.new_update:
            self.send_output(loop)
            self.new_update = False

        if self.status == "broken":
            update_output.join()

    def send_output(self, loop):
        updated_message = bot.settings.get("terminal_template") % (
            self.name,
            self.status.title(),
            self.last_output)

        asyncio.set_event_loop(loop)
        asyncio.run_coroutine_threadsafe(
            self.discord_client.edit_message(
                self.message, updated_message),
            loop
        )

        self.message.content = updated_message

    def watch_output(self):
        try:
            output = os.read(self.fd, 1024)

            # Send init input when ready
            if bot.settings.get("user") and bot.settings.get("user")["password"]:
                self.send_input(bot.settings.get("user")["password"] + "\n")  # Login via su

            # Set init variables
            self.send_input("\n".join(bot.settings.get("terminal")["init"]) + "\n")

        except OSError:
            self.status = "broken"
            return

        while output:
            self.stream.feed(output.replace(b"(B", b""))

            message = "\n".join(self.terminal.display)
            self.last_output = message.replace("```", "'''")

            if bot.settings.get("show_cursor") == "true":
                characters = list(message)
                characters[self.terminal.cursor.y * message.index("\n") + self.terminal.cursor.x] = "█"
                self.last_output = "".join(characters)

            self.new_update = True

            try:
                output = os.read(self.fd, 1024)
            except OSError:
                self.status = "broken"
                return
