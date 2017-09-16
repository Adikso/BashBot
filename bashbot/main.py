from bashbot import bot


def main(installed=True):
    if installed:
        bot.settings.copy_default(True)
        bot.permissions.copy_default(True)
    else:
        bot.settings.load()
        bot.permissions.load()

    bot.register_commands()
    bot.connect()
