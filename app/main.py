import streamlit as st
from constants import (
    DATA_SOURCE_NAME_HUMAN_PROTEIN_ATLAS,
    DATA_SOURCES,
)
from search import search


def meta():
    st.set_page_config(
        page_title="Gene Searcher",
        page_icon="🧬",
        layout="wide",
        initial_sidebar_state="auto",
    )


def sidebar():
    st.sidebar.markdown("# Data Sources")
    for db in DATA_SOURCES:
        name = db.get("name", "Unknown")
        version = db.get("version", "Unknown")
        url = db.get("url", "Unknown")
        st.sidebar.markdown(f"- [{name}]({url}) v{version}")


def contents():
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
            result, diff = search(query)

    # search results
    st.markdown("## Search Results")
    if diff is not None:
        st.markdown(f"takes {diff:.4f} seconds")

    # Ensemble は表示しない
    tab_list = [
        db.get("name", "Unknown") for db in DATA_SOURCES if db.get("name") != "Ensembl"
    ]
    # FIXME: 他のデータベースが追加されたら Other Databases は必要なくなるので、その時に消す
    tab_list.append("Other Databases")

    # create tabs
    tab1, tab2 = st.tabs(tab_list)

    # The Human Protein Atlas
    message_before_search = "Please input query and click search button."
    with tab1:
        st.markdown("### The Human Protein Atlas")

        # search result
        if result is None:
            st.markdown(message_before_search)
        else:
            data = result.get(DATA_SOURCE_NAME_HUMAN_PROTEIN_ATLAS, None)

            if data is None or len(data) == 0:
                st.markdown(f"No data found by query: {query}")
            # TODO: リストで返ってくるので、リストの最初の要素を取得（検索候補は select で選べるように）
            # TODO: API からデータ取得
            # TODO: データを可視化

    # Other Databases
    with tab2:
        st.markdown("### Other Databases")

        # search result
        if result is None:
            # st.markdown(message_before_search)
            st.markdown("This tab is under construction.")
        else:
            st.markdown("This tab is under construction.")


def main():
    meta()
    sidebar()
    contents()


main()
