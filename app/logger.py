import sys
from logging import INFO, Formatter, Logger, StreamHandler, getLogger

DEFAULT_LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
DEFAULT_LOG_DATE_FORMAT = "%Y-%m-%dT%H:%M:%S"


# ref: https://hackers-high.com/python/logging-overview/
def create_logger(
    name: str,
    level: int = INFO,
    log_format: str = DEFAULT_LOG_FORMAT,
    data_format: str = DEFAULT_LOG_DATE_FORMAT,
) -> Logger:
    # get logger
    logger = getLogger(name)

    # clear handlers
    if logger.hasHandlers():
        logger.handlers.clear()

    # set log level
    logger.setLevel(level)

    # create handler
    handler = StreamHandler(sys.stdout)
    handler.setLevel(level)
    fmt = Formatter(log_format, data_format)
    handler.setFormatter(fmt)

    # add handler
    logger.addHandler(handler)

    # disable propagation
    logger.propagate = False

    return logger
