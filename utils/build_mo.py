"""Iterates through .po files in source packages and invokes msgfmt on them."""
import subprocess
from pathlib import Path

for po_path in Path("src").rglob("*.po"):
    print(po_path)
    output = str(po_path.with_suffix(".mo"))
    subprocess.run(["msgfmt", "-o", output, str(po_path)])
