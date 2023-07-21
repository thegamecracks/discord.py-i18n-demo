import random

import discord
from discord import app_commands
from discord.app_commands import locale_str as _
from discord.ext import commands

from ..bot import DPyGT


class Random(commands.Cog):
    def __init__(self, bot: DPyGT):
        self.bot = bot

    @app_commands.command(
        name=_("roll"),
        description=_("Roll one or more dice."),
    )
    @app_commands.describe(
        n_dice=_("The number of dice to roll."),
        n_sides=_("The number of sides with each dice."),
    )
    @app_commands.rename(
        n_dice=_("n-dice"),
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

        message = _("Rolls: [{0}]\nTotal: {1}")
        message = await interaction.translate(message) or str(message)
        message = message.format(rolls_str, sum(rolls))

        await interaction.response.send_message(message)


async def setup(bot: DPyGT):
    await bot.add_cog(Random(bot))
