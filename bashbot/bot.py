import discord

from bashbot.commands import CommandsManager
from bashbot.commands.about_command import AboutCommand
from bashbot.commands.close_command import CloseCommand
from bashbot.commands.freeze_command import FreezeCommand
from bashbot.commands.help_command import HelpCommand
from bashbot.commands.here_command import HereCommand
from bashbot.commands.open_command import OpenCommand
from bashbot.commands.permission_command import PermissionCommand
from bashbot.commands.rename_command import RenameCommand
from bashbot.commands.repeat_command import RepeatCommand
from bashbot.commands.select_command import SelectCommand
from bashbot.commands.sessions_command import SessionsCommand
from bashbot.commands.settings_command import SettingsCommand
from bashbot.controls import on_reaction_click
from discord import Client

from bashbot.permissions import set_permission, has_permission
from bashbot.session_manager import SessionManager
from bashbot.settings import Settings

from bashbot.commands.controls_command import ControlsCommand

commands_manager = CommandsManager()
settings = Settings("settings.json")
permissions = Settings("permissions.json")
client = Client()


def connect():
    @client.event
    async def on_ready():
        print('Logged in as %s with id: %s' % (client.user.name, client.user.id))

        if settings.get("firstrun"):
            print("You can add bot to your server via https://discordapp.com/api/oauth2/authorize?client_id=%s&scope=bot&permissions=1" % client.user.id)

        settings.set("_username", client.user.name)
        await client.change_presence(game=discord.Game(name=settings.get("presence_template") % client.user.name))

    @client.event
    async def on_message(message):
        is_command = False

        if message.channel.is_private:
            is_command = True

        for prefix in settings.get("prefixes"):
            if message.content.startswith(prefix):
                message.content = message.content[len(prefix):].lstrip()
                is_command = True

        if message.content.startswith("<@%s>" % client.user.id):
            message.content = message.content[len("<@%s>" % client.user.id):].lstrip()
            is_command = True

        session = SessionManager.get_session(message.channel)

        if is_command:
            success = await commands_manager.execute(client, message)
            if not success and not message.author.bot and session and session.status != "frozen":
                session.send_input(message.content)

            await delete_message(message)

        elif session and session.status != "frozen":
            if message.content.endswith(settings.get("redirect_tag")):
                session.send_input(message.content[:-len(settings.get("redirect_tag"))])

                await delete_message(message)

            else:
                short_tag = settings.get("short_tag").split("*")

                if short_tag[0] in message.content:
                    command = message.content[message.content.index(short_tag[0]) + len(short_tag[0]):]
                    command = command[:command.index(short_tag[1])]
                    session.send_input(command)

                    await delete_message(message)

        if not has_permission("chat.write", message.author, message.channel):
            await delete_message(message)

    @client.event
    async def on_reaction_add(reaction, user):
        on_reaction_click(reaction, user)

    @client.event
    async def on_reaction_remove(reaction, user):
        on_reaction_click(reaction, user)

    @client.event
    async def on_server_join(server):
        if settings.get("firstrun"):
            set_permission("global.internal.settings", "true", server.owner)
            set_permission("global.permissions.manage", "true", server.owner)
            set_permission("global.permissions.manage.edit", "true", server.owner)
            set_permission("global.permissions.manage.view", "true", server.owner)
            set_permission("global.session.kill", "true", server.owner)
            set_permission("global.session.killall", "true", server.owner)

            settings.set("firstrun", False)
            settings.save()

        about_msg = """
Hi, I am a discord bot that allows terminal access via chat.

**Learn more**: https://github.com/Adikso/BashBot
                """

        await client.send_message(list(server.channels)[0], about_msg)

    if not settings.get("token"):
        print("You have to provide token in %s and run bot again" % settings.filename)
    else:
        print("Starting bot..")
        client.run(settings.get("token"))


async def delete_message(message):
    me = message.channel.me if message.channel.type == discord.ChannelType.private else message.channel.server.me
    has_permission = message.channel.permissions_for(me).manage_messages

    if settings.get("delete_typed") == "true" and has_permission:
        await client.delete_message(message)


def register_commands():
    commands_manager.register(OpenCommand())
    commands_manager.register(RepeatCommand())
    commands_manager.register(HereCommand())
    commands_manager.register(SelectCommand())
    commands_manager.register(CloseCommand())
    commands_manager.register(HelpCommand())
    commands_manager.register(FreezeCommand())
    commands_manager.register(SettingsCommand())
    commands_manager.register(AboutCommand())
    commands_manager.register(PermissionCommand())
    commands_manager.register(ControlsCommand())
    commands_manager.register(SessionsCommand())
    commands_manager.register(RenameCommand())
