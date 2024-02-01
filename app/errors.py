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


class SearchError(Exception):
    """Error occurred during searching data."""
