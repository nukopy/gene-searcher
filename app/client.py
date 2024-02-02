import aiohttp

from app.errors import FetchClientError, FetchClientResponseError, FetchUnexpectedError
from app.logger import create_logger

logger = create_logger(__name__)

DEFAULT_HEADERS = {
    "Content-Type": "application/json",
}
DEFAULT_TIMEOUT_SECONDS = 30


async def fetch(
    session: aiohttp.ClientSession,
    url: str,
    params: dict = None,
    headers: dict = None,
    timeout_seconds: int = DEFAULT_TIMEOUT_SECONDS,
) -> aiohttp.ClientResponse:
    # setup HTTP headers
    headers = {**DEFAULT_HEADERS, **(headers or {})}

    # fetch data
    try:
        res = await session.get(
            url, params=params, headers=headers, timeout=timeout_seconds
        )
        res.raise_for_status()  # raise error if status is not 200-299
        logger.info(f"fetch data successfully from {res.url}")

        return res
    except aiohttp.ClientResponseError as e:
        msg = f"Error on fetch: failed to fetch data from {url} with status {e.status} due to response error"
        logger.error(msg)

        raise FetchClientResponseError(msg) from e
    except aiohttp.ClientError as e:
        msg = f"Error on fetch: failed to fetch data from {url} due to client error"
        logger.error(msg)

        raise FetchClientError(msg) from e
    except Exception as e:
        msg = f"Error on fetch: failed to fetch data from {url} due to unexpected error"
        logger.error(msg)

        raise FetchUnexpectedError(msg) from e
