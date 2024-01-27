import streamlit as st
from constants import (
    DATA_SOURCE_NAME_BENCHSCI,
    DATA_SOURCE_NAME_BIOGPS,
    DATA_SOURCE_NAME_DICE,
    DATA_SOURCE_NAME_HUMAN_PROTEIN_ATLAS,
)
from search import search

MESSAGE_BEFORE_SEARCH = "Please input query and click search button."


def header():
    # header
    st.markdown(
        """
        # Gene Searcher

        Gene Searcher is a tool for searching for genes and their associated
        """
    )


def search_input() -> str:
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
            result, diff = search(query)

    return query, result, diff


def search_result(query: str, result: dict, diff: float):
    st.markdown("## Search Results")

    # 検索にかかった時間
    if diff is not None:
        st.markdown(f"takes {diff:.4f} seconds")

    # create tabs
    tab_list = [
        "RNA Expression Data",
        "Vaccine List",
    ]
    tab_rna, tab_vaccine = st.tabs(tab_list)
    with tab_rna:
        heading_rna = tab_list[0]
        st.markdown(f"### {heading_rna}")

        # search result
        if result is None:
            st.markdown(MESSAGE_BEFORE_SEARCH)
        else:
            # The Human Protein Atlas
            st.markdown(f"#### {DATA_SOURCE_NAME_HUMAN_PROTEIN_ATLAS}")
            data_hpa = result.get(DATA_SOURCE_NAME_HUMAN_PROTEIN_ATLAS, None)

            if data_hpa is None or len(data_hpa) == 0:
                st.markdown(f"No data found by query: `{query}`")
            # TODO: リストで返ってくるので、リストの最初の要素を取得（検索候補は select で選べるように）
            # TODO: API からデータ取得
            # TODO: データを可視化

            # DICE
            st.markdown(f"#### {DATA_SOURCE_NAME_DICE}")
            data_dice = []
            if data_dice is None or len(data_dice) == 0:
                st.markdown(f"No data found by query: `{query}`")
            else:
                pass
                # TODO: API からデータ取得
                # TODO: データを可視化

            # BioGPS
            st.markdown(f"#### {DATA_SOURCE_NAME_BIOGPS}")
            data_biogps = []
            if data_biogps is None or len(data_biogps) == 0:
                st.markdown(f"No data found by query: `{query}`")
            else:
                pass
                # TODO: API からデータ取得
                # TODO: データを可視化

    # Other Databases
    with tab_vaccine:
        heading_vaccine = tab_list[1]
        st.markdown(f"### {heading_vaccine}")

        # search result
        if result is None:
            st.markdown(MESSAGE_BEFORE_SEARCH)
        else:
            # BenchSci
            st.markdown(f"#### {DATA_SOURCE_NAME_BENCHSCI}")


def contents():
    # header
    header()

    # search input
    query, result, diff = search_input()

    # search results
    search_result(query, result, diff)
