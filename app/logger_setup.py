"""
Easy logger setup for frequent use of logging
"""

__author__ = "8243359, Czerwinski, 8408446, Noll"

import logging

loggers = {}

basic_formatter = logging.Formatter(
    '%(asctime)s - %(levelname)s - %(module)s - %(funcName)s - %(message)s')


def setup_logger(name: str, formatter: logging.Formatter | None = basic_formatter):
    """
    Sets up a logger, keeps track in a dictionary
    :param name:
    :param formatter:
    :return:
    """
    if loggers.get(name) is not None:
        return loggers.get(name)

    handler = logging.StreamHandler()
    handler.setFormatter(formatter)

    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    logger.addHandler(handler)
    return logger
