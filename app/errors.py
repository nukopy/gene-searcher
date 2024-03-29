# ------------------------------------------------------------------------
# for logger
# ------------------------------------------------------------------------


class LoggerCreationError(Exception):
    """Error occurred during creating logger."""


class LoggerStreamHandlerCreationError(Exception):
    """Error occurred during creating StreamHandler."""


# ------------------------------------------------------------------------
# for HTTP client
# ------------------------------------------------------------------------


class FetchClientResponseError(Exception):
    """
    Client status error occurred during fetching data.
    This error is raised with `res.raise_for_status()` when status >= 400.
    """


class FetchClientError(Exception):
    """Client error occurred during fetching data."""


class FetchUnexpectedError(Exception):
    """Unexpected error occurred during fetching data."""


# ------------------------------------------------------------------------
# for search
# ------------------------------------------------------------------------


class FetchFromMyGeneError(Exception):
    """Not found on BioGPS."""
