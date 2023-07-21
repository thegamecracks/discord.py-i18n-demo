import gettext
import importlib.resources

import discord
from discord import app_commands


_locales_path = str(importlib.resources.files(__package__).joinpath("locales"))


def locale_to_gnu(locale: discord.Locale) -> str:
    return str(locale).replace("-", "_")


class GettextTranslator(app_commands.Translator):
    async def translate(
        self,
        string: app_commands.locale_str,
        locale: discord.Locale,
        context: app_commands.TranslationContextTypes,
    ) -> str | None:
        try:
            t = gettext.translation(
                domain="dpygt",
                localedir=_locales_path,
                languages=(locale_to_gnu(locale),),
            )
        except OSError:
            return

        s = t.gettext(str(string))
        return s or None
