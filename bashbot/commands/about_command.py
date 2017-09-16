from bashbot.commands import Command
from bashbot.commands.syntax import SyntaxBuilder


class AboutCommand(Command):
    def __init__(self):
        super().__init__()

        self.name = "About command"
        self.aliases = [".about"]
        self.description = "Shows information about project"
        self.usage = ".about"
        self.permission = "info.about"

        self.syntax = SyntaxBuilder() \
            .set_action("about") \
            .build()

    async def about(self, client, message, parameters):
        about_msg = """
__**About me**__

BashBot is a Discord bot that allows terminal access via chat.

**Github**: https://github.com/Adikso/BashBot
**Author**: Adikso.
                        """
        await client.send_message(message.channel, about_msg)
