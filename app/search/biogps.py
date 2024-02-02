import aiohttp

# from app.client import fetch
from app.constants import DATA_SOURCE_NAME_BENCHSCI
from app.errors import FetchClientError, FetchClientResponseError, FetchUnexpectedError
from app.logger import create_logger

logger = create_logger(__name__)


async def search_biogps(session: aiohttp.ClientSession, query: str) -> (str, dict):
    """
    BioGPS
    """

    try:
        # TODO: BioGPS の API を叩く
        api_url = "https://biogps.org/api/search.json"
        res = {}

        return (DATA_SOURCE_NAME_BENCHSCI, res)
    except FetchClientResponseError as e:
        msg = f"Error on search_biogps: failed to fetch data from {api_url} due to response error"
        logger.error(msg)

        raise Exception(f"{msg}: {e}") from e
    except FetchClientError as e:
        msg = f"Error on search_biogps: failed to fetch data from {api_url} due to client error"
        logger.error(msg)

        raise Exception(f"{msg}: {e}") from e
    except FetchUnexpectedError as e:
        msg = f"Error on search_biogps: failed to fetch data from {api_url} due to unexpected error"
        logger.error(msg)

        raise Exception(f"{msg}: {e}") from e
