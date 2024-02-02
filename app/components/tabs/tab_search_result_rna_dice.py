import io

import streamlit as st

from app.constants import (
    DATA_SOURCE_NAME_DICE,
)
from app.logger import create_logger

logger = create_logger(__name__)


def tab_inner_dice(query: str, result: dict):
    st.markdown(f"### {DATA_SOURCE_NAME_DICE}")
    data_dice = result.get(DATA_SOURCE_NAME_DICE, None)

    # fetch 時にエラーが発生した場合は早期リターン
    if isinstance(data_dice, Exception):
        st.error(f"Error on search: `{query}`\n\n{data_dice}", icon="🚨")
        return

    # data を result から取得できなかった場合は早期リターン
    if data_dice is None or len(data_dice) == 0:
        st.warning(f"""No data found by query: `{query}`""", icon="⚠️")
        st.warning(
            """
            Status of search results may be `No data found` if you search by gene synonyms and Ensembl ID.

            Now, gene-searcher doesn't support search by gene synonyms and Ensembl ID on DICE.
            You can search by query like `IL2RA`, but cannot search by like `CD25` and `ENSG00000134460`.

            **Please search by gene symbol name**.
            """
        )
        return

    # write gene info
    # TBD: API から取得できるのは CSV データのみなので、ここでは遺伝子情報を表示しない

    # write link
    link = f"https://dice-database.org/genes/{query}"
    st.markdown(f"Data source: {link}")

    # データの前処理
    # CSV バイナリデータを BytesIO に変換
    csv_data = io.BytesIO(data_dice)

    # BytesIO から pandas.DataFrame に変換

    # TODO: データを可視化
    st.info("TODO: fetch & visualize data")
