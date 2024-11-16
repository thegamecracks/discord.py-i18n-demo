import argparse
import importlib.metadata
import logging
import sys

import discord

from .bot import DPyGT
from .config import load_config

parser = argparse.ArgumentParser(
    prog=__package__,
    description=importlib.metadata.metadata("discord.py-i18n-demo")["Summary"],
)
parser.add_argument(
    "-v",
    "--verbose",
    action="count",
    default=0,
    help="Increase logging verbosity",
)

args = parser.parse_args()

root_level = logging.INFO
if args.verbose > 0:
    log = logging.getLogger(__package__)
    log.setLevel(logging.DEBUG)
if args.verbose > 1:
    root_level = logging.DEBUG

# Configure logging early to capture our own initialization
discord.utils.setup_logging(
    level=root_level,
    root=True,
)

config = load_config()

if config.bot.token == "":
    sys.exit(
        "No bot token has been supplied by a config.toml file.\n"
        "Please get a Bot Token from https://discord.com/developers/applications "
        "and add it to your configuration."
    )

bot = DPyGT(config)
bot.run(
    config.bot.token,
    log_handler=None,
)
