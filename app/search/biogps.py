import aiohttp

# from app.client import fetch
from app.constants import DATA_SOURCE_NAME_BENCHSCI
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
        res.status = 200

        return (DATA_SOURCE_NAME_BENCHSCI, {})
    except aiohttp.ClientError as e:
        msg = f"Error on search_biogps: failed to fetch data from {api_url} with status {res.status} due to client error"
        logger.error(msg)

        raise Exception(msg) from e
    except Exception as e:
        msg = f"Error on search_biogps: failed to fetch data from {api_url} due to unexpected error"
        logger.error(msg)

        raise Exception(msg) from e
