import streamlit as st

from app.components.tabs.tab_search_result_rna_biogps import tab_inner_biogps
from app.components.tabs.tab_search_result_rna_dice import tab_inner_dice
from app.components.tabs.tab_search_result_rna_hpa import tab_inner_hpa
from app.constants import (
    MESSAGE_BEFORE_SEARCH,
)
from app.logger import create_logger

logger = create_logger(__name__)


def tab_search_result_rna(heading: str, query: str, result: dict):
    # search result
    if result is None:
        st.markdown(MESSAGE_BEFORE_SEARCH)
        return

    # The Human Protein Atlas
    tab_inner_hpa(query, result)
    st.divider()

    # DICE
    tab_inner_dice(query, result)
    st.divider()

    # BioGPS
    tab_inner_biogps(query, result)
