import copy
import csv
import io
import statistics

import numpy as np
import pandas as pd
import plotly.graph_objects as go
import streamlit as st

from app.constants import CHART_BACKGROUND_COLOR, DATA_SOURCE_NAME_DICE
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
            Status of search results may be "No data found..." if you search by gene synonyms and Ensembl ID.

            Now, gene-searcher doesn't support search by gene synonyms and Ensembl ID on DICE.
            You can search by query like `IL2RA` (**query is character sensitive**), but cannot search by query like `CD25` and `ENSG00000134460`.

            Please search by upper-cased gene symbol name.
            """
        )
        return

    # write gene info
    # TBD: API から取得できるのは CSV データのみなので、ここでは遺伝子情報を表示しない

    # write link
    gene = query.upper()
    link = f"https://dice-database.org/genes/{gene}"
    st.markdown(
        f"""
        #### General Information

        Data source: {link}
        """
    )

    # ------------------------------
    # データの前処理
    # ------------------------------

    logger.info("starting to preprocess data from DICE API...")

    # CSV バイナリデータを BytesIO に変換
    data_dice: bytes
    csv_text = data_dice.decode("utf-8")
    csv_stream = io.StringIO(csv_text)
    reader = csv.reader(csv_stream)

    # データの質が悪く、カラム数が異なる行が混じっているため、1 行ずつデータを読込、計算する
    # 1 行目はヘッダー、2 行目以降はデータ
    stats_list = []
    for i, row in enumerate(reader):
        if i == 0:
            continue

        # 1 列目は cell type, 2 列目以降は expression level [TPM]
        cell_type = row[0]
        expression_levels = row[1:]

        # calculate mean, median, min, max
        expression_levels = list(map(float, expression_levels))
        mean = statistics.mean(expression_levels)
        median = statistics.median(expression_levels)
        min_ = min(expression_levels)
        max_ = max(expression_levels)

        # append to data_for_box_plot

        # append to stats_list
        stats_list.append(
            {
                "cell_type": cell_type,
                "mean": mean,
                "median": median,
                "min": min_,
                "max": max_,
                "raw_data": expression_levels,
            }
        )

    # deep copy stats_list
    stats_list_for_boxplot = copy.deepcopy(stats_list)

    # create DataFrame
    for d in stats_list:
        # raw_data があるままだと DataFrame に変換できないため削除
        del d["raw_data"]
    df_stats = pd.DataFrame(stats_list).set_index("cell_type")

    # sort by median desc (ref: https://dice-database.org/genes/IL2RA)
    df_stats = df_stats.sort_values("median", ascending=False)
    logger.info(f"df_stats shape: {df_stats.shape}")
    logger.info(f"df_stats rows: {df_stats.index}")
    logger.info("done preprocessing data from DICE API!")

    # ------------------------------
    # write contents
    # ------------------------------

    # write horizontal box plot
    # ref: https://dice-database.org/genes/IL2RA
    fig = go.Figure()

    # sort by median desc
    stats_list_for_boxplot = sorted(
        stats_list_for_boxplot, key=lambda x: x["median"], reverse=False
    )

    # get min, max
    data_min = df_stats["min"].min()
    data_max = df_stats["max"].max()
    # 最小値が0の場合の処理
    if data_min <= 0:
        data_min = min(filter(lambda x: x > 0, df_stats["min"]))

    # 範囲の計算 (min - 1, max + 1) に収める
    range_min = 10 ** np.floor(np.log10(data_min))
    range_max = 10 ** np.ceil(np.log10(data_max))

    # 各細胞タイプに対してボックスプロットを追加
    for stats in stats_list_for_boxplot:
        cell_type = stats["cell_type"]
        data = stats["raw_data"]
        fig.add_trace(
            go.Box(
                x=data,
                name=cell_type,
                boxpoints=False,  # only whiskers
                line_color="black",
                fillcolor="rgba(255,199,47,0.5)",  # transparent
                # tooltip
                hoverinfo="none",
                hovertemplate=f"<b>{stats['cell_type']}</b><br>"
                + f"Mean: {stats['mean']}<br>"
                + f"Median: {stats['median']}<br>"
                + f"Min: {stats['min']}<br>"
                + f"Max: {stats['max']}<br>",
            )
        )

    # レイアウトの設定
    fig.update_layout(
        title=f"RNA expression of {gene} by immune cell types",
        xaxis_title="Trascripts per million [TPM]",
        yaxis_title="Cell Type",
        showlegend=False,
        width=650,
        height=600,
        xaxis={
            "type": "log",
            "range": [np.log10(range_min), np.log10(range_max)],
            "tickformat": ".1e",
            "dtick": 1,
            "tickfont": {"size": 12},
            "showgrid": True,
            "gridcolor": "LightGray",
            "gridwidth": 1,
            "zeroline": True,
        },
        yaxis={
            "tickfont": {"size": 12},
            "showgrid": True,
            "gridcolor": "LightGray",
            "gridwidth": 1,
            "zeroline": True,
        },
        # chart color
        paper_bgcolor=CHART_BACKGROUND_COLOR,
        plot_bgcolor=CHART_BACKGROUND_COLOR,
    )
    st.markdown("#### Data")
    st.plotly_chart(fig, use_container_width=False)
    # if mobile use_container_width=True
    # if desktop use_container_width=False

    # write table for download
    toggle = st.toggle(
        "Show source data of above chart", key=f"toggle_show_source_data_dice_{gene}"
    )
    if toggle:
        st.markdown(
            "As you mouse over the table below, you can download CSV file from popup."
        )
        st.dataframe(df_stats)
