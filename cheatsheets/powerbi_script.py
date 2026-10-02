import pandas as pd
import streamlit as st

from .paths import REFERENCE_DIR


def create_sample_sales():
    dates = pd.date_range("2025-01-01", periods=12, freq="MS")
    regions = ["North", "South", "East", "West"]
    categories = ["Electronics", "Furniture", "Office Supplies", "Accessories"]
    records = []

    for month_index, order_date in enumerate(dates):
        for region_index, region in enumerate(regions):
            for category_index, category in enumerate(categories):
                units = 24 + (month_index * 3) + (region_index * 5) + (category_index * 4)
                unit_price = 38 + (category_index * 27) + (region_index * 6)
                sales = units * unit_price
                cost_rate = 0.61 + ((category_index + region_index) % 4) * 0.035
                records.append(
                    {
                        "OrderDate": order_date,
                        "Region": region,
                        "Category": category,
                        "Units": units,
                        "Sales": sales,
                        "Profit": round(sales * (1 - cost_rate), 2),
                    }
                )

    return pd.DataFrame(records)


def powerbi_cheatsheet():
    st.set_page_config(page_title="CheatSheets | Power BI", page_icon=":material/auto_stories:", layout="wide")
    reference_file = REFERENCE_DIR / "powerbi_cheatsheet.md"
    if not reference_file.is_file():
        st.error(f"Reference file not found: {reference_file.name}")
        st.stop()

    sales = create_sample_sales()
    st.title("Power BI report playground")
    st.caption("Explore a sample sales model with report-style filters and visuals.")

    reference_tab,report_tab = st.tabs(["Cheatsheet", "Report Playground"])
    with reference_tab:
        st.download_button(
            "Download Power BI reference",
            data=reference_file.read_bytes(),
            file_name=reference_file.name,
            mime="text/markdown",
            icon=":material/download:",
        )
        st.markdown(reference_file.read_text(encoding="utf-8"))
    with report_tab:
        filter_columns = st.columns(3)
        regions = ["All regions", *sorted(sales["Region"].unique())]
        categories = ["All categories", *sorted(sales["Category"].unique())]
        years = ["All years", *sorted(sales["OrderDate"].dt.year.unique().tolist())]

        selected_region = filter_columns[0].selectbox("Region", regions, key="powerbi_region")
        selected_category = filter_columns[1].selectbox("Category", categories, key="powerbi_category")
        selected_year = filter_columns[2].selectbox("Year", years, key="powerbi_year")

        filtered = sales
        if selected_region != "All regions":
            filtered = filtered[filtered["Region"] == selected_region]
        if selected_category != "All categories":
            filtered = filtered[filtered["Category"] == selected_category]
        if selected_year != "All years":
            filtered = filtered[filtered["OrderDate"].dt.year == selected_year]

        total_sales = filtered["Sales"].sum()
        total_profit = filtered["Profit"].sum()
        total_units = filtered["Units"].sum()
        profit_margin = total_profit / total_sales if total_sales else 0

        metric_columns = st.columns(4)
        metric_columns[0].metric("Total sales", f"${total_sales:,.0f}")
        metric_columns[1].metric("Total profit", f"${total_profit:,.0f}")
        metric_columns[2].metric("Profit margin", f"{profit_margin:.1%}")
        metric_columns[3].metric("Units", f"{total_units:,}")

        view = st.segmented_control(
            "Visual",
            ["Trend", "Category", "Region", "Data"],
            default="Trend",
            key="powerbi_visual",
        )
        if view == "Trend":
            monthly = filtered.set_index("OrderDate").resample("MS")[["Sales", "Profit"]].sum()
            st.line_chart(monthly, y=["Sales", "Profit"], width="stretch")
        elif view == "Category":
            summary = filtered.groupby("Category")["Sales"].sum().sort_values(ascending=False)
            st.bar_chart(summary, x_label="Category", y_label="Sales", width="stretch")
        elif view == "Region":
            summary = filtered.groupby("Region")["Sales"].sum().sort_values(ascending=False)
            st.bar_chart(summary, x_label="Region", y_label="Sales", width="stretch")
        else:
            st.dataframe(filtered, hide_index=True, width="stretch")

        st.download_button(
            "Download sample data",
            data=filtered.to_csv(index=False).encode("utf-8"),
            file_name="powerbi_sample_sales.csv",
            mime="text/csv",
            icon=":material/download:",
        )

