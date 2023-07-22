from __future__ import annotations

import gettext
import importlib.resources
from typing import TYPE_CHECKING, Any

import discord
from discord import app_commands
from discord.ext import commands

if TYPE_CHECKING:
    from .bot import DPyGT


_locales_path = str(importlib.resources.files(__package__).joinpath("locales"))
DOMAIN = "dpygt"


def locale_to_gnu(locale: discord.Locale) -> str:
    return str(locale).replace("-", "_")


class EmptyTranslations(gettext.NullTranslations):
    """Returns an empty message to indicate no translation is available."""

    def gettext(self, message: str) -> str:
        return ""

    def ngettext(self, msgid1: str, msgid2: str, n: int) -> str:
        return ""

    def pgettext(self, context: str, message: str) -> str:
        return ""

    def npgettext(self, context: str, msgid1: str, msgid2: str, n: int) -> str:
        return ""


class GettextTranslator(app_commands.Translator):
    async def translate(
        self,
        string: app_commands.locale_str,
        locale: discord.Locale,
        context: app_commands.TranslationContextTypes,
    ) -> str | None:
        try:
            t = gettext.translation(
                domain=DOMAIN,
                localedir=_locales_path,
                languages=(locale_to_gnu(locale), "en_US"),
            )
        except OSError:
            return

        t.add_fallback(EmptyTranslations())

        plural: app_commands.locale_str | None = string.extras.get("plural")
        if plural is not None:
            assert isinstance(context.data, int)
            translated = t.ngettext(string.message, plural.message, context.data)
        else:
            translated = t.gettext(string.message)

        return translated or None


async def translate(
    message: app_commands.locale_str,
    obj: DPyGT | discord.Interaction,
    locale: discord.Locale | None = None,
    data: Any = None,
) -> str:
    """A shorthand for translating a message.

    Unlike the methods built into discord.py, this will use the original message
    if a translation could not be found.

    """
    if isinstance(obj, commands.Bot):
        if locale is None:
            return str(message)

        assert obj.tree.translator is not None
        context = app_commands.TranslationContext(
            location=app_commands.TranslationContextLocation.other,
            data=data,
        )
        translated = await obj.tree.translator.translate(
            message,
            locale=locale,
            context=context,
        )
    else:
        translated = await obj.translate(message, data=data)

    return translated or str(message)
