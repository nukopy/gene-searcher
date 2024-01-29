import aiohttp

# from app.client import fetch
from app.constants import DATA_SOURCE_NAME_BENCHSCI
from app.logger import create_logger

logger = create_logger(__name__)


async def search_dice(session: aiohttp.ClientSession, query: str) -> (str, dict):
    """
    DICE
    """

    try:
        # TODO: DICE の API を叩く
        api_url = "https://dice-database.org/api/search"
        res = {}
        res.status = 200

        return (DATA_SOURCE_NAME_BENCHSCI, {})
    except aiohttp.ClientError as e:
        msg = f"Error on search_dice: failed to fetch data from {api_url} with status {res.status} due to client error"
        logger.error(msg)

        raise Exception(msg) from e
    except Exception as e:
        msg = f"Error on search_dice: failed to fetch data from {api_url} due to unexpected error"
        logger.error(msg)

        raise Exception(msg) from e
