import base64
import json

import nbformat
import streamlit as st
from nbconvert import HTMLExporter
from playwright.sync_api import sync_playwright
from code_editor import code_editor
from pynteract import Shell

from .paths import DATA_DIR, REFERENCE_DIR


def playground():
    
    st.subheader("Python playground")
    st.caption("Code runs on this app's server. Run only code you trust.")

    starter_code = 'print("Hello from Python!")\n2 + 2'
    st.session_state.setdefault("python_playground_code", starter_code)
    editor_response = code_editor(
        st.session_state["python_playground_code"],
        lang="python",
        height=240,
        response_mode=["debounce", "blur"],
        key="python_playground_editor",
    )
    if editor_response.get("type"):
        st.session_state["python_playground_code"] = editor_response.get("text", "")

    if st.button("Run code", icon=":material/play_arrow:", key="run_python_playground"):
        if "python_playground_shell" not in st.session_state:
            st.session_state["python_playground_shell"] = Shell(
                namespace={},
                silent=True,
                display_mode="last",
            )
        result = st.session_state["python_playground_shell"].run(
            st.session_state["python_playground_code"],
            filename="python_playground.py",
        )
        st.session_state["python_playground_output"] = result.stdout
        st.session_state["python_playground_error"] = (
            str(result.exception) if result.exception else result.stderr
        )

    if st.session_state.get("python_playground_output"):
        st.code(st.session_state["python_playground_output"], language="text")
    if st.session_state.get("python_playground_error"):
        st.error(st.session_state["python_playground_error"])



@st.cache_data(show_spinner=False)
def create_notebook_exports(notebook_bytes):
    notebook = nbformat.reads(notebook_bytes.decode("utf-8"), as_version=4)
    html, _ = HTMLExporter(template_name="lab").from_notebook_node(notebook)

    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(
            headless=True,
            executable_path=playwright.chromium.executable_path,
        )
        try:
            page = browser.new_page(
                viewport={"width": 1440, "height": 1000},
                device_scale_factor=1,
            )
            page.set_content(html, wait_until="networkidle")
            pdf_bytes = page.pdf(format="A4", print_background=True)
            image_bytes = page.screenshot(full_page=True)
        finally:
            browser.close()

    return pdf_bytes, image_bytes


def python_cheatsheet():
    st.set_page_config(page_title="CheatSheets | Python", page_icon=":material/auto_stories:", layout="wide")
    notebook_file = DATA_DIR / "python_cheatsheet.ipynb"
    reference_file = REFERENCE_DIR / "python_cheatsheet.md"
    if not notebook_file.is_file():
        st.error(f"Notebook not found: {notebook_file.name}")
        st.stop()
    
    cheatsheet_tab, playground_tab = st.tabs(["Cheatsheet", "Playground"])
    with cheatsheet_tab:
        st.caption(notebook_file.name)
        notebook_bytes = notebook_file.read_bytes()
        notebook_json = json.loads(notebook_bytes)
        pdf_bytes, image_bytes = create_notebook_exports(notebook_bytes)

        download_columns = st.columns(4)
        with download_columns[0]:
            st.download_button(
                "Download Markdown",
                data=reference_file.read_bytes(),
                file_name=reference_file.name,
                mime="text/markdown",
                icon=":material/download:",
            )
        with download_columns[1]:
            st.download_button(
                "Download .ipynb",
                data=notebook_bytes,
                file_name=notebook_file.name,
                mime="application/x-ipynb+json",
                icon=":material/download:",
            )
        with download_columns[2]:
            st.download_button(
                "Download PDF",
                data=pdf_bytes,
                file_name=f"{notebook_file.stem}.pdf",
                mime="application/pdf",
                icon=":material/download:",
            )
        with download_columns[3]:
            st.download_button(
                "Download PNG",
                data=image_bytes,
                file_name=f"{notebook_file.stem}.png",
                mime="image/png",
                icon=":material/download:",
            )

        st.markdown(reference_file.read_text(encoding="utf-8"))

        for cell in notebook_json.get("cells", []):
            source = cell.get("source", [])
            content = source if isinstance(source, str) else "".join(source)
            if not content.strip():
                continue

            cell_type = cell.get("cell_type")
            if cell_type == "markdown":
                st.markdown(content)
            elif cell_type == "code":
                language = cell.get("metadata", {}).get("language", "python")
                st.code(content, language=language)

                for output in cell.get("outputs", []):
                    output_text = output.get("text")
                    if output_text:
                        st.text("".join(output_text) if isinstance(output_text, list) else output_text)

                    output_data = output.get("data", {})
                    if "image/png" in output_data:
                        image = output_data["image/png"]
                        st.image(base64.b64decode("".join(image) if isinstance(image, list) else image))
                    elif "text/html" in output_data:
                        html = output_data["text/html"]
                        st.html("".join(html) if isinstance(html, list) else html)
                    elif "text/markdown" in output_data:
                        markdown = output_data["text/markdown"]
                        st.markdown("".join(markdown) if isinstance(markdown, list) else markdown)
                    elif "text/plain" in output_data:
                        plain_text = output_data["text/plain"]
                        st.text("".join(plain_text) if isinstance(plain_text, list) else plain_text)

                    if output.get("output_type") == "error":
                        st.code("\n".join(output.get("traceback", [])), language="text")

    with playground_tab:
        playground()


