"""Logging configuration for the trading bot."""

import logging
import sys
from pathlib import Path


def setup_logging(
    log_file: str = "trading_bot.log",
    console_level: int = logging.INFO,
    file_level: int = logging.DEBUG,
) -> logging.Logger:
    """
    Configure logging for both console and file output.

    Args:
        log_file: Path to the log file.
        console_level: Logging level for console output.
        file_level: Logging level for file output.

    Returns:
        Configured logger instance.
    """
    logger = logging.getLogger("trading_bot")
    logger.setLevel(logging.DEBUG)

    if logger.handlers:
        return logger

    formatter = logging.Formatter(
        fmt="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(console_level)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    log_path = Path(log_file)
    file_handler = logging.FileHandler(log_path)
    file_handler.setLevel(file_level)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    logger.debug("Logging initialized. Log file: %s", log_path.resolve())
    return logger


def get_logger(name: str) -> logging.Logger:
    """Get a child logger for a specific module."""
    return logging.getLogger(f"trading_bot.{name}")
