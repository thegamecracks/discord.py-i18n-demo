import discord
from discord import app_commands
from discord.app_commands import locale_str as _
from discord.ext import commands

from dpygt.bot import DPyGT
from dpygt.translator import translate


class Choices(commands.Cog):
    def __init__(self, bot: DPyGT):
        self.bot = bot

    @app_commands.command(
        # Command name
        name=_("fruit"),
        # Command description ("fruit")
        description=_("What's your favourite fruit?"),
    )
    @app_commands.describe(
        # Command parameter description ("fruit")
        fruit=_("Your favourite fruit"),
    )
    @app_commands.rename(
        # Command parameter name (used by "fruit")
        fruit=_("fruit"),
    )
    @app_commands.choices(
        fruit=[
            # Command parameter choice (used by "/fruit <fruit>")
            app_commands.Choice(name=_("Apple"), value=1),
            # Command parameter choice (used by "/fruit <fruit>")
            app_commands.Choice(name=_("Banana"), value=2),
            # Command parameter choice (used by "/fruit <fruit>")
            app_commands.Choice(name=_("Cherry"), value=3),
        ],
    )
    async def fruit(
        self,
        interaction: discord.Interaction,
        fruit: app_commands.Choice[int],
    ):
        # Message telling the user their favourite fruit
        message = await translate(_("Your favourite fruit is {}!"), interaction)
        message = message.format(fruit)
        await interaction.response.send_message(message)


async def setup(bot: DPyGT):
    await bot.add_cog(Choices(bot))
