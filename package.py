from pathlib import Path
import platform
import subprocess
import tarfile


def create_archive() -> None:
    if platform.system() == "Linux":
        release_path = Path("release")
        release_path.mkdir(exist_ok=True)
        archive_path = release_path / "MyApp.tar.gz"
        with tarfile.open(archive_path, "w:gz") as tar:
            tar.add("dist", arcname="MyApp")
        print(f"Archive created: {archive_path}")
    else:
        subprocess.run(["iscc", "installer.css"])


if __name__ == "__main__":
    create_archive()
