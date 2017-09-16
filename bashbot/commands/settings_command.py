from bashbot import bot
from bashbot.commands import Command
from bashbot.commands.syntax import SyntaxBuilder


class SettingsCommand(Command):

    protected_settings = ["token", "_user"]

    def __init__(self):
        super().__init__()

        self.name = "Manage settings"
        self.aliases = [".settings", ".setting"]
        self.description = "Get/Set bot settings"
        self.usage = ".settings <name> [value]\n.settings save"
        self.permission = "internal.settings"

        self.syntax = SyntaxBuilder()\
            .set_action("all") \
            .action("save", "save") \
            .parent()\
                .param("name", "get") \
                .param("value", "set") \
        .build()

    async def get(self, client, message, parameters):
        if parameters["name"] in self.protected_settings:
            await client.send_message(message.channel, "This setting is protected")
            return

        await client.send_message(message.channel,
                                  "**Key** = %s \n**Value** = %s" %
                                  (
                                      parameters["name"],
                                      bot.settings.get(parameters["name"]))
                                  )

    async def set(self, client, message, parameters):
        if parameters["name"] in self.protected_settings:
            await client.send_message(message.channel, "This setting is protected")
            return

        bot.settings.set(parameters["name"], parameters["value"])
        await client.send_message(message.channel, "Successfully set `%s` value" % parameters["name"])

    async def save(self, client, message, parameters):
        bot.settings.save()
        await client.send_message(message.channel, "Settings saved to file")

    async def all(self, client, message, parameters):
        all_settings = "**Settings list:**\n\n"

        for key, value in bot.settings.settings.items():
            if key not in self.protected_settings:
                all_settings += (":black_small_square: %s = %s" % (key, value)).replace("`", "'").replace("\n", "\\n") + "\n"

        await client.send_message(message.channel, all_settings)
