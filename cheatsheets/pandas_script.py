import streamlit as st
import pandas as pd
import dataframe_image as dfi
from code_editor import code_editor
from pynteract import Shell

from .paths import DATA_DIR, EXPORT_DIR, REFERENCE_DIR

def editable_cheat_sheet():
    csv_path = DATA_DIR / "pandas_cheatsheet.csv"
    df = pd.read_csv(csv_path)

    st.title("Edit Pandas Cheat Sheet")
    st.write("Here you can edit the Pandas cheat sheet data.")
    with st.form("edit_pandas_cheatsheet"):
        edited_df = st.data_editor(
            df,
            num_rows="dynamic",
            hide_index=True,
            use_container_width=True,
            key="pandas_cheatsheet_editor",
        )
        submitted = st.form_submit_button("Save changes")

    if submitted:
        edited_df.to_csv(csv_path, index=False)
        st.session_state.is_editing_pandas_cheatsheet = False
        st.rerun()

def export_pandas_cheatsheet():
    csv_path = DATA_DIR / "pandas_cheatsheet.csv"
    df = pd.read_csv(csv_path)
    styled_df = (
        df.style
        .hide(axis="index")
        .set_properties(**{"text-align": "center"})
        .set_table_styles([
            {"selector": "th", "props": [("text-align", "center")]},
            {"selector": "td", "props": [("text-align", "center")]},
        ])
    )
    EXPORT_DIR.mkdir(parents=True, exist_ok=True)
    dfi.export(styled_df, str(EXPORT_DIR / "pandas_cheatsheet.png"))
    st.success("Cheat sheet exported to exports/pandas_cheatsheet.png")


def pandas_playground():
    playground_csv = DATA_DIR / "pandas_playground.csv"
    df = pd.read_csv(playground_csv)
    st.caption("Explore the sample sales data. Code runs on this app's server; run only code you trust.")
    st.download_button(
        "Download playground data",
        data=playground_csv.read_bytes(),
        file_name=playground_csv.name,
        mime="text/csv",
        icon=":material/download:",
    )
    df = st.data_editor(
        df,
        hide_index=True,
        num_rows="dynamic",
        width="stretch",
        key="pandas_playground_data",
    )
    starter_code = '''print(df.head())
print("Rows and columns:", df.shape)
print(df.groupby("Region")["Revenue"].sum().sort_values(ascending=False))
'''
    st.session_state.setdefault("pandas_playground_code", starter_code)
    editor_response = code_editor(
        st.session_state["pandas_playground_code"],
        lang="python",
        height=260,
        response_mode=["debounce", "blur"],
        key="pandas_playground_editor",
    )
    if editor_response.get("type"):
        st.session_state["pandas_playground_code"] = editor_response.get("text", "")

    if st.button("Run Pandas code", icon=":material/play_arrow:", key="run_pandas_playground"):
        shell = st.session_state.get("pandas_playground_shell")
        if shell is None:
            shell = Shell(namespace={"pd": pd}, silent=True, display_mode="last")
            st.session_state["pandas_playground_shell"] = shell
        shell.namespace.update({"pd": pd, "df": df.copy()})
        result = shell.run(
            st.session_state["pandas_playground_code"],
            filename="pandas_playground.py",
        )
        st.session_state["pandas_playground_output"] = result.stdout
        st.session_state["pandas_playground_error"] = (
            str(result.exception) if result.exception else result.stderr
        )

    if st.session_state.get("pandas_playground_output"):
        st.code(st.session_state["pandas_playground_output"], language="text")
    if st.session_state.get("pandas_playground_error"):
        st.error(st.session_state["pandas_playground_error"])


def current_cheat_sheet():
    st.set_page_config(page_title="CheatSheets | Pandas", page_icon=":material/auto_stories:", layout="wide")
    if st.session_state.get("is_editing_pandas_cheatsheet", False):
        editable_cheat_sheet()
        return

    st.title("Pandas Cheat Sheet")
    csv_path = DATA_DIR / "pandas_cheatsheet.csv"
    reference_path = REFERENCE_DIR / "pandas_cheatsheet.md"
    df = pd.read_csv(csv_path)
    cheatsheet_tab, playground_tab = st.tabs(["Cheatsheet", "Playground"])
    with cheatsheet_tab:
        st.download_button(
            "Download Markdown cheatsheet",
            data=reference_path.read_bytes(),
            file_name=reference_path.name,
            mime="text/markdown",
            icon=":material/download:",
        )
        st.markdown(reference_path.read_text(encoding="utf-8"))
        st.subheader("Current cheatsheet data")
        st.dataframe(df, hide_index=True, use_container_width=True)

        edit_col, export_col = st.columns(2)
        with edit_col:
            st.button(
                "Edit",
                on_click=lambda: setattr(st.session_state, "is_editing_pandas_cheatsheet", True),
                use_container_width=True,
            )
        with export_col:
            st.button(
                "Export as PNG",
                on_click=export_pandas_cheatsheet,
                use_container_width=True,
            )

    with playground_tab:
        pandas_playground()

