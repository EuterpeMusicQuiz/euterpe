import os
import subprocess

VERSION = __version__ = "UNKNOWN"

PACKAGE_DIR = os.path.dirname(__file__)
VERSION_FILE = os.path.join(PACKAGE_DIR, "VERSION")


def _get_version_from_git() -> str:
    git_desc = subprocess.run(
        ["git", "describe", "--always", "--tags"],
        capture_output = True,
        cwd = PACKAGE_DIR,
    ).stdout.decode()
    return git_desc.split("-g")[0]

def _get_version() -> str:
    try:
        version = _get_version_from_git()
        open(VERSION_FILE, "w").write(version)
        return version
    except Exception:
        return open(VERSION_FILE, "r").read()


try:
    VERSION = __version__ = _get_version()
except:
    pass
