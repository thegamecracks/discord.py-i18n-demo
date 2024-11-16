def _get_version() -> str:
    from importlib.metadata import version

    return version("discord.py-i18n-demo")


__version__ = _get_version()
