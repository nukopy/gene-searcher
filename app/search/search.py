import asyncio
import time

import aiohttp
import streamlit as st
from human_protein_atlas import search_hpa


async def fetch(
    session: aiohttp.ClientSession,
    url: str,
    params: dict = None,
    headers: dict = None,
) -> dict:
    res = await session.get(url, params=params, headers=headers)
    data = await res.json()

    return data


async def _search(query: str) -> (dict, float):
    print("start searching...")
    start = time.time()

    # start async tasks
    global session
    tasks = []
    results: list[(str, dict)] = []
    async with aiohttp.ClientSession() as session:
        # fetch from Human Protein Atlas
        tasks.append(search_hpa(session, query))

        # fetch from DICE
        # TODO

        # fetch from BioGPS
        # TODO

        # fetch from BenchSci
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
    print(f"end searching ({diff:.4f} sec)")

    return data, end - start


@st.cache_data
def search(query: str) -> (dict, float):
    """sync wrapper for caching API responses on streamlit"""
    return asyncio.run(_search(query))
