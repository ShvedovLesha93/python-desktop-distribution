from pathlib import Path
import platform
import subprocess
import tarfile


def create_archive() -> None:
    if platform.system() == "Linux":
        archive_path = Path("release") / "MyApp.tar.gz"
        with tarfile.open(archive_path, "w:gz") as tar:
            tar.add("dist", arcname="MyApp")
        print(f"Archive created: {archive_path}")
    else:
        subprocess.run(["iscc", "installer.css"])


if __name__ == "__main__":
    create_archive()
