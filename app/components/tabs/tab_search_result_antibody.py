import streamlit as st

from app.constants import (
    DATA_SOURCE_NAME_BENCHSCI,
    MESSAGE_BEFORE_SEARCH,
)
from app.logger import create_logger

logger = create_logger(__name__)


def tab_innser_benchsci(query: str, result: dict):
    st.markdown(f"#### {DATA_SOURCE_NAME_BENCHSCI}")
    data_benchsci = result.get(DATA_SOURCE_NAME_BENCHSCI, None)

    # fetch 時にエラーが発生した場合は早期リターン
    if isinstance(data_benchsci, Exception):
        st.error(f"Error on search: `{query}`\n\n{data_benchsci}", icon="🚨")
        return

    # data を result から取得できなかった場合は早期リターン
    if data_benchsci is None or len(data_benchsci) == 0:
        st.warning(f"No data found by query: `{query}`", icon="⚠️")
        return

    # TODO: API からデータ取得
    # TODO: データを可視化
    st.info("TODO: fetch & visualize data")


def tab_search_result_antibody(heading: str, query: str, result: dict):
    st.markdown(f"### {heading}")

    # search result
    if result is None:
        st.markdown(MESSAGE_BEFORE_SEARCH)
        return

    # BenchSci
    tab_innser_benchsci(query, result)
