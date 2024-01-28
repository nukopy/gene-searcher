import streamlit as st

from app.constants import (
    DATA_SOURCE_NAME_BENCHSCI,
    MESSAGE_BEFORE_SEARCH,
)
from app.logger import create_logger

logger = create_logger(__name__)


def tab_innser_benchsci(query: str, result: dict):
    st.markdown(f"#### {DATA_SOURCE_NAME_BENCHSCI}")
    data_benchsci = []
    if data_benchsci is None or len(data_benchsci) == 0:
        st.markdown(f"No data found by query: `{query}`")
        return

    # TODO: API からデータ取得
    # TODO: データを可視化


def tab_search_result_vaccine(heading: str, query: str, result: dict):
    st.markdown(f"### {heading}")

    # search result
    if result is None:
        st.markdown(MESSAGE_BEFORE_SEARCH)
        return

    # BenchSci
    tab_innser_benchsci(query, result)
