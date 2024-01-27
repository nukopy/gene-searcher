import aiohttp


async def fetch(
    session: aiohttp.ClientSession,
    url: str,
    params: dict = None,
    headers: dict = None,
) -> dict:
    res = await session.get(url, params=params, headers=headers)
    data = await res.json()

    return data
