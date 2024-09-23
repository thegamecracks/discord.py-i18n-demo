from __future__ import annotations

import importlib.metadata
import logging
from typing import TYPE_CHECKING

from discord.ext import commands

from .translator import GettextTranslator

if TYPE_CHECKING:
    from .config import DPyGTSettings

log = logging.getLogger(__name__)


# https://discordpy.readthedocs.io/en/stable/ext/commands/api.html
class DPyGT(commands.Bot):
    def __init__(self, config: DPyGTSettings):
        super().__init__(
            command_prefix=commands.when_mentioned,
            intents=config.bot.intents.create_intents(),
            strip_after_prefix=True,
        )
        self.config = config

    async def _maybe_load_jishaku(self) -> None:
        if not self.config.bot.allow_jishaku:
            return

        try:
            version = importlib.metadata.version("jishaku")
        except importlib.metadata.PackageNotFoundError:
            pass
        else:
            await self.load_extension("jishaku")
            log.info("Loaded jishaku extension (version: %s)", version)

    async def setup_hook(self) -> None:
        for path in self.config.bot.extensions:
            await self.load_extension(path, package=__package__)
        log.info("Loaded %d extensions", len(self.config.bot.extensions))
        await self._maybe_load_jishaku()

        await self.tree.set_translator(GettextTranslator())


class Context(commands.Context[DPyGT]): ...
