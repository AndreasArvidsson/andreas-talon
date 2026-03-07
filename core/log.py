import logging
from talon import Module

mod = Module()

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
# logger.setLevel(logging.DEBUG)


@mod.action_class
class Actions:
    @staticmethod
    def debug(message: str):
        """Log debug message"""
        logger.debug(message)

    @staticmethod
    def info(message: str):
        """Log info message"""
        logger.info(message)

    @staticmethod
    def warning(message: str):
        """Log warning message"""
        logger.warning(message)

    @staticmethod
    def error(message: str):
        """Log error message"""
        logger.error(message)
