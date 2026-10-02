# Power BI Quick Reference

## Core workflow

1. Import and transform source data in Power Query.
2. Set column data types and remove invalid or duplicate rows.
3. Build a star schema with dimension tables around a fact table.
4. Create relationships using matching keys and a clear filter direction.
5. Add DAX measures for aggregations and time intelligence.
6. Choose visuals that answer a specific question, then add slicers for exploration.

## DAX measures

```DAX
Total Sales = SUM(Sales[Sales])

Total Profit = SUM(Sales[Profit])

Profit Margin = DIVIDE([Total Profit], [Total Sales], 0)

Order Count = DISTINCTCOUNT(Sales[OrderID])

Average Order Value = DIVIDE([Total Sales], [Order Count], 0)

Sales YTD = TOTALYTD([Total Sales], 'Date'[Date])

Sales Previous Year =
    CALCULATE([Total Sales], SAMEPERIODLASTYEAR('Date'[Date]))

Sales YoY Change =
    DIVIDE([Total Sales] - [Sales Previous Year], [Sales Previous Year], 0)
```

## Filter context

```DAX
Electronics Sales =
    CALCULATE([Total Sales], Product[Category] = "Electronics")

Sales for Selected Region =
    CALCULATE([Total Sales], KEEPFILTERS(Region[Name]))
```

`CALCULATE` evaluates an expression under modified filter context. Prefer measures for reusable calculations; use calculated columns when a value must be stored per row.

## Power Query M

```powerquery
let
    Source = Excel.Workbook(File.Contents("Sales.xlsx"), null, true),
    SalesSheet = Source{[Item="Sales", Kind="Sheet"]}[Data],
    Headers = Table.PromoteHeaders(SalesSheet, [PromoteAllScalars=true]),
    TypedColumns = Table.TransformColumnTypes(
        Headers,
        {{"OrderDate", type date}, {"Sales", Currency.Type}, {"Profit", Currency.Type}}
    )
in
    TypedColumns
```

## Visual selection

- Line chart: trends over time.
- Bar or column chart: compare categories or regions.
- Card: highlight one key measure.
- Matrix: compare measures across multiple dimensions.
- Slicer: let report viewers filter by date, region, or category.

The playground uses an illustrative sample sales dataset. It is not a Power BI Desktop model and does not execute DAX; use the formulas above in Power BI Desktop.