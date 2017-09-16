from bashbot.commands.syntax import SyntaxNode
from bashbot.permissions import has_permission


class Command:
    def __init__(self):
        self.name = None
        self.aliases = None
        self.description = None
        self.usage = None
        self.syntax = SyntaxNode(None)
        self.allowed_private = False
        self.permission = None

    async def execute(self, client, message, alias, args):
        parameters = {"_alias": alias}
        valid_syntax = True

        action = None
        current_node = self.syntax

        index = -1
        for arg in args:
            index += 1
            node = current_node.get(arg)

            if not node:
                param = current_node.get_param()

                if param:
                    if param.multiple:
                        parameters[param.name] = ' '.join(args[index:]).rstrip()
                    else:
                        parameters[param.name] = arg

                    current_node = param

                    if param.action:
                        action = param.action

                    if param.multiple:
                        break

                    continue

                valid_syntax = False
                action = None
                break

            if node.action:
                action = node.action
                continue
            else:
                action = None

            current_node = node

        if action:
            await getattr(self, action)(client, message, parameters)
        else:
            if not valid_syntax:
                await client.send_message(message.channel, "__**Syntax error**__\n**Usage**: %s" % self.usage)
                return

            if self.syntax.action:
                await getattr(self, self.syntax.action)(client, message, parameters)


class CommandsManager:
    def __init__(self):
        self.commands = []

    def register(self, command):
        self.commands.append(command)

    async def execute(self, client, message):
        alias = message.content.split()[0]
        args = message.content.split()[1:]

        print("%s @ %s[%s]: %s" % (message.author.name, message.channel.name,
                                   (message.channel.server.name if hasattr(message.channel, "server") else "PM"),
                                   message.content.encode('utf-8')))

        for command in self.commands:
            if alias in command.aliases:
                if command.allowed_private or not message.channel.is_private:
                    if has_permission(command.permission, message.author, message.channel):
                        await command.execute(client, message, alias, args)

                        return True
                    else:
                        await client.send_message(message.channel, ":lock: You don't have permission to use this command")
                        return True
                else:
                    await client.send_message(message.channel, "This command is not available in private chat")
                    return True

        return False

    def get(self, alias):
        for command in self.commands:
            if command.name == alias or alias in command.aliases:
                return command

        return None


__all__ = ["syntax", "open_command", "test_command"]
