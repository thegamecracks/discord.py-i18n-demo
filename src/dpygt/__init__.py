def _get_version() -> str:
    from importlib.metadata import version

    return version("sqlitediff")


__version__ = _get_version()
