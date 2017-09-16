from bashbot import bot
from bashbot.commands import Command
from bashbot.commands.syntax import SyntaxBuilder


class HelpCommand(Command):
    def __init__(self):
        super().__init__()

        self.name = "Help command"
        self.aliases = [".help"]
        self.description = "Shows help"
        self.usage = ".help [name]"
        self.allowed_private = True
        self.permission = "info.help"

        self.syntax = SyntaxBuilder() \
            .set_action("show_help") \
            .param("command_name", "show_help") \
        .build()

    async def show_help(self, client, message, parameters):
        if "command_name" not in list(parameters.keys()):
            commands_list = ""

            for command in bot.commands_manager.commands:
                commands_list += ":black_small_square: **%s** - %s\n" % (command.aliases[0], command.description)

            help_msg = """
__**List of commands**__
            
%s
            
**Prefix commands with**: %s or tag me
**Example**:
%s.select 2
@%s .open

In order to send command to terminal session type:
`%shelp\\n`
            
Use `@%s .help <command>` to get more information about the command
            """ % (
                commands_list,
                " or ".join(bot.settings.get("prefixes")),
                bot.settings.get("prefixes")[0],
                bot.settings.get("_username"),
                bot.settings.get("prefixes")[0],
                bot.settings.get("_username")
            )
        else:
            command = bot.commands_manager.get(parameters["command_name"])

            if not command:
                help_msg = "There is no such command"
            else:
                help_msg = """
**Information about command:** %s

**Description:**
%s

**Usage**:
%s
                """ % (command.aliases[0], command.description, command.usage)

        if not message.channel.is_private:
            await client.send_message(message.channel, "%s Check private message!" % message.author.mention)

        await client.send_message(message.author, help_msg)
