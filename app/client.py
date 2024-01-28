import aiohttp

from app.logger import create_logger

logger = create_logger(__name__)


async def fetch(
    session: aiohttp.ClientSession,
    url: str,
    params: dict = None,
    headers: dict = None,
) -> dict:
    res = await session.get(url, params=params, headers=headers)
    logger.info(f"fetch data from {res.url}")
    data = await res.json()

    return data
