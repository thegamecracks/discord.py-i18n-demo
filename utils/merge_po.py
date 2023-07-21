"""Re-invokes xgettext on source packages and merges them into .po/.pot files."""
import subprocess
from pathlib import Path

for package_path in Path("src").iterdir():
    if not package_path.is_dir():
        continue
    elif not any(package_path.glob("*.pot")):
        continue

    print(package_path)

    source_files: list[Path] = []
    source_files.extend(package_path.rglob("*.py"))
    if not source_files:
        continue

    po_paths: list[Path] = []
    po_paths.extend(package_path.rglob("*.pot"))
    po_paths.extend(package_path.rglob("*.po"))
    if not po_paths:
        continue

    merging_po = package_path / "messages.po.merging"
    subprocess.check_call(["xgettext", "-o", merging_po, *source_files])

    # Hide CHARSET warning by defaulting to utf-8
    content_type_temp = rb'"Content-Type: text/plain; charset=CHARSET\n"'
    content_type_utf8 = rb'"Content-Type: text/plain; charset=UTF-8\n"'
    content_pot = merging_po.read_bytes()
    content_pot = content_pot.replace(content_type_temp, content_type_utf8)
    merging_po.write_bytes(content_pot)

    for po_path in po_paths:
        print(po_path)
        subprocess.check_call(["msgmerge", po_path, merging_po, "-o", po_path])

    merging_po.unlink()
