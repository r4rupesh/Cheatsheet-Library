import sqlite3

import pandas as pd
import streamlit as st
from code_editor import code_editor

from .paths import REFERENCE_DIR


STARTER_QUERY = """SELECT departments.name AS department,
       COUNT(employees.employee_id) AS employee_count,
       ROUND(AVG(employees.salary), 2) AS average_salary
FROM departments
LEFT JOIN employees USING (department_id)
GROUP BY departments.department_id
ORDER BY average_salary DESC;"""

READ_ONLY_ACTIONS = {
    sqlite3.SQLITE_SELECT,
    sqlite3.SQLITE_READ,
    sqlite3.SQLITE_FUNCTION,
    sqlite3.SQLITE_RECURSIVE,
}


def create_sample_database():
    connection = sqlite3.connect(":memory:")
    connection.row_factory = sqlite3.Row
    connection.executescript(
        """
        CREATE TABLE departments (
            department_id INTEGER PRIMARY KEY,
            name TEXT NOT NULL
        );
        CREATE TABLE employees (
            employee_id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            title TEXT NOT NULL,
            department_id INTEGER NOT NULL,
            salary REAL NOT NULL,
            FOREIGN KEY (department_id) REFERENCES departments(department_id)
        );
        INSERT INTO departments VALUES
            (1, 'Engineering'), (2, 'Design'), (3, 'Operations'), (4, 'Research');
        INSERT INTO employees VALUES
            (1, 'Avery Chen', 'Software Engineer', 1, 118000),
            (2, 'Jordan Patel', 'Data Engineer', 1, 106000),
            (3, 'Morgan Lee', 'Product Designer', 2, 92000),
            (4, 'Riley Morgan', 'UX Researcher', 2, 88000),
            (5, 'Casey Rivera', 'Operations Analyst', 3, 76000),
            (6, 'Taylor Brooks', 'Research Scientist', 4, 124000),
            (7, 'Jamie Kim', 'Research Analyst', 4, 97000);
        """
    )
    connection.set_authorizer(
        lambda action, _arg1, _arg2, _database, _trigger: (
            sqlite3.SQLITE_OK if action in READ_ONLY_ACTIONS else sqlite3.SQLITE_DENY
        )
    )
    return connection


def run_read_only_query(query):
    connection = create_sample_database()
    try:
        cursor = connection.execute(query)
        if cursor.description is None:
            raise ValueError("Enter a query that returns rows, such as SELECT.")
        rows = cursor.fetchall()
        return pd.DataFrame(rows, columns=[column[0] for column in cursor.description])
    finally:
        connection.close()


def sql_cheatsheet():
    st.set_page_config(page_title="CheatSheets | SQL", page_icon=":material/auto_stories:", layout="wide")
    cheatsheet_file = REFERENCE_DIR / "sql_cheatsheet.sql"
    if not cheatsheet_file.is_file():
        st.error(f"Cheatsheet not found: {cheatsheet_file.name}")
        st.stop()

    st.title("SQL cheatsheet")
    st.download_button(
        "Download SQL cheatsheet",
        data=cheatsheet_file.read_bytes(),
        file_name=cheatsheet_file.name,
        mime="text/sql",
        icon=":material/download:",
    )

    cheatsheet_tab, playground_tab = st.tabs(["Cheatsheet", "Playground"])
    with cheatsheet_tab:
        st.code(cheatsheet_file.read_text(encoding="utf-8"), language="sql")

    with playground_tab:
        st.caption("Practice read-only queries against the sample employees and departments tables.")
        with st.expander("Sample data", expanded=False):
            connection = create_sample_database()
            try:
                for table_name in ("employees", "departments"):
                    st.markdown(f"**{table_name}**")
                    preview = pd.read_sql_query(f"SELECT * FROM {table_name}", connection)
                    st.dataframe(preview, hide_index=True, width="stretch")
            finally:
                connection.close()

        st.session_state.setdefault("sql_playground_query", STARTER_QUERY)
        editor_response = code_editor(
            st.session_state["sql_playground_query"],
            lang="sql",
            height=250,
            response_mode=["debounce", "blur"],
            key="sql_playground_editor",
        )
        if editor_response.get("type"):
            st.session_state["sql_playground_query"] = editor_response.get("text", "")

        if st.button("Run query", icon=":material/play_arrow:", key="run_sql_playground"):
            try:
                result = run_read_only_query(st.session_state["sql_playground_query"])
                st.session_state["sql_playground_result"] = result
                st.session_state.pop("sql_playground_error", None)
            except Exception as error:
                st.session_state.pop("sql_playground_result", None)
                st.session_state["sql_playground_error"] = str(error)

        if "sql_playground_result" in st.session_state:
            st.dataframe(st.session_state["sql_playground_result"], hide_index=True, width="stretch")
        if st.session_state.get("sql_playground_error"):
            st.error(st.session_state["sql_playground_error"])
