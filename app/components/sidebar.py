import streamlit as st
from constants import DATA_SOURCES


def sidebar():
    st.sidebar.markdown("# Data Sources")
    for db in DATA_SOURCES:
        name = db.get("name", "Unknown")
        version = db.get("version", "Unknown")
        url = db.get("url", "Unknown")
        st.sidebar.markdown(f"- [{name}]({url}) v{version}")
