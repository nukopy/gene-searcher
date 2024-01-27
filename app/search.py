import asyncio
import time

import aiohttp
import streamlit as st
from constants import DATA_SOURCE_NAME_HUMAN_PROTEIN_ATLAS


async def fetch(
    session: aiohttp.ClientSession,
    url: str,
    params: dict = None,
    headers: dict = None,
) -> dict:
    res = await session.get(url, params=params, headers=headers)
    data = await res.json()

    return data


async def search_hpa(session: aiohttp.ClientSession, query: str) -> (str, dict):
    api_url = "https://www.proteinatlas.org/api/search_download.php"
    # ref: https://www.proteinatlas.org/api/search_download.php?search=%22IL2RA%22&format=json&columns=g,gs,rnatsm,rnatd&compress=no
    params = {
        "search": query,
        "format": "json",
        "columns": "g,gs,rnatsm,rnatd",
        "compress": "no",
    }
    headers = {"Content-Type": "application/json"}

    return DATA_SOURCE_NAME_HUMAN_PROTEIN_ATLAS, await fetch(
        session, api_url, params, headers
    )


async def _search(query: str) -> (dict, float):
    print("start searching...")
    start = time.time()

    # start async tasks
    global session
    tasks = []
    results: list[(str, dict)] = []
    async with aiohttp.ClientSession() as session:
        # for Human Protein Atlas
        tasks.append(search_hpa(session, query))

        # for Other Databases
        # TODO

        # await all tasks
        results = await asyncio.gather(*tasks)

    # extract each result
    data: dict[str, dict] = {}
    for name, result in results:
        print(f"result from {name}: {result}")
        data[name] = result

    end = time.time()
    diff = end - start
    print(f"end searching({diff:.4f} sec)")

    return data, end - start


@st.cache_data
def search(query: str) -> (dict, float):
    """sync wrapper for caching API responses on streamlit"""
    return asyncio.run(_search(query))
