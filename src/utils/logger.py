import logging
import logging.handlers
import sys
from pathlib import Path
from typing import Optional


def ensure_logs_dir(logs_dir: Optional[Path] = None) -> Path:
    """Ensure the logs directory exists and return its path."""
    if logs_dir is None:
        logs_dir = Path(__file__).parent.parent.parent / "logs"
    logs_dir.mkdir(parents=True, exist_ok=True)
    return logs_dir


def setup_logger(
    name: str,
    log_file: str | None = None,
    log_level_console: int = logging.INFO,
    log_level_file: int = logging.DEBUG,
    max_bytes: int = 10 * 1024 * 1024,  # 10MB
    backup_count: int = 5,
) -> logging.Logger:
    """
    Set up a logger with console and optional rotating file handlers.

    Args:
        name (str): Name of the logger.
        log_file (str, optional): Name of the log file. Will be placed in logs/ directory.
        log_level_console (int): Log level for console output.
        log_level_file (int): Log level for file output.
        max_bytes (int): Maximum log file size before rotation.
        backup_count (int): Number of backup log files to keep.

    Returns:
        logging.Logger: Configured logger instance.
    """
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)  # Set base level to capture all messages

    # Check if logger already has handlers to avoid duplicate logs
    if logger.handlers:
        return logger

    # Formatter
    formatter = logging.Formatter(
        fmt="%(asctime)s - %(name)s - %(levelname)-8s - %(filename)s:%(lineno)d - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    # Console Handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(log_level_console)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    # File Handler with rotation
    if log_file:
        logs_dir = ensure_logs_dir()
        log_path = logs_dir / log_file

        try:
            file_handler = logging.handlers.RotatingFileHandler(
                filename=log_path,
                maxBytes=max_bytes,
                backupCount=backup_count,
                encoding="utf-8",
                mode="a",
            )
            file_handler.setLevel(log_level_file)
            file_handler.setFormatter(formatter)
            logger.addHandler(file_handler)
            logger.debug("Log file handler created at: %s", log_path)
        except Exception as e:
            logger.error("Failed to create file handler: %s", e, exc_info=True)

    # Prevent logging from propagating to the root logger
    logger.propagate = False

    return logger


def get_logger(name: Optional[str] = None) -> logging.Logger:
    """
    Get a configured logger instance.

    Args:
        name (str, optional): Name of the logger. If None, uses the root package name.

    Returns:
        logging.Logger: Configured logger instance.
    """
    if name is None:
        name = "ai_agent"
    return setup_logger(name, f"{name}.log")
