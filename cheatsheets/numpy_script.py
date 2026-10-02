import numpy as np
import streamlit as st
from code_editor import code_editor
from pynteract import Shell

from .paths import REFERENCE_DIR


STARTER_CODE = '''values = np.array([12, 18, 25, 31, 42])
mean_value = values.mean()

print("Values:", values)
print("Mean:", mean_value)
print("Above the mean:", values[values > mean_value])
'''


def numpy_cheatsheet():
    st.set_page_config(page_title="CheatSheets | NumPy", page_icon=":material/auto_stories:", layout="wide")
    reference_file = REFERENCE_DIR / "numpy_cheatsheet.md"
    if not reference_file.is_file():
        st.error(f"Reference file not found: {reference_file.name}")
        st.stop()

    st.title("NumPy cheatsheet")
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
        st.caption("Code runs on this app's server; run only code you trust. The `np` namespace is ready, and variables persist between runs.")
        st.session_state.setdefault("numpy_playground_code", STARTER_CODE)
        editor_response = code_editor(
            st.session_state["numpy_playground_code"],
            lang="python",
            height=280,
            response_mode=["debounce", "blur"],
            key="numpy_playground_editor",
        )
        if editor_response.get("type"):
            st.session_state["numpy_playground_code"] = editor_response.get("text", "")

        if st.button("Run NumPy code", icon=":material/play_arrow:", key="run_numpy_playground"):
            shell = st.session_state.get("numpy_playground_shell")
            if shell is None:
                shell = Shell(
                    namespace={"np": np},
                    silent=True,
                    display_mode="last",
                )
                st.session_state["numpy_playground_shell"] = shell
            shell.namespace["np"] = np
            result = shell.run(
                st.session_state["numpy_playground_code"],
                filename="numpy_playground.py",
            )
            st.session_state["numpy_playground_output"] = result.stdout
            st.session_state["numpy_playground_error"] = (
                str(result.exception) if result.exception else result.stderr
            )

        if st.session_state.get("numpy_playground_output"):
            st.code(st.session_state["numpy_playground_output"], language="text")
        if st.session_state.get("numpy_playground_error"):
            st.error(st.session_state["numpy_playground_error"])
