from __future__ import annotations

import tomllib
from pathlib import Path
from typing import TYPE_CHECKING, Any

from pydantic import BaseModel

if TYPE_CHECKING:
    import discord

CONFIG_DEFAULT_PATH = Path("config_default.toml")
CONFIG_PATH = Path("config.toml")


class _BaseModel(BaseModel):
    class Config:
        extra = "forbid"


# https://docs.pydantic.dev/usage/settings/
class DPyGTSettings(_BaseModel):
    bot: DPyGTSettingsBot


class DPyGTSettingsBot(_BaseModel):
    extensions: list[str]
    intents: DPyGTSettingsBotIntents
    token: str


class DPyGTSettingsBotIntents(_BaseModel):
    """The intents used when connecting to the Discord gateway.

    Default intents are enabled but can be overridden here.

    .. seealso:: https://discordpy.readthedocs.io/en/stable/api.html#intents

    """

    class Config:
        extra = "allow"

    def create_intents(self) -> discord.Intents:
        import discord

        intents = dict(discord.Intents.default())
        intents |= self.model_dump()
        return discord.Intents(**intents)


DPyGTSettings.model_rebuild()
DPyGTSettingsBot.model_rebuild()


def _recursive_update(dest: dict, src: dict) -> None:
    for k, vsrc in src.items():
        vdest = dest.get(k)
        if isinstance(vdest, dict) and isinstance(vsrc, dict):
            _recursive_update(vdest, vsrc)
        else:
            dest[k] = vsrc


def _load_raw_config(path: Path) -> dict[str, Any]:
    with path.open("rb") as f:
        return tomllib.load(f)


def load_default_config() -> DPyGTSettings:
    """Loads the default configuration file.

    :returns: The settings that were parsed.
    :raises FileNotFoundError:
        The default configuration file could not be found.

    """
    data = _load_raw_config(CONFIG_DEFAULT_PATH)
    return DPyGTSettings.model_validate(data)


def load_config(*, merge_default: bool = True) -> DPyGTSettings:
    """Loads the bot configuration file.

    :param merge_default:
        If True, the default configuration file will be used as a base
        and the normal configuration is applied on top of it,
        if it exists.
    :returns: The settings that were parsed.
    :raises FileNotFoundError:
        If merge_default is False, this means the configuration file
        could not be found. Otherwise, it means the default configuration
        file could not be found.

    """
    if not merge_default:
        data = _load_raw_config(CONFIG_PATH)
    elif CONFIG_PATH.exists():
        data = _load_raw_config(CONFIG_DEFAULT_PATH)
        overwrites = _load_raw_config(CONFIG_PATH)
        _recursive_update(data, overwrites)
    else:
        data = _load_raw_config(CONFIG_DEFAULT_PATH)

    return DPyGTSettings.model_validate(data)
