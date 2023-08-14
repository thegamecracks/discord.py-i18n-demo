This is the Python package to be installed when running [`pip`] on this project.

- `cogs/`: Contains sub-modules/packages that can be loaded at runtime.
- `locales/`: Contains gettext localizations written by translators.
- [`__init__.py`]: Marks the directory as a regular package.
- [`__main__.py`]: Provides the command-line interface used with `python -m dpygt`.
- `bot.py`: Defines the [`commands.Bot`] subclass handling Discord connectivity.
- `config_default.toml`: Defines the default configuration for filling in missing settings.
- `config.py`: Handles parsing and validating user configuration.
- `dpygt.pot`: Provides a localization template for this package.
- `translator.py`: Provides discord.py with an adapter for invoking gettext.

[`pip`]: https://packaging.python.org/en/latest/tutorials/installing-packages/
[`__init__.py`]: https://docs.python.org/3/tutorial/modules.html#packages
[`__main__.py`]: https://docs.python.org/3/library/__main__.html#main-py-in-python-packages
[`commands.Bot`]: https://discordpy.readthedocs.io/en/stable/ext/commands/api.html#discord.ext.commands.Bot
