# CheatSheets Library

CheatSheets Library is a Streamlit learning app with concise references and hands-on practice areas for popular data tools.

**Jump to:** [Tools](#tools) · [Features](#features) · [Project layout](#project-layout) · [Run locally](#run-locally)

## Tools

| Tool | What you can explore | Source | Reference |
| --- | --- | --- | --- |
| Python | Notebook reference and code playground | [Python page](cheatsheets/python_script.py) | [Python guide](references/python_cheatsheet.md) |
| Pandas | DataFrame cheatsheet and sample-data playground | [Pandas page](cheatsheets/pandas_script.py) | [Pandas guide](references/pandas_cheatsheet.md) |
| Excel | Formula practice and workbook download | [Excel page](cheatsheets/excel_script.py) | [Workbook](data/excel_cheatsheet.xlsx) |
| SQL | Read-only query playground | [SQL page](cheatsheets/sql_script.py) | [SQL guide](references/sql_cheatsheet.sql) |
| Power BI | Filterable sample report | [Power BI page](cheatsheets/powerbi_script.py) | [Power BI guide](references/powerbi_cheatsheet.md) |
| NumPy | Array operations playground | [NumPy page](cheatsheets/numpy_script.py) | [NumPy guide](references/numpy_cheatsheet.md) |
| Matplotlib | Chart builder and code playground | [Matplotlib page](cheatsheets/matplotlib_script.py) | [Matplotlib guide](references/matplotlib_cheatsheet.md) |
| Seaborn | Statistical chart playground | [Seaborn page](cheatsheets/seaborn_script.py) | [Seaborn guide](references/seaborn_cheatsheet.md) |
| Scikit-learn | Classification and regression models | [Scikit-learn page](cheatsheets/scikit_learn_script.py) | [Scikit-learn guide](references/scikit_learn_cheatsheet.md) |
| SciPy | Integration, optimization, statistics, and signals | [SciPy page](cheatsheets/scipy_script.py) | [SciPy guide](references/scipy_cheatsheet.md) |

## Features

<details>
<summary>References and downloads</summary>

Each tool has a concise guide. Depending on the tool, the app also provides downloadable notebooks, workbooks, charts, query results, or sample data.

</details>

<details>
<summary>Interactive playgrounds</summary>

Try Python and data-library code, edit sample tables, evaluate spreadsheet formulas, run read-only SQL queries, explore model metrics, and adjust charts.

Code playgrounds execute on the app server. Run only code you trust.

</details>

## Project layout

- [`script.py`](script.py): app entry point and home navigation.
- [`cheatsheets/`](cheatsheets): Streamlit pages and shared path configuration.
- [`data/`](data): notebook, workbook, and CSV datasets.
- [`references/`](references): Markdown and SQL reference files.
- [`scripts/`](scripts): utility scripts, including the notebook generator.
- [`exports/`](exports): generated exports.

## Run locally

<details>
<summary>Windows PowerShell setup</summary>

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
streamlit run script.py
```

After the server starts, open [http://localhost:8506](http://localhost:8506) or the URL printed by Streamlit.

</details>

See [requirements.txt](requirements.txt) for the app dependencies.