import discord
from discord import Message, Interaction, Embed, app_commands
from discord.ext import commands
from discord.ext.commands import Context
from discord.ui import View

from bashbot.command import session_exists
from bashbot.terminal.control import TerminalControl
from bashbot.terminal.sessions import sessions
from bashbot.terminal.terminal import Terminal


async def controls_callback(interaction: Interaction):
    label = interaction.data['custom_id']
    if label.startswith('control_'):
        label = label[len('control_'):]
        terminal = sessions().by_message(interaction.message)
        control: TerminalControl = terminal.controls[label]
        terminal.send_input(control.text)

    await interaction.response.defer()


class ControlsCommand(commands.Cog):
    @commands.hybrid_group(
        name='controls',
        aliases=['.controls'],
        description='Manages terminal controls',
        usage='add/remove [emoji] [content..]'
    )
    async def controls(self, ctx):
        if ctx.invoked_subcommand is None:
            pass

    @controls.command()
    @session_exists()
    async def add(self, ctx: Context, label, content):
        terminal: Terminal = sessions().by_channel(ctx.channel)
        message: Message = sessions().find_message(terminal)

        view = View.from_message(message)
        view.timeout = None

        button = discord.ui.Button(style=discord.ButtonStyle.gray, label=label, custom_id=f'control_{label}')
        button.callback = controls_callback
        view.add_item(button)

        new_message = await message.edit(view=view)
        sessions().update_message_reference(terminal, new_message)

        terminal.add_control(label, content)

        if ctx.interaction:
            embed = Embed(description=f"Control added", color=0x00ff00)
            await ctx.reply(embed=embed, ephemeral=False, delete_after=0)

    @controls.command()
    @session_exists()
    async def remove(self, ctx: Context, label: str = None):
        terminal: Terminal = sessions().by_channel(ctx.channel)
        message: Message = sessions().find_message(terminal)

        terminal.remove_control(label)
        view = View.from_message(message)

        for component in view.children:
            if component.custom_id == label:
                view.remove_item(component)
                break
        else:
            await ctx.reply(content="Couldn't find specified control")
            return

        new_message = await message.edit(view=view)
        sessions().update_message_reference(terminal, new_message)

        if ctx.interaction:
            embed = Embed(description=f"Control removed", color=0xff0000)
            await ctx.reply(embed=embed, ephemeral=False, delete_after=0)

    @remove.autocomplete('label')
    async def remove_autocomplete(self, interaction: Interaction, current: str):
        terminal: Terminal = sessions().by_channel(interaction.channel)
        results = terminal.search_control(current)
        return [
            app_commands.Choice(name=option, value=option)
            for option in results
        ]
