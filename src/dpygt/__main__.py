import argparse
import importlib.metadata
import logging

from .bot import DPyGT
from .config import load_config

parser = argparse.ArgumentParser(
    prog=__package__,
    description=importlib.metadata.metadata("dpygt")["Summary"],
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

config = load_config()
bot = DPyGT(config)
bot.run(config.bot.token, root_logger=True)
