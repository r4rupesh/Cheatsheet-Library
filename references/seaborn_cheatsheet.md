# Seaborn Quick Reference

Seaborn is a statistical visualization library built on Matplotlib. Pass a pandas DataFrame with `data=` and refer to columns by name.

## Start with a theme

```python
import seaborn as sns
import matplotlib.pyplot as plt

sns.set_theme(style="whitegrid", palette="deep")
fig, ax = plt.subplots(figsize=(9, 5), layout="constrained")
```

## Relationships

```python
sns.scatterplot(data=df, x="Units", y="Sales", hue="Region", ax=ax)
sns.lineplot(data=df, x="Month", y="Sales", hue="Category", marker="o", ax=ax)
```

## Categories

```python
sns.barplot(data=df, x="Region", y="Profit", hue="Category", errorbar=None, ax=ax)
sns.countplot(data=df, x="Category", hue="Region", ax=ax)
```

## Distributions

```python
sns.histplot(data=df, x="Sales", hue="Category", bins=20, multiple="layer", ax=ax)
sns.boxplot(data=df, x="Category", y="Sales", ax=ax)
sns.violinplot(data=df, x="Category", y="Sales", inner="quart", ax=ax)
```

## Statistical relationships

```python
sns.regplot(data=df, x="Units", y="Sales", ax=ax)
sns.heatmap(df.select_dtypes("number").corr(), annot=True, cmap="vlag", ax=ax)
```

## Labels and export

```python
ax.set(title="Sales by region", xlabel="Region", ylabel="Profit ($)")
fig.savefig("plot.png", dpi=180, bbox_inches="tight")
```

The playground includes an editable sales dataset, chart controls, PNG/CSV downloads, and an optional code editor.