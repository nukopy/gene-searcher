import streamlit as st

from app.components.tabs import (
    tab_search_result_rna,
    tab_search_result_vaccine,
)
from app.constants import (
    TAB_NAME_RNA_EXPRESSION_DATA,
    TAB_NAME_VACCINE_LIST,
)
from app.logger import create_logger
from app.search.search import search

logger = create_logger(__name__)


def session_state_init():
    if "result" not in st.session_state and "diff" not in st.session_state:
        st.session_state["result"] = None
        st.session_state["diff"] = None


def header():
    st.header("# Gene Searcher")
    st.markdown(
        """
        Gene Searcher is a tool for searching for genes and their associated
        """
    )


def input_query() -> tuple:
    # search input
    # query_type = st.radio(
    #     "Query type",
    #     ["Gene name", "Ensemble ID"],
    #     index=0,
    # )
    # if query_type == "Gene name":
    #     placeholder = "Gene name (e.g. IL2RA)"
    # else:
    #     placeholder = "Ensemble ID (e.g. ENSG00000134460)"

    # search input
    # note: 各データベースの Web ページでは自由にクエリを使用できるので、一旦その仕様に合わせてクエリのタイプは区別せず入力する
    # placeholder = "Input gene symbol (e.g. IL2RA, CD25), Ensemble ID (e.g. ENSG00000134460), or keywords (e.g. 'lymphocyte activation')"
    placeholder = "Input gene symbol (e.g. IL2RA, ERBB2)"
    query = st.text_input("Query", placeholder=placeholder)

    # search button to trigger search
    is_button_clicked = st.button("Search")

    if query == "" or query is None:
        return is_button_clicked, "", None, None

    if is_button_clicked:
        with st.spinner("Searching..."):
            result, diff = search(query)
            st.session_state["result"] = result
            st.session_state["diff"] = diff

    return (
        is_button_clicked,
        query,
        st.session_state["result"],
        st.session_state["diff"],
    )


def search_result(is_button_clicked: bool, query: str, result: dict, diff: float):
    if is_button_clicked and query == "":
        st.warning("Please input query!", icon="⚠️")

    st.markdown("## Search Results from Databases")

    # 検索にかかった時間
    if diff is not None:
        st.markdown(f"search takes {diff:.2f} seconds")

    # create tabs
    tab_list = [
        TAB_NAME_RNA_EXPRESSION_DATA,
        TAB_NAME_VACCINE_LIST,
    ]
    tab_rna, tab_vaccine = st.tabs(tab_list)

    # RNA Expression Data
    with tab_rna:
        tab_search_result_rna(TAB_NAME_RNA_EXPRESSION_DATA, query, result)

    # Vaccine List
    with tab_vaccine:
        tab_search_result_vaccine(TAB_NAME_VACCINE_LIST, query, result)


def contents():
    session_state_init()

    # header
    header()

    # search input
    is_button_clicked, query, result, diff = input_query()

    # search results
    search_result(is_button_clicked, query, result, diff)
