import sys
from logging import INFO, Formatter, Handler, Logger, StreamHandler, getLogger
from typing import IO, Optional

from app.errors import LoggerCreationError, LoggerStreamHandlerCreationError

DEFAULT_LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
DEFAULT_LOG_DATE_FORMAT = "%Y-%m-%dT%H:%M:%S"


def create_stream_handler(
    level: int,
    output: IO[str],
    log_format: str,
    date_format: str,
) -> StreamHandler:
    """Create and configure a StreamHandler."""

    try:
        handler = StreamHandler(output)
        fmt = Formatter(log_format, date_format)
        handler.setFormatter(fmt)
        handler.setLevel(level)

        return handler
    except Exception as e:
        raise LoggerStreamHandlerCreationError(
            f"Failed to create StreamHandler: {e}"
        ) from e


# ref: https://hackers-high.com/python/logging-overview/
def create_logger(
    name: str,
    level: int = INFO,
    handlers: Optional[list[Handler]] = None,
    log_format: str = DEFAULT_LOG_FORMAT,
    date_format: str = DEFAULT_LOG_DATE_FORMAT,
) -> Logger:
    try:
        # get logger
        logger = getLogger(name)

        # clear handlers
        for h in logger.handlers[:]:
            logger.removeHandler(h)

        # set log level
        logger.setLevel(level)

        # setup handler
        if handlers is not None and len(handlers) > 0:
            for handler in handlers:
                logger.addHandler(handler)
        else:
            # default handler is StreamHandler with sys.stdout
            handler = create_stream_handler(level, sys.stdout, log_format, date_format)

        # set handler to logger
        logger.addHandler(handler)

        # disable propagation
        logger.propagate = False

        return logger
    except Exception as e:
        raise LoggerCreationError(
            f"Failed to create logger of module '{name}': {e}"
        ) from e
