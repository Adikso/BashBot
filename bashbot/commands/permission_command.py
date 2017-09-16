from bashbot import permissions, bot
from bashbot.commands import Command
from bashbot.commands.syntax import SyntaxBuilder


class PermissionCommand(Command):
    def __init__(self):
        super().__init__()

        self.name = "Manage permissions"
        self.aliases = [".permission", ".p", ".permissions"]
        self.description = "Manage permissions"
        self.usage = ".permission <user> <permission_name> [new_value]\n.permission list\n\n**Example:**\n.permission @Adikso channels.#general.info_about false"
        self.permission = "permissions.manage"

        self.syntax = SyntaxBuilder()\
            .action("list", "list_all").parent()\
            .param("username", "show")\
            .param("permission_name", "verify")\
            .param("new_value", "set")\
        .build()

    async def show(self, client, message, parameters):
        username = parameters["username"]

        if username.startswith("<@"):
            username = username[2:-1]

        permissions = bot.permissions.get(username)
        permissions_list = "__**%s's permissions:**__\n" % username

        if not permissions:
            permissions = bot.permissions.get("default")

        if "channels" in permissions:
            permissions_list += "\n**Channels**\n"
            for channel, perms in permissions["channels"].items():
                permissions_list += "<#%s>\n" % channel
                for key_perm, value_perm in perms.items():
                    permissions_list += "       %s = %s\n" % (key_perm, value_perm)

        if "servers" in permissions:
            permissions_list += "\n**Servers**\n"
            for server, perms in permissions["servers"].items():
                permissions_list += "%s\n" % server
                for key_perm, value_perm in perms.items():
                    permissions_list += "       %s = %s\n" % (key_perm, value_perm)

        if "global" in permissions:
            permissions_list += "\n**Global**\n"
            for key, value in permissions["global"].items():
                permissions_list += "%s = %s\n" % (key, value)

        await client.send_message(message.channel, permissions_list)

    async def set(self, client, message, parameters):
        permissions.set_permission(parameters["permission_name"], parameters["new_value"], parameters["username"])
        await client.send_message(message.channel, "Permission updated")

    async def verify(self, client, message, parameters):
        username = parameters["username"]

        if username.startswith("<@"):
            username = username[2:-1]

        permissions = bot.permissions.get(username)

        if parameters["permission_name"] in list(permissions.keys()):
            value = permissions[parameters["permission_name"]]
            await client.send_message(message.channel, "%s = %s" % (parameters["permission_name"], value))
