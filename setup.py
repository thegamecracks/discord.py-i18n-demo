"""
This setup.py handles compiling .po (portable object) files into their
appropriate .mo (machine object) results.

Reference: https://setuptools.pypa.io/en/latest/userguide/extension.html#setuptools.command.build.SubCommand
"""
import shutil
import subprocess
from pathlib import Path
from typing import Iterator
import warnings

from setuptools import Command, setup
from setuptools.command.build import SubCommand, build


class build_mo(Command, SubCommand):
    """Builds machine object translation files."""

    build_lib = "build/lib"

    # SubCommand protocol

    def initialize_options(self) -> None:
        """
        Set or (reset) all options/attributes/caches used by the command
        to their default values. Note that these values may be overwritten during
        the build.
        """

    def finalize_options(self) -> None:
        """
        Set final values for all options/attributes used by the command.
        Most of the time, each option/attribute/cache should only be set if it does not
        have any value yet (e.g. ``if self.attr is None: self.attr = val``).
        """

    def run(self) -> None:
        """
        Execute the actions intended by the command.
        (Side effects **SHOULD** only take place when ``run`` is executed,
        for example, creating new files or writing to the terminal output).
        """
        msgfmt = shutil.which("msgfmt")
        if msgfmt is None:
            return warnings.warn(
                "msgfmt is not available, building .mo files will be skipped",
                RuntimeWarning,
            )

        for path in self._find_po_files():
            output = str(self._get_output_path(path.with_suffix(".mo")))
            subprocess.run(["msgfmt", "-o", output, str(path)])

    def get_source_files(self) -> list[str]:
        """
        Return a list of all files that are used by the command to create
        the expected outputs. For example, if your build command transpiles
        Java files into Python, you should list here all the Java files.
        The primary purpose of this function is to help populating the ``sdist``
        with all the files necessary to build the distribution.
        All files should be strings relative to the project root directory.
        """
        return list(self.get_output_mapping().values())

    def get_outputs(self) -> list[str]:
        """
        Return a list of files intended for distribution as they would have been
        produced by the build.
        These files should be strings in the form of
        ``"{build_lib}/destination/file/path"``.

        .. note::
           The return value of ``get_output()`` should include all files used as keys
           in ``get_output_mapping()`` plus files that are generated during the build
           and don't correspond to any source file already present in the project.
        """
        return list(self.get_output_mapping().keys())

    def get_output_mapping(self) -> dict[str, str]:
        """
        Return a mapping between destination files as they would be produced by the
        build (dict keys) into the respective existing (source) files (dict values).
        Existing (source) files should be represented as strings relative to the project
        root directory.
        Destination files should be strings in the form of
        ``"{build_lib}/destination/file/path"``.
        """
        return {
            str(self._get_output_path(path)): str(path)
            for path in self._find_po_files()
        }

    # Utility methods

    def _find_po_files(self) -> Iterator[Path]:
        for package_path in Path("src").iterdir():
            if not package_path.is_dir():
                continue

            for po_path in package_path.rglob("*.po"):
                yield po_path

    def _get_output_path(self, path_str: Path | str) -> Path:
        if self.editable_mode:
            return Path(path_str)
        return Path(self.build_lib) / path_str

    # Subcommand registration

    build.sub_commands.append(("build_mo", None))


setup(cmdclass={"build_mo": build_mo})
