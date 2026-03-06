import io
import logging
import platform
import subprocess
import sys
import tarfile
import urllib.request
import zipfile
from pathlib import Path

import os

from app.logger import configure_logging

configure_logging(file_log_name="launcher")

if getattr(sys, "frozen", False):
    APP_DIR = Path(sys.executable).resolve().parent
else:
    APP_DIR = Path(__file__).resolve().parent

VENV = APP_DIR / ".venv"

LOG_FILE = APP_DIR / "launcher.log"

log = logging.getLogger("launcher")

log.debug(f"DISPLAY: {os.environ.get('DISPLAY', 'NOT SET')}")
log.debug(f"WAYLAND_DISPLAY: {os.environ.get('WAYLAND_DISPLAY', 'NOT SET')}")

_system = platform.system()
_machine = platform.machine().lower()

if _system == "Windows":
    UV = APP_DIR / "uv.exe"
    PYTHON = VENV / "Scripts" / "python.exe"
else:
    UV = APP_DIR / "uv"
    PYTHON = VENV / "bin" / "python"

UV_VERSION = "0.10.4"
UV_MIN_SIZE = 5 * 1024 * 1024  # 5 MB

if _system == "Windows":
    UV_URL = f"https://github.com/astral-sh/uv/releases/download/{UV_VERSION}/uv-x86_64-pc-windows-msvc.zip"
elif _system == "Linux":
    _arch = "aarch64" if _machine == "aarch64" else "x86_64"
    UV_URL = f"https://github.com/astral-sh/uv/releases/download/{UV_VERSION}/uv-{_arch}-unknown-linux-gnu.tar.gz"
else:
    raise RuntimeError(f"Unsupported platform: {_system}")

log.debug(f"Platform: {_system}/{_machine}")
log.debug(f"UV_URL: {UV_URL}")


def log_paths():
    log.debug(f"APP_DIR : {APP_DIR}")
    log.debug(f"UV      : {UV} (exists: {UV.exists()})")
    log.debug(f"VENV    : {VENV} (exists: {VENV.exists()})")
    log.debug(f"PYTHON  : {PYTHON} (exists: {PYTHON.exists()})")


def download_uv() -> None:
    log.info(f"Downloading uv {UV_VERSION} from: {UV_URL}")
    with urllib.request.urlopen(UV_URL) as response:
        data = io.BytesIO(response.read())
    log.debug(f"Archive downloaded, size: {len(data.getvalue()) / 1024 / 1024:.1f} MB")

    if _system == "Windows":
        with zipfile.ZipFile(data) as zf:
            log.debug(f"Archive contents: {zf.namelist()}")
            with zf.open("uv.exe") as src, open(UV, "wb") as dst:
                dst.write(src.read())
    else:
        with tarfile.open(fileobj=data, mode="r:gz") as tf:
            log.debug(f"Archive contents: {tf.getnames()}")
            member = tf.extractfile(f"uv-{_arch}-unknown-linux-gnu/uv")
            with open(UV, "wb") as dst:
                dst.write(member.read())
        UV.chmod(0o755)

    size = UV.stat().st_size
    log.debug(f"uv written to: {UV} ({size / 1024 / 1024:.1f} MB)")

    if size < UV_MIN_SIZE:
        UV.unlink()
        raise RuntimeError(
            f"uv is suspiciously small ({size} bytes), download may be corrupt. File removed."
        )

    log.info("uv downloaded successfully")


def bootstrap():
    if not UV.exists():
        log.info("First launch: downloading uv, please wait...")
        download_uv()

    if not VENV.exists():
        log.info("First launch: setting up environment, please wait...")
        subprocess.run(
            [
                UV,
                "sync",
                "--link-mode",
                "copy",
                "--no-dev",
                "--python-preference",
                "only-managed",
                "--python",
                "3.12",
            ],
            cwd=APP_DIR,
            check=True,
        )
        log.info("Environment ready.")
        log.debug(f"PYTHON  : {PYTHON} (exists: {PYTHON.exists()})")
    else:
        log.info("Virtual environment already exists, skipping bootstrap.")


def wait_for_user() -> None:
    """Pause for the user — gracefully handles no-terminal launches."""
    try:
        input("\nPress Enter to close...")
    except EOFError:
        pass  # No terminal, just exit


def main():
    try:
        log_paths()
        bootstrap()
        log_paths()

        has_terminal = sys.stdout and sys.stdout.isatty()

        log.info(f"Launching app: {PYTHON} {APP_DIR / 'main.py'}")
        result = subprocess.run(
            [PYTHON, APP_DIR / "main.py"],
            capture_output=not has_terminal,  # перехватываем только без терминала
            text=not has_terminal,
        )
        if result.returncode != 0:
            log.error(f"App exited with error code: {result.returncode}")
            if not has_terminal:
                log.error(f"stdout:\n{result.stdout}")
                log.error(f"stderr:\n{result.stderr}")
            wait_for_user()
            sys.exit(result.returncode)
    except Exception as e:
        log.exception(f"Launcher error: {e}")
        wait_for_user()
        sys.exit(1)


if __name__ == "__main__":
    main()
