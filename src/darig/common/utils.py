from importlib.metadata import PackageNotFoundError, version


def darig_version() -> str:
    try:
        return version("darig")
    except PackageNotFoundError:
        return "Unknown (package not installed)"
