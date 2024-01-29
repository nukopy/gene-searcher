import asyncio
import time
from typing import Tuple, Union

import aiohttp
import streamlit as st

from app.constants import (
    DATA_SOURCE_NAME_BENCHSCI,
    DATA_SOURCE_NAME_BIOGPS,
    DATA_SOURCE_NAME_DICE,
    DATA_SOURCE_NAME_HUMAN_PROTEIN_ATLAS,
)
from app.logger import create_logger
from app.search.benchsci import search_benchsci
from app.search.biogps import search_biogps
from app.search.dice import search_dice
from app.search.human_protein_atlas import search_hpa

logger = create_logger(__name__)

ResultType = Union[Tuple[str, dict], Exception]


async def _search(query: str) -> (dict, float):
    logger.info(f"start searching by query '{query}'...")
    start = time.time()

    # start async tasks
    global session
    tasks = []
    results: list[(str, dict)] = []
    async with aiohttp.ClientSession() as session:
        # FIXME: asyncio.TaskGroup のエラーハンドリング必要？多分必要なさそうだけど
        # ref: https://gihyo.jp/article/2022/10/monthly-python-2210

        # fetch from Human Protein Atlas
        tasks.append(search_hpa(session, query))

        # fetch from DICE
        tasks.append(search_dice(session, query))

        # fetch from BioGPS
        tasks.append(search_biogps(session, query))

        # fetch from BenchSci
        tasks.append(search_benchsci(session, query))

        # await all tasks
        results: list[ResultType] = await asyncio.gather(*tasks, return_exceptions=True)

    # extract each result
    data: dict[str, Union[dict, Exception]] = {}

    # caution: result の結果の順序は tasks.append した順番になるので注意
    # FIXME: もうちょっときれいに書けないかな。raise しないで Exception を戻り値にするとか
    for db_name, result in zip(
        [
            DATA_SOURCE_NAME_HUMAN_PROTEIN_ATLAS,
            DATA_SOURCE_NAME_DICE,
            DATA_SOURCE_NAME_BIOGPS,
            DATA_SOURCE_NAME_BENCHSCI,
        ],
        results,
    ):
        if isinstance(result, Exception):
            logger.error(f"Error on _search query '{query}': {result}")
            data[db_name] = result
            continue

        _, res = result
        data[db_name] = res

    end = time.time()
    diff = end - start

    logger.info(f"data: {data}")
    logger.info(f"end searching by query '{query}' (takes {diff:.4f} sec)")

    return data, end - start


@st.cache_data
def search(query: str) -> (dict, float):
    """sync wrapper for caching API responses on streamlit"""
    return asyncio.run(_search(query))
