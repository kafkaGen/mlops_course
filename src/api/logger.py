import os
import sys

from dotenv import load_dotenv
from loguru import logger as loguru_logger


def setup_logger(name: str | None = None) -> loguru_logger.__class__:
    """
    Set up and configure a Loguru logger instance that can be reused across the application.

    Args:
        name: Optional name for the logger context

    Returns:
        Configured Loguru logger instance
    """

    load_dotenv()

    log_level = os.getenv("LOG_LEVEL", "INFO").upper()

    loguru_logger.remove()
    loguru_logger.add(
        sys.stderr,
        format=(
            "<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | "
            "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>"
        ),
        level=log_level,
        colorize=True,
    )

    if name:
        return loguru_logger.bind(name=name)

    return loguru_logger


logger = setup_logger("mlops_course")
