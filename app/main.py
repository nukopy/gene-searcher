import asyncio
import time

import aiohttp
import streamlit as st
from constants import (
    DATA_SOURCE_NAME_HUMAN_PROTEIN_ATLAS,
    DATA_SOURCES,
)


def sidebar():
    st.sidebar.markdown("# Data Sources")
    for db in DATA_SOURCES:
        name = db.get("name", "Unknown")
        version = db.get("version", "Unknown")
        url = db.get("url", "Unknown")
        st.sidebar.markdown(f"- [{name}]({url}) v{version}")


async def contents():
    # header
    st.markdown(
        """
        # Gene Searcher

        Gene Searcher is a tool for searching for genes and their associated
        """
    )

    # search input
    query_type = st.radio(
        "Query type",
        ["Gene name", "Ensemble ID"],
        index=0,
    )
    if query_type == "Gene name":
        placeholder = "Gene name (e.g. IL2RA)"
    else:
        placeholder = "Ensemble ID (e.g. ENSG00000134460)"
    query = st.text_input("Query", placeholder=placeholder)

    # search button to trigger search
    button = st.button("Search")
    result, diff = None, None
    if button:
        with st.spinner("Searching..."):
            result, diff = await search(query)

    # search results
    st.markdown("## Search Results")
    if diff is not None:
        st.markdown(f"takes {diff:.4f} seconds")

    # Ensemble は表示しない
    tab_list = [
        db.get("name", "Unknown") for db in DATA_SOURCES if db.get("name") != "Ensembl"
    ]
    tab_list.append("Other Databases")  # for TODO
    tab1, tab2 = st.tabs(tab_list)

    # The Human Protein Atlas
    message_before_search = "Please input query and click search button."
    with tab1:
        st.markdown("### The Human Protein Atlas")

        # search result
        if result is None:
            st.markdown(message_before_search)
        else:
            st.markdown(f"Takes time: {diff:.4f} sec")
            # TODO: リストで返ってくるので、リストの最初の要素を取得（検索候補は se）
            # TODO: API からデータ取得
            # TODO: データを可視化

    # Other Databases
    with tab2:
        st.markdown("### Other Databases")

        # search result
        if result is None:
            st.markdown(message_before_search)
        else:
            st.markdown(f"Takes time: {diff:.4f} sec")


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


async def search(query: str) -> (dict, float):
    print("start searching...")
    start = time.time()

    # trigger request tasks
    tasks = []
    results: list[(str, dict)] = []
    data: dict[str, dict] = {}
    async with aiohttp.ClientSession() as session:
        # for Human Protein Atlas
        tasks.append(search_hpa(session, query))

        # for Other Databases
        # TODO

        # await all tasks
        results = await asyncio.gather(*tasks)

        # extract each result
        for name, result in results:
            print(f"result from {name}: {result}")
            data[name] = result

    end = time.time()
    diff = end - start
    print(f"end searching({diff:.4f} sec)")

    return data, end - start


async def main():
    sidebar()
    await contents()


asyncio.run(main())
