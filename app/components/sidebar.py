import streamlit as st

from app.constants import DATA_SOURCES


def sidebar():
    st.sidebar.markdown("# Data Sources")
    for db in DATA_SOURCES:
        name = db.get("name", "Unknown")
        version = db.get("version", "Unknown")
        url = db.get("url", "Unknown")
        db_text = f"- [{name}]({url}) {version}\n"

        # release date
        release_date = db.get("release_date", "Unknown")
        release_data_text = f"  - Release date: {release_date}"

        # datasets
        datasets = db.get("datasets", [])
        datasets_text = "  - Datasets:\n"
        if len(datasets) > 0:
            for dataset in datasets:
                datasets_text += f"    - {dataset}\n"

        # write
        st.sidebar.markdown(
            f"""
{db_text}
{release_data_text}
{datasets_text if len(datasets) > 0 else ""}
"""
        )
