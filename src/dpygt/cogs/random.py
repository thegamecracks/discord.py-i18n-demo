import random

import discord
from discord import app_commands
from discord.app_commands import locale_str as _
from discord.ext import commands

from dpygt.bot import DPyGT
from dpygt.translator import translate


class Random(commands.Cog):
    def __init__(self, bot: DPyGT):
        self.bot = bot

    @app_commands.command(
        # Command name
        name=_("roll"),
        # Command description ("roll")
        description=_("Roll one or more dice."),
    )
    @app_commands.describe(
        # Command parameter description ("n-dice")
        n_dice=_("The number of dice to roll."),
        # Command parameter description ("n-sides")
        n_sides=_("The number of sides with each dice."),
    )
    @app_commands.rename(
        # Command parameter name (used by "roll")
        n_dice=_("n-dice"),
        # Command parameter name (used by "roll")
        n_sides=_("n-sides"),
    )
    async def roll(
        self,
        interaction: discord.Interaction,
        n_dice: app_commands.Range[int, 1, 30],
        n_sides: app_commands.Range[int, 4, 256],
    ):
        rolls = [random.randint(1, n_sides) for _ in range(n_dice)]
        rolls_str = ", ".join(map(str, rolls))

        # Message sent after one or more dice have been rolled
        # {0}: a comma-separated list of each die's values
        # {1}: the total value of rolled dice
        message = await translate(_("Rolls: [{0}]\nTotal: {1}"), interaction)
        message = message.format(rolls_str, sum(rolls))

        await interaction.response.send_message(message)


async def setup(bot: DPyGT):
    await bot.add_cog(Random(bot))
