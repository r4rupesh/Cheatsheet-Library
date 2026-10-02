import streamlit as st


TOOL_CATEGORIES = [
    ("Python", "Core syntax and runnable code"),
    ("Pandas", "Tabular data and analysis"),
    ("Excel", "Formulas and spreadsheet practice"),
    ("SQL", "Queries and sample tables"),
    ("Power BI", "Interactive business reports"),
    ("NumPy", "Arrays and numerical computing"),
    ("Matplotlib", "Build and export charts"),
    ("Seaborn", "Statistical data visualization"),
    ("Scikit-learn", "Machine learning models"),
    ("SciPy", "Scientific and statistical tools"),
]


def choose_category(category):
    st.session_state["category_picker"] = category


def return_home():
    st.session_state["category_picker"] = None


def show_home():
    st.title("CheatSheets", icon=":material/auto_stories:")
    st.html(f"""
    <style>
    @keyframes home-enter {{
        from {{ opacity: 0; transform: translateY(14px); }}
        to {{ opacity: 1; transform: translateY(0); }}
    }}
    .home-intro {{
        padding: 28px 30px;
        margin: 4px 0 26px;
        border-left: 6px solid #e7b765;
        background-color: #183f36;
        background-image: repeating-linear-gradient(135deg, transparent 0 22px, rgba(255,255,255,.035) 22px 23px);
        color: #f5f7f2;
        animation: home-enter .7s ease-out both;
    }}
    .home-intro-kicker {{
        margin: 0 0 12px;
        color: #e7b765;
        font-size: 12px;
        font-weight: 700;
    }}
    .home-intro h1 {{
        margin: 0 0 10px;
        color: #f5f7f2;
        font-family: Georgia, 'Times New Roman', serif;
        font-size: 42px;
        line-height: 1.08;
    }}
    .home-intro-copy {{
        margin: 0;
        max-width: 640px;
        color: #d2ded6;
        font-size: 16px;
    }}
    @media (max-width: 640px) {{
        .home-intro {{ padding: 22px 20px; }}
        .home-intro h1 {{ font-size: 34px; }}
    }}
    @media (prefers-reduced-motion: reduce) {{
        .home-intro {{ animation: none; }}
    }}
    </style>
    <section class="home-intro">
        <p class="home-intro-kicker">CHEATSHEET LIBRARY · {len(TOOL_CATEGORIES)} TOPICS</p>
        <h1>Learn a tool. Try it live.</h1>
        <p class="home-intro-copy">Compact references and practical sandboxes for working with data, code, and charts.</p>
    </section>
    """)

    st.subheader("Browse tools")
    for row_start in range(0, len(TOOL_CATEGORIES), 3):
        columns = st.columns(3)
        for column, (name, description) in zip(
            columns,
            TOOL_CATEGORIES[row_start:row_start + 3],
        ):
            with column:
                with st.container(border=True):
                    st.markdown(f"**{name}**")
                    st.caption(description)
                    st.button(
                        "Open",
                        key=f"open_{name.lower().replace(' ', '_')}",
                        icon=":material/arrow_forward:",
                        on_click=choose_category,
                        args=(name,),
                        width="stretch",
                    )


st.set_page_config(
    page_title="CheatSheets | Learn & Practice",
    page_icon=":material/auto_stories:",
    layout="wide",
)

category = st.session_state.get("category_picker")
if category is None:
    show_home()
else:
    st.button(
        "Back to tools",
        key="back_to_tools",
        icon=":material/arrow_back:",
        on_click=return_home,
    )

    if category == "Python":
        from cheatsheets.python_script import python_cheatsheet

        python_cheatsheet()
    elif category == "Pandas":
        from cheatsheets.pandas_script import current_cheat_sheet

        current_cheat_sheet()
    elif category == "Excel":
        from cheatsheets.excel_script import excel_cheatsheet

        excel_cheatsheet()
    elif category == "SQL":
        from cheatsheets.sql_script import sql_cheatsheet

        sql_cheatsheet()
    elif category == "Power BI":
        from cheatsheets.powerbi_script import powerbi_cheatsheet

        powerbi_cheatsheet()
    elif category == "NumPy":
        from cheatsheets.numpy_script import numpy_cheatsheet

        numpy_cheatsheet()
    elif category == "Matplotlib":
        from cheatsheets.matplotlib_script import matplotlib_cheatsheet

        matplotlib_cheatsheet()
    elif category == "Seaborn":
        from cheatsheets.seaborn_script import seaborn_cheatsheet

        seaborn_cheatsheet()
    elif category == "Scikit-learn":
        from cheatsheets.scikit_learn_script import scikit_learn_cheatsheet

        scikit_learn_cheatsheet()
    elif category == "SciPy":
        from cheatsheets.scipy_script import scipy_cheatsheet

        scipy_cheatsheet()
    else:
        return_home()
        st.rerun()