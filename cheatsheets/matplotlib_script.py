from io import BytesIO
import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st
from code_editor import code_editor
from pynteract import Shell

from .paths import REFERENCE_DIR


COLORS = {
    "Forest": "#167D63",
    "Blue": "#3976C5",
    "Coral": "#D96C52",
    "Gold": "#C89522",
}


def create_sample_data():
    return pd.DataFrame(
        {
            "Month": ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"],
            "MonthIndex": list(range(1, 13)),
            "Revenue": [42, 48, 45, 58, 64, 61, 73, 78, 75, 88, 96, 110],
            "Units": [18, 21, 19, 25, 29, 27, 33, 36, 34, 40, 44, 51],
            "Profit": [11, 13, 12, 16, 18, 17, 21, 23, 22, 26, 29, 34],
        }
    )


def run_custom_matplotlib_code(source_code):
    plt.close("all")
    if "matplotlib_code_shell" not in st.session_state:
        st.session_state["matplotlib_code_shell"] = Shell(
            namespace={},
            silent=True,
            display_mode="last",
        )

    result = st.session_state["matplotlib_code_shell"].run(
        source_code,
        filename="matplotlib_playground.py",
    )
    plot_images = []
    for figure_number in plt.get_fignums():
        figure = plt.figure(figure_number)
        image_file = BytesIO()
        figure.savefig(image_file, format="png", dpi=180, bbox_inches="tight")
        plot_images.append(image_file.getvalue())
        plt.close(figure)

    return result.stdout, str(result.exception) if result.exception else result.stderr, plot_images


def matplotlib_cheatsheet():
    st.set_page_config(page_title="CheatSheets | Matplotlib", page_icon=":material/auto_stories:", layout="wide")
    reference_file = REFERENCE_DIR / "matplotlib_cheatsheet.md"
    if not reference_file.is_file():
        st.error(f"Reference file not found: {reference_file.name}")
        st.stop()

    st.title("Matplotlib cheatsheet")
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
        st.caption("Edit the sample data, choose a chart type, and download the finished plot.")
        data = st.data_editor(
            create_sample_data(),
            hide_index=True,
            num_rows="dynamic",
            width="stretch",
            key="matplotlib_sample_data",
        )

        chart_type = st.selectbox(
            "Chart type",
            ["Line", "Bar", "Scatter", "Histogram"],
            key="matplotlib_chart_type",
        )
        numeric_columns = data.select_dtypes(include="number").columns.tolist()
        control_columns = st.columns(3)
        color_name = control_columns[0].selectbox("Color", list(COLORS), key="matplotlib_color")
        if chart_type == "Histogram":
            value_column = control_columns[1].selectbox("Values", numeric_columns, key="matplotlib_hist_values")
            bins = control_columns[2].slider("Bins", 3, 30, 10, key="matplotlib_hist_bins")
            x_column = None
            y_column = None
        else:
            if chart_type == "Scatter":
                x_options = numeric_columns
            else:
                x_options = data.columns.tolist()
            x_column = control_columns[1].selectbox("X axis", x_options, key="matplotlib_x_axis")
            y_column = control_columns[2].selectbox(
                "Y axis",
                numeric_columns,
                index=min(1, len(numeric_columns) - 1),
                key="matplotlib_y_axis",
            )
            value_column = None
            bins = None

        title = st.text_input("Chart title", value="Monthly performance", key="matplotlib_title")
        figure, axes = plt.subplots(figsize=(10, 5), layout="constrained")
        color = COLORS[color_name]

        if chart_type == "Line":
            axes.plot(data[x_column], data[y_column], marker="o", linewidth=2.5, color=color)
        elif chart_type == "Bar":
            axes.bar(data[x_column].astype(str), data[y_column], color=color, width=0.68)
        elif chart_type == "Scatter":
            axes.scatter(data[x_column], data[y_column], color=color, s=64, alpha=0.85)
        else:
            axes.hist(data[value_column].dropna(), bins=bins, color=color, edgecolor="white")

        axes.set_title(title, loc="left", fontsize=16, pad=14)
        if chart_type == "Histogram":
            axes.set_xlabel(value_column)
            axes.set_ylabel("Frequency")
        else:
            axes.set_xlabel(x_column)
            axes.set_ylabel(y_column)
        axes.spines[["top", "right"]].set_visible(False)
        axes.grid(axis="y", alpha=0.22)
        st.pyplot(figure, width="stretch")

        image_file = BytesIO()
        figure.savefig(image_file, format="png", dpi=180, bbox_inches="tight")
        plt.close(figure)
        st.download_button(
            "Download chart as PNG",
            data=image_file.getvalue(),
            file_name="matplotlib_chart.png",
            mime="image/png",
            icon=":material/download:",
            key="download_matplotlib_chart",
        )

        st.subheader("Write your own Matplotlib code")
        st.caption("Code runs on this app's server. Run only code you trust. You do not need to call plt.show().")
        starter_code = '''import matplotlib.pyplot as plt

months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun"]
sales = [12, 18, 15, 24, 28, 35]

fig, ax = plt.subplots(figsize=(8, 4))
ax.plot(months, sales, marker="o", color="#167D63")
ax.set(title="Monthly sales", xlabel="Month", ylabel="Sales")
ax.grid(axis="y", alpha=0.25)
'''
        st.session_state.setdefault("matplotlib_user_code", starter_code)
        editor_response = code_editor(
            st.session_state["matplotlib_user_code"],
            lang="python",
            height=300,
            response_mode=["debounce", "blur"],
            key="matplotlib_user_code_editor",
        )
        if editor_response.get("type"):
            st.session_state["matplotlib_user_code"] = editor_response.get("text", "")

        if st.button("Run Matplotlib code", icon=":material/play_arrow:", key="run_matplotlib_user_code"):
            output, error, user_plot_images = run_custom_matplotlib_code(
                st.session_state["matplotlib_user_code"]
            )
            st.session_state["matplotlib_user_output"] = output
            st.session_state["matplotlib_user_error"] = error
            st.session_state["matplotlib_user_plot_images"] = user_plot_images

        if st.session_state.get("matplotlib_user_output"):
            st.code(st.session_state["matplotlib_user_output"], language="text")
        if st.session_state.get("matplotlib_user_error"):
            st.error(st.session_state["matplotlib_user_error"])
        for user_plot_image in st.session_state.get("matplotlib_user_plot_images", []):
            st.image(user_plot_image)
