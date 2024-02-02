import streamlit as st

from app.constants import (
    DATA_SOURCE_NAME_BIOGPS,
)
from app.logger import create_logger

logger = create_logger(__name__)


def tab_inner_biogps(query: str, result: dict):
    st.markdown(f"### {DATA_SOURCE_NAME_BIOGPS}")
    data_biogps = result.get(DATA_SOURCE_NAME_BIOGPS, None)

    # fetch 時にエラーが発生した場合は早期リターン
    if isinstance(data_biogps, Exception):
        st.error(f"Error on search: `{query}`\n\n{data_biogps}", icon="🚨")
        return

    # data を result から取得できなかった場合は早期リターン
    if data_biogps is None or len(data_biogps) == 0:
        st.warning(f"No data found by query: `{query}`", icon="⚠️")
        return

    # TODO: API からデータ取得
    # TODO: データを可視化
    st.info("TODO: fetch & visualize data")
