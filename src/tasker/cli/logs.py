from __future__ import annotations

import logging
from pathlib import Path

from rich.logging import RichHandler


class ColoredMessageFormatter(logging.Formatter):
    """Color the entire log message based on its log level."""

    COLORS = {
        logging.DEBUG: "dim",
        logging.INFO: "green",
        logging.WARNING: "yellow",
        logging.ERROR: "red",
        logging.CRITICAL: "bold red",
    }

    def format(self, record: logging.LogRecord) -> str:
        message = super().format(record)
        color = self.COLORS.get(record.levelno, "white")

        return f"[{color}]{message}[/{color}]"


def setup_logging(
    level: int = logging.INFO,
    log_file: str | Path | None = None,
) -> None:
    """
    Configure the root logger.

    Console:
        Colored output containing only the log message.

    File:
        Plain-text logs with timestamp, level, logger name, and message.

    Args:
        level: Root logging level.
        log_file: Optional path to a log file.
    """
    root_logger = logging.getLogger()
    root_logger.setLevel(level)

    # Prevent duplicate handlers if called more than once.
    root_logger.handlers.clear()

    # Colored stdout logging.
    console_handler = RichHandler(
        level=level,
        show_time=False,
        show_level=False,
        show_path=False,
        markup=True,
        rich_tracebacks=True,
    )
    console_handler.setFormatter(
        ColoredMessageFormatter("%(message)s")
    )

    root_logger.addHandler(console_handler)

    # Optional file logging.
    if log_file is not None:
        log_path = Path(log_file)
        log_path.parent.mkdir(parents=True, exist_ok=True)

        file_handler = logging.FileHandler(
            log_path,
            encoding="utf-8",
        )
        file_handler.setLevel(level)
        file_handler.setFormatter(
            logging.Formatter(
                "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
            )
        )

        root_logger.addHandler(file_handler)

