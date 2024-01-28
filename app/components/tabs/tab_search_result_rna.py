import json

import pandas as pd
import plotly.graph_objects as go
import streamlit as st

from app.constants import (
    DATA_SOURCE_NAME_BIOGPS,
    DATA_SOURCE_NAME_DICE,
    DATA_SOURCE_NAME_HUMAN_PROTEIN_ATLAS,
    MESSAGE_BEFORE_SEARCH,
)
from app.logger import create_logger
from app.plot.human_protein_atlas import TISSUE_PLOT_ATTRIBUTES, modify_tissue_data_key
from app.search.human_protein_atlas import (
    COLUMNS_HUMAN_PROTEIN_ATLAS,
    COLUMNS_RNA_EXPRESSION,
)

logger = create_logger(__name__)


def tab_inner_hpa(query: str, result: dict):
    st.markdown(f"### {DATA_SOURCE_NAME_HUMAN_PROTEIN_ATLAS}")
    data_hpa = result.get(DATA_SOURCE_NAME_HUMAN_PROTEIN_ATLAS, None)

    # data が result から取得できなかった場合は早期リターン
    if data_hpa is None or len(data_hpa) == 0:
        st.markdown(f"No data found by query: `{query}`")
        return

    # select gene
    gene_select_labels = [
        f'{x["Gene"]} (synonyms: {", ".join(x["Gene synonym"])})' for x in data_hpa
    ]
    st.markdown(f"{len(data_hpa)} genes found by query: `{query}`")
    selected_gene_label = st.selectbox("Select gene", options=gene_select_labels)

    # extract gene name from selected_gene_label, from "IL2RA (synonyms: CD25, IDDM10, IL2R)" to "IL2RA"
    gene = selected_gene_label.split(" ")[0]
    selected_gene_data = list(filter(lambda x: x["Gene"] == gene, data_hpa))[0]

    # write gene info
    gene_name = selected_gene_data.get("Gene", "Unknown")
    ensembl_id = selected_gene_data.get("Ensembl", "Unknown")
    st.markdown(
        f"""
        General Information:

        - Gene: `{selected_gene_data.get("Gene", "Unknown")}`
        - Gene synonyms: {", ".join(selected_gene_data.get("Gene synonym", []))}
        - Gene Ensembl ID: `{selected_gene_data.get("Ensembl", "Unknown")}`
        - Gene description: {selected_gene_data.get("Gene description", "Unknown")}
        """
    )

    # - Tissue
    # extract tissue metadata
    keys = list(COLUMNS_HUMAN_PROTEIN_ATLAS.keys())
    tissue_metadata = {k: v for k, v in selected_gene_data.items() if k in keys}
    logger.info(f"tissue_metadata: {tissue_metadata}")

    # extract only RNA expression data
    keys = list(COLUMNS_RNA_EXPRESSION.keys())
    # note: nTPM is str from API response, so convert to float
    tissue_data: dict[str, float] = {
        k: float(v) for k, v in selected_gene_data.items() if k in keys
    }

    # modify keys
    # extract tissue name & capitalize: "Tissue RNA - hypothalamus [nTPM]" -> "Hypothalamus"
    tissue_data = {modify_tissue_data_key(k): v for k, v in tissue_data.items()}

    # tissue, nTPM を TISSUE_PLOT_ATTRIBUTES の順序に基づいて並び替える
    col_tissues = [t["tissue"] for t in TISSUE_PLOT_ATTRIBUTES]
    col_tissue_nTPMs = [tissue_data[t["tissue"]] for t in TISSUE_PLOT_ATTRIBUTES]
    col_organs = [t["organ"] for t in TISSUE_PLOT_ATTRIBUTES]
    colors = [t["color"] for t in TISSUE_PLOT_ATTRIBUTES]

    # create dataframe
    tissue_data = {
        "tissue": col_tissues,
        "organ": col_organs,
        "nTPM": col_tissue_nTPMs,
    }
    df_tissue = pd.DataFrame(tissue_data)

    # create link
    link = f"https://www.proteinatlas.org/{ensembl_id}-{gene_name}/tissue"

    # write tissue metadata
    st.markdown(
        f"""
        #### Tissue

        Data source: {link}

        - Tissue expression cluster (RNA): {tissue_metadata.get("Tissue expression cluster", "Unknown")}
        - Tissue specificity (RNA): {tissue_metadata.get("RNA tissue specificity", "Unknown")}
        - Tissue distribution (RNA): {tissue_metadata.get("RNA tissue distribution", "Unknown")}
        """
    )

    # visualize data
    # - create figure
    logger.info(f"df_tissue shape: {df_tissue.shape}")
    logger.info(f"df_tissue columns: {df_tissue.columns}")
    graph_object = go.Bar(
        x=df_tissue["tissue"],  # TissueカラムのデータをX軸に設定
        y=df_tissue["nTPM"],  # nTPMカラムのデータをY軸に設定
        marker_color=colors,  # 色を設定
        opacity=0.8,  # 透明度を設定
        # for tooltip
        customdata=df_tissue["organ"],  # tooltip のためのデータを設定
        hovertemplate="<b>Tissue: %{x}</b><br>nTPM: %{y}<br>Organ: %{customdata}<extra></extra>",
    )
    fig = go.Figure(graph_object)

    # - fig settings
    fig.update_layout(
        title="RNA expression of tissues (Concensus dataset)",
        xaxis_tickangle=-60,
        xaxis_title="tissue",
        yaxis_title="nTPM",
        hoverlabel={
            "align": "left",
            "bgcolor": "rgba(36,35,35,0.8)",
            "font_color": "white",
            "font_size": 14,
            "font_family": "'Open Sans', sans-serif",
        },
    )

    # write chart
    st.plotly_chart(fig, use_container_width=True)

    # write table for download
    toggle = st.toggle("Show source data of above chart")
    if toggle:
        st.markdown(
            "As you mouse over the table below, you can download CSV file from popup."
        )
        st.dataframe(df_tissue, hide_index=True)


def tab_inner_dice(query: str, result: dict):
    st.markdown(f"### {DATA_SOURCE_NAME_DICE}")
    data_dice = []
    if data_dice is None or len(data_dice) == 0:
        st.markdown(f"No data found by query: `{query}`")
        return

    # TODO: API からデータ取得
    # TODO: データを可視化


def tab_inner_biogps(query: str, result: dict):
    st.markdown(f"### {DATA_SOURCE_NAME_BIOGPS}")
    data_biogps = []
    if data_biogps is None or len(data_biogps) == 0:
        st.markdown(f"No data found by query: `{query}`")
        return

    # TODO: API からデータ取得
    # TODO: データを可視化


def tab_search_result_rna(heading: str, query: str, result: dict):
    # search result
    logger.info(f"result: {json.dumps(result, indent=2)}")
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
