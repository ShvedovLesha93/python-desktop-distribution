import shutil
from pathlib import Path
import subprocess

APP_PATH = Path("app")
DIST_PATH = Path("dist")


def run_pyinstaller() -> tuple[bool, str | None]:
    cmd = ["uv", "run", "pyinstaller", "main.spec"]

    try:
        subprocess.run(cmd, check=True)
        return (True, None)
    except subprocess.CalledProcessError as e:
        return (False, str(e))


def collect_files() -> None:
    shutil.copytree(
        APP_PATH,
        DIST_PATH / "app",
        ignore=shutil.ignore_patterns("__pycache__", "*.po", "*.pot", "*.pyc"),
    )

    for file in ["main.py", "uv.lock", "pyproject.toml", "version.json"]:
        shutil.copy(file, DIST_PATH / file)


def clean():
    """Clean previous builds."""
    print("🧹 Cleaning previous builds...")

    dirs_to_clean = ["dist"]
    for dir_name in dirs_to_clean:
        dir_path = Path(dir_name)
        if dir_path.exists():
            shutil.rmtree(dir_path)
            print(f"   Removed {dir_name}/")

    print("✓ Clean complete\n")


def main() -> None:
    clean()
    result, err = run_pyinstaller()
    if result:
        print("✓ PyInstaller build complete\n")
        collect_files()
        print("✓ Necessary files copied\n")
    else:
        print(f"✗ Build failed: {err}")


if __name__ == "__main__":
    main()
