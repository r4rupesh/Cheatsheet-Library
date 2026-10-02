from io import BytesIO
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
import streamlit as st
from code_editor import code_editor
from pynteract import Shell

from .paths import REFERENCE_DIR


PALETTES = ["deep", "muted", "colorblind", "Set2", "crest", "viridis"]
STYLES = ["whitegrid", "darkgrid", "white", "ticks"]


def create_sample_sales():
    rng = np.random.default_rng(42)
    records = []
    months = pd.date_range("2025-01-01", periods=12, freq="MS")
    regions = ["North", "South", "East", "West"]
    categories = ["Electronics", "Furniture", "Office Supplies"]
    category_prices = {"Electronics": 180, "Furniture": 240, "Office Supplies": 48}

    for month_index, month in enumerate(months, start=1):
        for region_index, region in enumerate(regions):
            for category_index, category in enumerate(categories):
                units = int(rng.integers(12, 70))
                sales = max(20, category_prices[category] * units + month_index * 85 + region_index * 140 + rng.normal(0, 900))
                margin = 0.16 + category_index * 0.045 + rng.uniform(0, 0.11)
                records.append(
                    {
                        "Month": month.strftime("%b"),
                        "MonthIndex": month_index,
                        "Region": region,
                        "Category": category,
                        "Units": units,
                        "Sales": round(sales, 2),
                        "Profit": round(sales * margin, 2),
                    }
                )

    return pd.DataFrame(records)


def run_seaborn_code(source_code, data):
    plt.close("all")
    shell = st.session_state.get("seaborn_code_shell")
    if shell is None:
        shell = Shell(namespace={}, silent=True, display_mode="last")
        st.session_state["seaborn_code_shell"] = shell
    shell.namespace.update({"sns": sns, "plt": plt, "pd": pd, "np": np, "df": data.copy()})

    response = shell.run(source_code, filename="seaborn_playground.py")
    images = []
    for figure_number in plt.get_fignums():
        figure = plt.figure(figure_number)
        image_buffer = BytesIO()
        figure.savefig(image_buffer, format="png", dpi=180, bbox_inches="tight")
        images.append(image_buffer.getvalue())
        plt.close(figure)

    error = str(response.exception) if response.exception else response.stderr
    return response.stdout, error, images


