import aiohttp

from app.logger import create_logger

logger = create_logger(__name__)


async def fetch(
    session: aiohttp.ClientSession,
    url: str,
    params: dict = None,
    headers: dict = None,
    timeout_seconds: int = 30,
) -> dict:
    # setup HTTP headers
    default_headers = {
        "Content-Type": "application/json",
    }
    if headers is None:
        headers = default_headers
    else:
        headers = {**default_headers, **headers}

    # fetch data
    try:
        res = await session.get(
            url, params=params, headers=headers, timeout=timeout_seconds
        )
        res.raise_for_status()  # raise error if status is not 200-299
        logger.info(f"fetch data successfully from {res.url}")
        data = await res.json()

        return data
    except aiohttp.ClientError as e:
        msg = f"Error on fetch: failed to fetch data from {url} with status {res.status} due to client error"
        logger.error(msg)

        raise Exception(msg) from e
    except Exception as e:
        msg = f"Error on fetch: failed to fetch data from {url} due to unexpected error"
        logger.error(msg)

        raise Exception(msg) from e
