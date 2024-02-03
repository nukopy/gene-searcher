import io

import pandas as pd
import plotly.graph_objects as go
import streamlit as st

from app.constants import (
    CHART_BACKGROUND_COLOR,
    DATA_SOURCE_NAME_BIOGPS,
    DATA_SOURCE_NAME_MYGENEINFO,
)
from app.logger import create_logger
from app.search.biogps import BIOGPS_SUPPORT_DATASETS
from app.search.mygeneinfo import RESULT_KEY_GENE_ANOTATIONS
from app.search.search import search_biogps_sync

logger = create_logger(__name__)


def get_synonyms_string_from_gene_anotation(g: dict) -> str:
    synonyms = ""

    # get synonyms string like "CD25, IDDM10, IL2R" or "CD25"
    alias = g.get("alias", None)

    # alias は list または str の場合がある
    if alias is not None:
        if isinstance(alias, list):
            synonyms = ", ".join(alias)
        elif isinstance(alias, str):
            synonyms = alias

    return synonyms if synonyms else "Not found"


def get_gene_ensembl_id_from_gene_anotation(g: dict) -> str:
    ensemble_info = g.get("ensembl", None)
    if ensemble_info is not None:
        return ensemble_info.get("gene", "Unknown")

    return "Not found"


def tab_inner_biogps(query: str, result: dict):
    st.markdown(f"### {DATA_SOURCE_NAME_BIOGPS}")
    data_mygene = result.get(DATA_SOURCE_NAME_MYGENEINFO, None)

    # fetch 時にエラーが発生した場合は早期リターン
    if isinstance(data_mygene, Exception):
        st.error(f"Error on search: `{query}`\n\n{data_mygene}", icon="🚨")
        return

    # data を result から取得できなかった場合は早期リターン
    if data_mygene is None or len(data_mygene) == 0:
        st.warning(f"No data found on MyGene.info by query: `{query}`", icon="⚠️")
        return

    # data_biogps から MyGene.info の遺伝子アノテーションデータを取得
    gene_anotations = data_mygene.get(RESULT_KEY_GENE_ANOTATIONS, [])
    if len(gene_anotations) == 0:
        st.warning(
            f"No gene anotation data found from MyGene.info by query: `{query}`",
            icon="⚠️",
        )
        return

    # write num of search result
    st.markdown(f"{len(gene_anotations)} genes found by query: `{query}`")

    # --------------------------------------------------
    # select gene
    # --------------------------------------------------

    # get labels like "IL2RA (synonyms: CD25, IDDM10, IL2R)"
    gene_select_labels = []
    for g in gene_anotations:
        # get symbol like "IL2RA"
        gene = g["symbol"]

        # get synonyms like "CD25, IDDM10, IL2R" or "CD25"
        s = get_synonyms_string_from_gene_anotation(g)
        gene_select_labels.append(f"{gene} (synonyms: {s})")

    # get idx if query == gene["symbol"]
    idx = 0
    for i, g in enumerate(gene_anotations):
        if g["symbol"] == query:
            idx = i
            break

    # write gene select box
    selected_gene_label = st.selectbox(
        "Select gene", options=gene_select_labels, index=idx
    )
    selected_gene = selected_gene_label.split(" ")[0]

    # --------------------------------------------------
    # write gene info
    # --------------------------------------------------

    selected_gene_annotation = list(
        filter(lambda x: x["symbol"] == selected_gene, gene_anotations)
    )[0]  # 必ず一致する遺伝子が見つかるはず

    # extract gene annotation data
    symbol = selected_gene_annotation.get("symbol", "Unknown")
    ncbi_gene_id = selected_gene_annotation.get("_id", "Unknown")
    synonyms = get_synonyms_string_from_gene_anotation(selected_gene_annotation)
    description = selected_gene_annotation.get("name", "Unknown")
    gene_ensembl_id = get_gene_ensembl_id_from_gene_anotation(selected_gene_annotation)
    # e.g. http://biogps.org/#goto=genereport&id=2064
    link = f"http://biogps.org/gene/{ncbi_gene_id}"

    st.markdown(
        f"""
        #### General Information

        Data source: {link}

        - Gene: `{symbol}`
        - Gene synonyms: {synonyms}
        - NCBI Gene ID: `{ncbi_gene_id}`
        - Gene Ensembl ID: {r"`" + gene_ensembl_id + r"`" if gene_ensembl_id != "Not found" else "Not found"}
        - Gene description: {description}
        """
    )

    # --------------------------------------------------
    # select dataset and probeset
    # --------------------------------------------------

    st.markdown("#### Data")

    col_dataset, col_probeset = st.columns(2)

    # データセットの選択
    idx_dataset = col_dataset.selectbox(
        "Select dataset",
        options=range(len(BIOGPS_SUPPORT_DATASETS)),
        format_func=lambda x: BIOGPS_SUPPORT_DATASETS[x]["name"]
        + f" (ID: {BIOGPS_SUPPORT_DATASETS[x]['dataset_id']})",
    )
    selected_dataset_id = BIOGPS_SUPPORT_DATASETS[idx_dataset]["dataset_id"]
    selected_dataset_name = BIOGPS_SUPPORT_DATASETS[idx_dataset]["name"]

    # write dataset link (e.g. http://biogps.org/dataset/BDS_00014/)
    link_dataset = f"http://biogps.org/dataset/{selected_dataset_id}/"
    col_dataset.markdown(
        f"Details of datasets: [{selected_dataset_name} (ID: {selected_dataset_id})]({link_dataset})"
    )

    # --------------------------------------------------
    # fetch CSV data with dataset_id and ncbi_gene_id
    # --------------------------------------------------

    # fetch data from BioGPS
    data_biogps = search_biogps_sync(selected_dataset_id, ncbi_gene_id)
    if data_biogps is None:
        st.warning(
            f"No data found on BioGPS by dataset_id: `{selected_dataset_id}` and ncbi_gene_id: `{ncbi_gene_id}`",
            icon="⚠️",
        )
        return

    # csv データを pandas DataFrame に変換
    csv_text = data_biogps.decode("utf-8")  # bytes to str
    csv_stream = io.StringIO(csv_text)
    df = pd.read_csv(csv_stream).set_index("Samples")
    logger.info(f"BioGPS df index: {df.index}")

    # Probeset の選択（レスポンスデータの CSV のカラムから取得できる）
    probesets = df.columns.tolist()
    selected_probeset = col_probeset.selectbox("Select probeset", options=probesets)

    # データの前処理: probesets ごとにデータを抽出し、prefix が一致する行の平均、標準偏差を計算する
    preprocessed_dfs = {}
    for p in probesets:
        logger.info(f"preprocessing data for probeset: {p}")

        # 特定の probeset のデータを抽出
        df_probeset = df[p]

        # prefix が一致する行の平均、標準偏差を計算
        grouped = df_probeset.groupby(
            df_probeset.index.str.extract(r"([^\.]+)", expand=False)
        )
        se_mean = grouped.mean()
        se_std = grouped.std(ddof=1)

        # rename series
        se_mean.name = f"{p}_mean"
        se_std.name = f"{p}_std"

        # plot 用に平均、標準偏差を結合
        df_plot = pd.concat([se_mean, se_std], axis=1)

        # sort by index desc
        df_plot = df_plot.sort_index(ascending=False)

        # store
        preprocessed_dfs[p] = df_plot

    # --------------------------------------------------
    # write chart
    # --------------------------------------------------

    # 指定されたデータセット、probeset のデータを可視化
    selected_df = preprocessed_dfs[selected_probeset]

    # plot horizontal bar chart with error bar
    title = f"RNA expression of {symbol} (datasets: {selected_dataset_name}, probe: {selected_probeset})"
    fig = go.Figure()
    fig.add_trace(
        go.Bar(
            name=title,
            x=selected_df[f"{selected_probeset}_mean"],
            y=selected_df.index,
            orientation="h",
            error_x={
                "type": "data",
                "array": selected_df[f"{selected_probeset}_std"],
                "visible": True,
                "thickness": 1,
            },
            # style of bar
            marker={
                "color": "rgba(158,202,225,1)",  # バーの塗りつぶし色
                "line": {
                    "color": "rgba(8,48,107,1)",  # 枠線の色
                    "width": 0.5,  # 枠線の太さ
                },
            },
        )
    )

    # configure layout
    fig.update_layout(
        title=title,
        xaxis_title="RNA Expression level",
        yaxis_title="Organs, Tissues, Cell Lines",
        height=1300,
        # space between bars
        bargap=0.4,
        xaxis={
            "showgrid": True,
            "gridcolor": "LightGray",
            "gridwidth": 1,
            "zeroline": True,
        },
        yaxis={
            "tickfont": {"size": 11},
            "showgrid": True,
            "gridcolor": "LightGray",
            "gridwidth": 1,
            "zeroline": True,
        },
        # chart color
        paper_bgcolor=CHART_BACKGROUND_COLOR,
        plot_bgcolor=CHART_BACKGROUND_COLOR,
    )

    # render
    st.plotly_chart(fig, use_container_width=True)

    # --------------------------------------------------
    # write table for download
    # --------------------------------------------------

    toggle = st.toggle(
        "Show source data of above chart",
        key=f"toggle_show_source_data_biogps_{symbol}",
    )
    if toggle:
        st.markdown(
            "As you mouse over the table below, you can download CSV file from popup."
        )

        # preprocessed data for plot
        col_chart_data, col_raw = st.columns(2)
        col_chart_data.markdown("#### Preprocessed Data for Chart")
        col_chart_data.dataframe(selected_df)

        # raw data
        col_raw.markdown("#### Raw Data")
        col_raw.markdown(
            f"Download: http://ds.biogps.org/dataset/csv/{selected_dataset_id}/gene/{ncbi_gene_id}/"
        )
        col_raw.dataframe(df)
