import logging
from logging.handlers import RotatingFileHandler
from rich.logging import RichHandler


def configure_logging(
    file_log_name: str = "app",
    console_level: int = logging.DEBUG,
    file_level: int = logging.INFO,
):
    root = logging.getLogger()
    if root.handlers:
        raise RuntimeError("Logging already configured! Call this only once in main().")

    # Create handlers (these run in MAIN process only)
    rich_handler = RichHandler(
        rich_tracebacks=True,
        markup=True,
        show_time=True,
        show_level=True,
        show_path=True,
    )
    rich_handler.setLevel(console_level)

    format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

    file_handler = RotatingFileHandler(
        f"{file_log_name}.log",
        maxBytes=10 * 1024 * 1024,  # 10MB
        backupCount=5,
        encoding="utf-8",
    )

    file_handler.setLevel(file_level)
    file_handler.setFormatter(logging.Formatter(format))

    root.addHandler(file_handler)
    root.addHandler(rich_handler)
    root.setLevel(console_level)
