# Power BI Dashboard Guide (about 1-2 hours)

Power BI Desktop is free (Windows): https://powerbi.microsoft.com/desktop

## 1. Load data
1. Home > Get Data > Text/CSV > select `data/superstore_clean.csv` > **Transform Data**.
2. In Power Query check the types: Order Date and Ship Date = Date, Sales/Profit = Decimal, Discount = Decimal, Year = Whole number. Close & Apply.

## 2. Create a Date table (Modeling > New Table)
```DAX
DateTable = CALENDAR(MIN(superstore_clean[Order Date]), MAX(superstore_clean[Order Date]))
```
Add columns: `Year = YEAR(DateTable[Date])`, `Month = FORMAT(DateTable[Date],"MMM")`, `MonthNo = MONTH(DateTable[Date])`.
Sort Month by MonthNo. Model view: drag DateTable[Date] to superstore_clean[Order Date] (one-to-many).

## 3. DAX measures (Modeling > New Measure)
```DAX
Total Sales    = SUM(superstore_clean[Sales])
Total Profit   = SUM(superstore_clean[Profit])
Total Orders   = DISTINCTCOUNT(superstore_clean[Order ID])
Profit Margin  = DIVIDE([Total Profit], [Total Sales], 0)
Avg Ship Days  = AVERAGE(superstore_clean[Ship Days])
Sales LY       = CALCULATE([Total Sales], SAMEPERIODLASTYEAR(DateTable[Date]))
YoY Growth %   = DIVIDE([Total Sales] - [Sales LY], [Sales LY], 0)
Loss Lines     = CALCULATE(COUNTROWS(superstore_clean), superstore_clean[Profit] < 0)
```

## 4. Page layout
| Visual | Fields |
|---|---|
| 4 **Card** visuals (top row) | Total Sales, Total Profit, Total Orders, Profit Margin |
| **Line chart** | Axis: DateTable[Date] (Year > Month), Values: Total Sales, Total Profit |
| **Clustered bar** | Axis: Category, Values: Total Sales, Total Profit |
| **Filled map** or **Treemap** | Location/Group: State or Region, Size: Total Sales |
| **Bar chart (sorted)** | Axis: Sub-Category, Values: Total Profit (conditional colour: negative = red) |
| **Column chart** (the story) | Axis: a Discount band, Values: Profit Margin. Create the band as a calculated column (below) |
| **Table** | Customer Name, Total Sales, Total Profit (Top N filter = 10) |
| **Slicers** | Year, Region, Segment, Category |

Discount band column:
```DAX
Discount Band =
SWITCH(TRUE(),
  superstore_clean[Discount] = 0, "0%",
  superstore_clean[Discount] <= 0.2, "1-20%",
  superstore_clean[Discount] <= 0.4, "21-40%",
  ">40%")
```

## 5. Finish
- Title: "Retail Sales Performance Dashboard"; use one colour theme (View > Themes).
- Add a text box with 3 insights (see README).
- File > Save as `powerbi/Retail_Sales_Dashboard.pbix`. Take a screenshot and save it in `screenshots/`.
