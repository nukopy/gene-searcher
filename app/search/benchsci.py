import aiohttp

# from app.client import fetch
from app.constants import DATA_SOURCE_NAME_BENCHSCI
from app.logger import create_logger

logger = create_logger(__name__)


async def search_benchsci(session: aiohttp.ClientSession, query: str) -> (str, dict):
    """
    BenchSci
    """

    try:
        # TODO: BenchSci の API を叩く
        api_url = "https://benchsci.com/api/v1/search"
        res = {}

        return (DATA_SOURCE_NAME_BENCHSCI, res)
    except aiohttp.ClientError as e:
        # msg = f"Error on search_benchsci: failed to fetch data from {api_url} with status {res.status} due to client error"
        msg = f"Error on search_benchsci: failed to fetch data from {api_url} due to client error"
        logger.error(msg)

        raise Exception(f"{msg}: {e}") from e
    except Exception as e:
        msg = f"Error on search_benchsci: failed to fetch data from {api_url} due to unexpected error"
        logger.error(msg)

        raise Exception(f"{msg}: {e}") from e
