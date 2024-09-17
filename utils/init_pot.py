"""Generates a .pot file from Python source files in a given directory."""

import argparse
import subprocess
import sys
from fnmatch import fnmatch
from pathlib import Path, PurePosixPath
from typing import Iterator

EXCLUDED = ["build", "env*", "venv*"]


def find_source_files(root: Path) -> Iterator[Path]:
    for path in root.glob("*.py"):
        if path.is_file():
            yield path

    for dir in root.iterdir():
        if not dir.is_dir():
            continue
        elif dir.name.startswith("."):
            continue
        elif any(fnmatch(dir.name, pat) for pat in EXCLUDED):
            continue

        yield from dir.rglob("*.py")


parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument(
    "-f",
    "--force",
    action="store_true",
    help="If a .pot file already exists, overwrite it",
)
parser.add_argument(
    "-v",
    "--verbose",
    action="count",
    default=0,
    help="Increase output verbosity",
)
parser.add_argument(
    "source",
    default=".",
    help="The directory to generate the file",
    nargs="?",
    type=Path,
)
args = parser.parse_args()

source: Path = args.source

if not source.is_dir():
    sys.exit(f"ERROR: no directory found at {source}")

output_path = source / f"{source.resolve().name}.pot"
if output_path.is_file():
    sys.exit(f"ERROR: existing template at {output_path}, use -f/--force to overwrite")

source_files = list(find_source_files(source))
if not source_files:
    sys.exit("ERROR: no .py source files found")

if args.verbose:
    for path in source_files:
        print(path)

subprocess.check_call(
    [
        "xgettext",
        "--add-comments",
        "-o",
        PurePosixPath(output_path),
        *(PurePosixPath(p) for p in source_files),
    ],
)

print(f"Generated {output_path} from {len(source_files)} source file(s)")