def seaborn_cheatsheet():
    st.set_page_config(page_title="CheatSheets | Seaborn", page_icon=":material/auto_stories:", layout="wide")
    reference_file = REFERENCE_DIR / "seaborn_cheatsheet.md"
    if not reference_file.is_file():
        st.error(f"Reference file not found: {reference_file.name}")
        st.stop()

    st.title("Seaborn cheatsheet")
    reference_tab, playground_tab = st.tabs(["Cheatsheet", "Playground"])

    with reference_tab:
        st.download_button(
            "Download reference",
            data=reference_file.read_bytes(),
            file_name=reference_file.name,
            mime="text/markdown",
            icon=":material/download:",
        )
        st.markdown(reference_file.read_text(encoding="utf-8"))

    with playground_tab:
        data = st.data_editor(
            create_sample_sales(),
            hide_index=True,
            num_rows="dynamic",
            width="stretch",
            key="seaborn_sales_data",
        )
        st.download_button(
            "Download sample data",
            data=data.to_csv(index=False).encode("utf-8"),
            file_name="seaborn_sample_sales.csv",
            mime="text/csv",
            icon=":material/download:",
        )

        controls = st.columns(4)
        chart_type = controls[0].selectbox(
            "Chart type",
            ["Line", "Bar", "Scatter", "Box", "Violin", "Histogram", "Heatmap"],
            key="seaborn_chart_type",
        )
        palette = controls[1].selectbox("Palette", PALETTES, key="seaborn_palette")
        style = controls[2].selectbox("Style", STYLES, key="seaborn_style")
        hue_options = ["None", *data.select_dtypes(exclude="number").columns.tolist()]
        hue_selection = controls[3].selectbox("Color by", hue_options, key="seaborn_hue")
        hue = None if hue_selection == "None" else hue_selection

        numeric_columns = data.select_dtypes(include="number").columns.tolist()
        categorical_columns = data.select_dtypes(exclude="number").columns.tolist()
        if chart_type == "Heatmap":
            numeric_data = data[numeric_columns].corr(numeric_only=True)
            figure, axes = plt.subplots(figsize=(9, 6), layout="constrained")
            sns.heatmap(numeric_data, annot=True, fmt=".2f", cmap="vlag", center=0, ax=axes)
            axes.set_title("Numeric feature correlation", loc="left")
        else:
            chart_controls = st.columns(3)
            if chart_type == "Histogram":
                value_column = chart_controls[0].selectbox("Values", numeric_columns, key="seaborn_hist_value")
                bins = chart_controls[1].slider("Bins", 5, 40, 16, key="seaborn_hist_bins")
                x_column = value_column
                y_column = None
            else:
                if chart_type in ("Scatter",):
                    x_options = numeric_columns
                elif chart_type in ("Box", "Violin", "Bar"):
                    x_options = categorical_columns
                else:
                    x_options = data.columns.tolist()
                x_column = chart_controls[0].selectbox("X axis", x_options, key="seaborn_x_axis")
                y_options = numeric_columns
                default_y_index = numeric_columns.index("Sales") if "Sales" in numeric_columns else min(1, len(numeric_columns) - 1)
                y_column = chart_controls[1].selectbox("Y axis", y_options, index=default_y_index, key="seaborn_y_axis")
                bins = None
                value_column = None

            chart_title = st.text_input("Chart title", value=f"{chart_type} plot", key="seaborn_chart_title")
            figure, axes = plt.subplots(figsize=(10, 5), layout="constrained")
            sns.set_theme(style=style, palette=palette)
            if chart_type == "Line":
                sns.lineplot(data=data, x=x_column, y=y_column, hue=hue, marker="o", errorbar=None, ax=axes)
            elif chart_type == "Bar":
                sns.barplot(data=data, x=x_column, y=y_column, hue=hue, errorbar=None, ax=axes)
            elif chart_type == "Scatter":
                sns.scatterplot(data=data, x=x_column, y=y_column, hue=hue, alpha=0.8, ax=axes)
            elif chart_type == "Box":
                sns.boxplot(data=data, x=x_column, y=y_column, hue=hue, ax=axes)
            elif chart_type == "Violin":
                sns.violinplot(data=data, x=x_column, y=y_column, hue=hue, inner="quart", ax=axes)
            else:
                sns.histplot(data=data, x=value_column, hue=hue, bins=bins, multiple="layer", ax=axes)
            axes.set_title(chart_title, loc="left", fontsize=16, pad=14)
            axes.spines[["top", "right"]].set_visible(False)
            if chart_type not in ("Histogram",):
                axes.set_xlabel(x_column)
                axes.set_ylabel(y_column)

        st.pyplot(figure, width="stretch")
        image_buffer = BytesIO()
        figure.savefig(image_buffer, format="png", dpi=180, bbox_inches="tight")
        plt.close(figure)
        st.download_button(
            "Download chart as PNG",
            data=image_buffer.getvalue(),
            file_name="seaborn_chart.png",
            mime="image/png",
            icon=":material/download:",
            key="download_seaborn_chart",
        )

        st.subheader("Write your own Seaborn code")
        st.caption("Code runs on this app's server. Run only code you trust. sns, plt, pd, np, and df are ready to use.")
        starter_code = '''fig, ax = plt.subplots(figsize=(8, 4))
sns.scatterplot(data=df, x="Units", y="Sales", hue="Region", ax=ax)
ax.set(title="Units and sales by region")
'''
        st.session_state.setdefault("seaborn_user_code", starter_code)
        editor_response = code_editor(
            st.session_state["seaborn_user_code"],
            lang="python",
            height=280,
            response_mode=["debounce", "blur"],
            key="seaborn_user_code_editor",
        )
        if editor_response.get("type"):
            st.session_state["seaborn_user_code"] = editor_response.get("text", "")

        if st.button("Run Seaborn code", icon=":material/play_arrow:", key="run_seaborn_user_code"):
            output, error, plot_images = run_seaborn_code(st.session_state["seaborn_user_code"], data)
            st.session_state["seaborn_user_output"] = output
            st.session_state["seaborn_user_error"] = error
            st.session_state["seaborn_user_plot_images"] = plot_images

        if st.session_state.get("seaborn_user_output"):
            st.code(st.session_state["seaborn_user_output"], language="text")
        if st.session_state.get("seaborn_user_error"):
            st.error(st.session_state["seaborn_user_error"])
        for image in st.session_state.get("seaborn_user_plot_images", []):
            st.image(image)
