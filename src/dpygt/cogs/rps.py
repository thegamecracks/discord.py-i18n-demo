from __future__ import annotations

import asyncio
import datetime
from abc import ABC, abstractmethod
from typing import Iterable

import discord
from discord import app_commands
from discord.app_commands import locale_str as _
from discord.ext import commands

from ..bot import DPyGT
from ..translator import translate

UM = discord.User | discord.Member


class RPSButton(discord.ui.Button["BaseRPSView"]):
    """Represents one of rock, paper, or scissors.

    The given value determines if it beats the next option.

    """

    def __init__(self, value: int, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.value = value

    def beats(self, other: RPSButton) -> bool:
        assert self.view is not None
        return (self.value + 1) % len(self.view.children) == other.value

    async def callback(self, interaction: discord.Interaction):
        assert self.view is not None
        await self.view.step(interaction, self)


class BaseRPSView(discord.ui.View, ABC):
    """Defines the interface for any Rock, Paper, Scissors variant."""

    children: list[RPSButton]
    message: discord.Message

    def __init__(
        self,
        interaction: discord.Interaction,
        buttons: Iterable[RPSButton],
        *args,
        **kwargs,
    ):
        super().__init__(*args, **kwargs)
        for button in buttons:
            self.add_item(button)
        self.interaction = interaction

    @property
    def timeout_timestamp(self) -> str | None:
        if self.timeout is None:
            return
        ends = datetime.datetime.now() + datetime.timedelta(seconds=self.timeout)
        return discord.utils.format_dt(ends, style="R")

    async def on_timeout(self):
        for button in self.children:
            button.disabled = True
        timestamp = discord.utils.format_dt(datetime.datetime.now(), style="R")
        content = await translate(_("(ended {0} from inactivity)"), self.interaction)
        content = content.format(timestamp)
        await self.message.edit(content=content, view=self)

    @abstractmethod
    def get_winners(self) -> list[UM] | None:
        """Returns the winners of the game."""

    @abstractmethod
    async def get_embed(self, winners: list[UM] | None) -> discord.Embed:
        """Returns the embed used for displaying the game's state."""

    @abstractmethod
    async def step(self, interaction: discord.Interaction, button: RPSButton):
        """Triggered after a move has been submitted."""

    async def update(self, interaction: discord.Interaction, **kwargs):
        """Edits the game message with the current view."""
        finished = all(b.disabled for b in self.children)

        content: str | None = None
        timestamp = self.timeout_timestamp
        if not finished and timestamp is not None:
            content = await translate(_("(ends {0})"), interaction)
            content = content.format(timestamp)

        if content is not None:
            kwargs["content"] = content

        kwargs["view"] = self

        try:
            if interaction.response.is_done():
                await interaction.edit_original_response(**kwargs)
            else:
                await interaction.response.edit_message(**kwargs)
        except discord.HTTPException:
            pass
        else:
            if finished:
                self.stop()

    async def start(self, *, wait=True):
        """Starts the game."""
        embed = await self.get_embed(self.get_winners())

        content = ""
        timestamp = self.timeout_timestamp
        if timestamp is not None:
            content = await translate(_("(ends {0})"), self.interaction)
            content = content.format(timestamp)

        await self.interaction.response.send_message(content, embed=embed, view=self)
        self.message = await self.interaction.original_response()

        if wait:
            await self.wait()


class RPSDuelView(BaseRPSView):
    """A typical variant of RPS with two players."""

    moves: dict[UM, RPSButton | None]

    def __init__(
        self,
        interaction: discord.Interaction,
        buttons: Iterable[RPSButton],
        players: set[UM],
        *args,
        **kwargs,
    ):
        super().__init__(interaction, buttons, *args, **kwargs)
        self.players = players
        self.moves = {p: None for p in players}

    @property
    def public(self) -> bool:
        """Indicates if anyone can join this game."""
        return len(self.players) < 2

    @property
    def n_ready(self) -> int:
        """Indicates the number of players that have selected a move."""
        return sum(v is not None for v in self.moves.values())

    @property
    def n_waiting(self) -> int:
        """Indicates the number of players that have not selected a move."""
        return 2 - self.n_ready

    async def interaction_check(self, interaction: discord.Interaction):
        if interaction.user.bot:
            return False
        # Check if they made a move already
        move = self.moves.get(interaction.user)
        if move is not None:
            return False
        elif self.public:
            # Check if there's room for another player
            return self.n_waiting > 0
        else:
            # Check if they are part of the game
            return interaction.user in self.players

    def get_winners(self) -> list[UM] | None:
        if any(m is None for m in self.moves.values()):
            return None
        elif self.public and len(self.moves) < 2:
            return None

        (a, a_move), (b, b_move) = self.moves.items()
        assert a_move is not None
        assert b_move is not None

        if a_move.beats(b_move):
            return [a]
        elif b_move.beats(a_move):
            return [b]

        return []

    def get_base_embed(self) -> discord.Embed:
        return discord.Embed()

    def list_moves(self, *, reveal: bool) -> list[str]:
        move_list: list[str] = []
        for player, button in self.moves.items():
            move = "⬛"
            if button is None:
                move = "🤔"
            elif reveal:
                move = button.emoji
            move_list.append(f"{move} {player.mention}")
        return move_list

    async def get_embed(self, winners: list[UM] | None) -> discord.Embed:
        description: list[str] = []

        if winners:
            content = await translate(_("The winner is {0}!"), self.interaction)
            content = content.format(winners[0].mention)
            description.append(content)
        elif winners is not None:
            description.append(await translate(_("It's a tie!"), self.interaction))

        description.extend(self.list_moves(reveal=winners is not None))

        n = self.n_waiting
        if len(self.moves) < 2 and n:
            content = await translate(
                _("Waiting for {0} player...", plural=_("Waiting for {0} players...")),
                self.interaction,
                data=n,
            )
            content = content.format(n)
            description.append(content)

        embed = self.get_base_embed()
        embed.description = "\n".join(description)

        return embed

    async def step(self, interaction: discord.Interaction, button: RPSButton):
        self.moves[interaction.user] = button

        winners = self.get_winners()
        final_embed = await self.get_embed(winners)

        if winners is not None:
            for button in self.children:
                button.disabled = True

            pause_embed = self.get_base_embed()
            reveal_message = await translate(_("Revealing the winner..."), interaction)
            pause_embed.description = "\n".join(
                [reveal_message] + self.list_moves(reveal=False)
            )
            await self.update(interaction, embed=pause_embed)
            await asyncio.sleep(2)

        await self.update(interaction, embed=final_embed)


def _create_buttons(items: Iterable[tuple[int, dict[str, object]]]) -> tuple[RPSButton]:
    return tuple(RPSButton(value, **kwargs) for value, kwargs in items)


class RPS(commands.Cog):
    STANDARD = (
        (2, {"emoji": "️🪨", "style": discord.ButtonStyle.primary}),
        (1, {"emoji": "📰", "style": discord.ButtonStyle.primary}),
        (0, {"emoji": "✂️", "style": discord.ButtonStyle.primary}),
    )

    def __init__(self, bot: DPyGT):
        self.bot = bot

    @app_commands.command(
        name=_("rock-paper-scissors"),
        description=_("Start a game of rock, paper, scissors."),
    )
    @app_commands.describe(
        user=_(
            "The user to play against. If not provided, anyone can play their move."
        ),
    )
    @app_commands.rename(
        user=_("user"),
    )
    async def rps(
        self,
        interaction: discord.Interaction,
        user: discord.User | None = None,
    ):
        view = RPSDuelView(
            interaction,
            _create_buttons(self.STANDARD),
            {interaction.user, user}
            if user is not None and user != interaction.user
            else set(),
            timeout=180,
        )

        await view.start()


async def setup(bot: DPyGT):
    await bot.add_cog(RPS(bot))
