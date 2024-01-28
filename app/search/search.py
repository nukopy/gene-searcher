import asyncio
import time

import aiohttp
import streamlit as st

from app.logger import create_logger
from app.search.human_protein_atlas import search_hpa

logger = create_logger(__name__)


async def _search(query: str) -> (dict, float):
    logger.info("start searching...")
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
        logger.info(f"add result from '{name}' to data")
        data[name] = result

    end = time.time()
    diff = end - start
    logger.info(f"end searching (takes {diff:.4f} sec)")

    return data, end - start


@st.cache_data
def search(query: str) -> (dict, float):
    """sync wrapper for caching API responses on streamlit"""
    return asyncio.run(_search(query))
