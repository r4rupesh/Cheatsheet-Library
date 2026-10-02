# Matplotlib Quick Reference

## Start a figure

```python
import matplotlib.pyplot as plt

fig, ax = plt.subplots(figsize=(9, 5), layout="constrained")
```

## Line chart

```python
ax.plot(months, revenue, marker="o", linewidth=2, label="Revenue")
ax.set(title="Revenue by month", xlabel="Month", ylabel="Revenue ($)")
ax.legend()
ax.grid(axis="y", alpha=0.25)
```

## Bar chart

```python
ax.bar(categories, values, color="#167D63")
ax.set(title="Sales by category", xlabel="Category", ylabel="Sales")
```

## Scatter plot

```python
ax.scatter(ad_spend, sales, s=60, alpha=0.8)
ax.set(title="Ad spend vs sales", xlabel="Ad spend", ylabel="Sales")
```

## Histogram

```python
ax.hist(values, bins=12, edgecolor="white")
ax.set(title="Value distribution", xlabel="Value", ylabel="Frequency")
```

## Labels, ticks, and annotations

```python
ax.set_xlabel("Month")
ax.set_ylabel("Revenue ($)")
ax.tick_params(axis="x", rotation=30)
ax.annotate("Peak", xy=(11, 110), xytext=(9, 120), arrowprops={"arrowstyle": "->"})
```

## Save and display

```python
fig.savefig("chart.png", dpi=180, bbox_inches="tight")
plt.show()
```

Use the object-oriented `fig, ax = plt.subplots()` interface for reusable charts. Build the chart in the playground, then download it as a PNG.