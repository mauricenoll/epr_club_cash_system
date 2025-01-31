import logging

loggers = {}

basic_formatter = logging.Formatter(
    '%(asctime)s - %(levelname)s - %(module)s - %(funcName)s - %(message)s')


def setup_logger(name: str, formatter: logging.Formatter | None = basic_formatter):
    if loggers.get(name) is not None:
        return loggers.get(name)

    handler = logging.StreamHandler()
    handler.setFormatter(formatter)

    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    logger.addHandler(handler)
    return logger
