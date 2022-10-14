from sys import stdout
from loguru import logger


def start():
    logger.remove()
    logger.add("logs/log_{time}.txt", rotation="1 day")
    logger.add(stdout, colorize=True, format="<green>{time:DD.MM.YY H:mm:ss}</green> "
                                             "| <yellow><b>{level}</b></yellow> | <magenta>{file}</magenta> | <cyan>{"
                                             "message}</cyan>")

    logger.debug("Logger configured")
