# Pandas Quick Reference

Pandas provides labeled `Series` and two-dimensional `DataFrame` objects for working with tabular data.

## Read and inspect

```python
import pandas as pd

df = pd.read_csv("data.csv")
df.head()
df.shape
df.info()
df.describe()
df["Region"].value_counts()
```

## Select and filter

```python
df["Revenue"]
df[["Region", "Category", "Revenue"]]
df.loc[df["Revenue"] > 500, ["OrderID", "Revenue"]]
df.iloc[:5, :3]
df.query("Units >= 5 and Region == 'North'")
```

## Transform and sort

```python
df["ProfitMargin"] = df["Profit"] / df["Revenue"]
df.sort_values("Revenue", ascending=False)
df.rename(columns={"Revenue": "Sales"})
df.drop(columns=["ProfitMargin"])
df.dropna()
df.fillna(0)
```

## Group and aggregate

```python
df.groupby("Region")["Revenue"].sum()
df.groupby(["Region", "Category"], as_index=False).agg(
    Orders=("OrderID", "count"),
    Revenue=("Revenue", "sum"),
    AverageProfit=("Profit", "mean"),
)
```

## Combine and reshape

```python
pd.merge(orders, customers, on="CustomerID", how="left")
pd.concat([january, february], ignore_index=True)
df.pivot_table(index="Region", columns="Category", values="Revenue", aggfunc="sum")
```

## Dates and export

```python
df["OrderDate"] = pd.to_datetime(df["OrderDate"])
df["Month"] = df["OrderDate"].dt.to_period("M")
df.to_csv("cleaned_data.csv", index=False)
```

The Playground tab uses `pandas_playground.csv` and exposes the dataset as `df` in its code editor.